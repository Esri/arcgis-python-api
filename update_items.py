#!/usr/bin/env python
"""
Used by Esri staff for uploading sample notebooks from this gallery to an
arbitrary AGOL organization.

Requires external packages `arcgis`, `yaml`, nbconvert, nbformat. Install via

conda install -c esri arcgis
conda install pyyaml
conda install nbconvert
conda install nbformat

"""

import argparse
import json
import logging
import os
import re
import sys
import traceback

import nbformat
import requests
import yaml
from arcgis.gis import GIS
from nbconvert import HTMLExporter

log = logging.getLogger(__name__)

ITEMS_METADATA_YAML_PATH = os.path.join(".", "items_metadata.yaml")
THUMBNAILS_DIR = os.path.join(".", "static", "thumbnails")
REPLACE_PROFILES_SCRIPT = os.path.join(".", "misc", "tools",
                                       "replace_profiles.py")

NB_PORTAL_TYPE = "Notebook"
NB_PORTAL_TYPE_KEYWORDS = "Notebook, Python"
NB_ITEM_PROPERTIES_RUNTIME_STAMP_ADVANCED = \
    {'notebookRuntimeName': 'ArcGIS Notebook Python 3 Advanced',
     'notebookRuntimeVersion': ''}
NB_ITEM_PROPERTIES_RUNTIME_STAMP_ADVANCED_GPU = \
    {'notebookRuntimeName': 'ArcGIS Notebook Python 3 Advanced with GPU support',
     'notebookRuntimeVersion': ''}
NB_ITEM_PROPERTIES_RUNTIME_STAMP_STANDARD = \
    {'notebookRuntimeName': 'ArcGIS Notebook Python 3 Standard',
     'notebookRuntimeVersion': ''}
NB_ITEM_FOLDER = "Notebook Samples"


def _main():
    """Parses arguments, connects to GIS, reads YAML, uploads NBs"""
    args = _parse_cmd_line_args()
    _setup_logging(args)
    gis = GIS(args.portal_url, args.username,
              args.password, verify_cert=False)
    if args.version:
        NB_ITEM_PROPERTIES_RUNTIME_STAMP_ADVANCED["notebookRuntimeVersion"] = args.version
        NB_ITEM_PROPERTIES_RUNTIME_STAMP_STANDARD["notebookRuntimeVersion"] = args.version
    else:
        _get_current_runtime(gis)
    items_metadata_yaml = _read_items_metadata_yaml()
    if args.replace_profiles:
        _replace_profiles()
    s = ItemsUploader(gis, items_metadata_yaml)
    s.upload_items()
    if s.failed_uploads:
        raise Exception(f"Some uploads failed: {s.failed_uploads}")


def _parse_cmd_line_args():
    """Parse CMD args, returns an object instance of all user passed in args"""
    parser = argparse.ArgumentParser(description="Takes all notebooks "
                                     "this in `gallery` directory, and will upload it to the specified "
                                     "portal/org in the right group with the right categories. "
                                     "(default is geosaurus.maps.arcgis.com, 'Esri Sample Notebooks' group)",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--username", "-u", type=str,
                        help="Required username for the portal/org")
    parser.add_argument("--password", "-p", type=str,
                        help="Required password for the portal/org")
    parser.add_argument("--portal-url", "-r", type=str,
                        help="The portal to connect to (default: geosaurus.maps.arcgis.com)",
                        default="https://geosaurus.maps.arcgis.com/")
    parser.add_argument("--version", "-ver", type=str,
                        help="The version of notebook runtime to set on sample notebooks "
                        "(default: the latest version)",
                        default="")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print all DEBUG log messages instead of just INFO")
    parser.add_argument("--replace-profiles", "-c", action="store_true",
                        help="Replace all profiles in notebooks with their appropriate username "
                        "and passwords. Does this by running misc/tools/replace_profiles.py")
    args = parser.parse_args(sys.argv[1:])  # don't use filename as 1st arg
    return args


def _setup_logging(args):
    """Sets up the logging based on args"""
    if args.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(logging.Formatter(
        '-----    %(levelname)s    |    '
        '%(asctime)s    |    '
        '%(filename)s line %(lineno)d'
        '     -----\n'
        '"%(message)s"'))
    log.addHandler(stdout_handler)
    log.info("Logging at level {}.".format(logging.getLevelName(log.level)))
    log.debug("args passed in => {}".format(args))


def _get_current_runtime(gis):
    ntbk_svr = gis.notebook_server[0]
    rest = ntbk_svr._url.replace("/admin", "/rest")
    rest_info = requests.get(f"{rest}/info?f=json", timeout=5, verify=False)
    version = rest_info.json()["currentRuntimeVersion"]
    NB_ITEM_PROPERTIES_RUNTIME_STAMP_ADVANCED["notebookRuntimeVersion"] = version
    NB_ITEM_PROPERTIES_RUNTIME_STAMP_STANDARD["notebookRuntimeVersion"] = version
    return version


def _read_items_metadata_yaml():
    """Returns the items_metadata.yaml file as a dict"""
    with open(ITEMS_METADATA_YAML_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _replace_profiles():
    """Runs misc/tools/replace_profiles.py to go through each notebook in the
    repo and replace profiles with usernames/passwords
    """
    cmd = f"{sys.executable} {REPLACE_PROFILES_SCRIPT}"
    os.system(cmd)


class ItemsUploader:
    def __init__(self, gis, items_metadata_yaml):
        self._gis = gis
        self._items_metadata_yaml = items_metadata_yaml
        self.failed_uploads = []

    def upload_items(self, share_after_upload=True):
        for entry in self._items_metadata_yaml["samples"] + \
                self._items_metadata_yaml["guides"] + \
                self._items_metadata_yaml["labs"]:
            self._stage_and_upload_item(entry, share_after_upload)

    def _stage_and_upload_item(self, entry, share_after_upload=True):
        log.info(f"Uploading {entry['title']}")
        log.debug(f"    sample: {entry}")
        try:
            nb_path = entry["path"]
            self._preupload_check(entry['title'], nb_path)
            runtime_stamp = self._infer_runtime_stamp(
                entry.get("runtime", "standard"))
            categories = entry.get("categories", None)
            self._stamp_file_with_runtime(nb_path, runtime_stamp)
            item_id = self._infer_item_id(entry["url"])
            item = self.update_item(
                item_id=item_id,
                item_type=NB_PORTAL_TYPE,
                item_type_keywords=NB_PORTAL_TYPE_KEYWORDS,
                title=entry['title'],
                categories=categories,
                snippet=entry['snippet'],
                description=entry['description'],
                license_info=entry['licenseInfo'],
                tags=entry['tags'],
                nb_path=nb_path,
                runtime_stamp=runtime_stamp,
                thumbnail=entry['thumbnail'])
            if share_after_upload:
                item.sharing.sharing_level = "EVERYONE"
            item.protect()
            if categories:
                self._assign_categories_to_item(item, categories)
            self._apply_html_preview_to_item(item, nb_path)
            log.info(f"    Uploaded succeeded -> {item.homepage}")
        except Exception as e:
            self.failed_uploads.append(entry['title'])
            log.warning(f"    Couldn't upload {entry['title']}: {e}")
            log.debug(traceback.format_exc())

    def _infer_item_id(self, url):
        """Takes in a URL, infers the item ID from it"""
        return re.match("[0-9A-Fa-f]{32}", url.split("?id=")[-1]).string

    def _preupload_check(self, nb_title, nb_path):
        """Check if file exists"""
        if not os.path.exists(nb_path):
            raise Exception(f"Couldn't find {nb_path}")

    def update_item(self, item_id, item_type, item_type_keywords, title, categories,
                    snippet, description, license_info, tags, nb_path,
                    runtime_stamp, thumbnail):
        """Actually uploads the notebook item to the portal"""
        item_properties = {"title": title,
                           "snippet": snippet,
                           "description": description,
                           "licenseInfo": license_info,
                           "tags": tags,
                           "properties": runtime_stamp}
        if categories:
            item_properties["categories"] = categories
        if item_type:
            item_properties['type'] = item_type
        if item_type_keywords:
            item_properties['typeKeywords'] = item_type_keywords

        existing_item = self._gis.content.get(item_id)
        if existing_item:
            log.debug(f'item {existing_item.homepage} exists, updating...')
            item_properties["url"] = existing_item.homepage
            existing_item.update(item_properties,
                                 data=nb_path,
                                 thumbnail=thumbnail)
            resp = existing_item
        else:
            raise Exception(
                f"Could not find item {item_id} to update. Failing!")
        return resp

    def _assign_categories_to_item(self, item, categories):
        new_categories = \
            list("/Categories/{}".format(cat) for cat in categories)
        assign_arg = [{f"{item.id}": new_categories},]
        resp = self._group.categories.assign_to_items(assign_arg)
        log.debug(f"        Category assign resp: {resp}")

    def _apply_html_preview_to_item(self, item, nb_path):
        html_str = self._nb_to_html_str(nb_path)

        json_file_name = "notebook_preview.json"
        json_file_path = os.path.join(".", json_file_name)
        with open(json_file_path, 'w', encoding="utf-8") as f:
            json.dump({"html": html_str}, f)

        if item.resources.list():
            item.resources.remove()
        item.resources.add(file=json_file_path, file_name=json_file_name)
        log.debug(f"Added html preview new resource for item {item.id}")
        os.remove(json_file_path)

    def _nb_to_html_str(self, nb_path):
        nb_node = nbformat.read(nb_path, as_version=nbformat.current_nbformat)
        html_exporter = HTMLExporter()
        (body, resources) = html_exporter.from_notebook_node(nb_node)
        log.debug("Generated HTML preview for " + nb_path)
        return body

    def _infer_runtime_stamp(self, sample_entry_runtime_field):
        if re.match(".*standard.*", sample_entry_runtime_field):
            return NB_ITEM_PROPERTIES_RUNTIME_STAMP_STANDARD
        elif re.match(".*advance.*gpu.*", sample_entry_runtime_field):
            return NB_ITEM_PROPERTIES_RUNTIME_STAMP_ADVANCED_GPU
        elif re.match(".*advance.*", sample_entry_runtime_field):
            return NB_ITEM_PROPERTIES_RUNTIME_STAMP_ADVANCED
        else:
            # Default to standard
            return NB_ITEM_PROPERTIES_RUNTIME_STAMP_STANDARD

    def _stamp_file_with_runtime(self, notebook_file_path, runtime_stamp):
        nb = nbformat.read(notebook_file_path, nbformat.NO_CONVERT)
        nb['metadata']['esriNotebookRuntime'] = runtime_stamp
        nbformat.write(nb, notebook_file_path, nbformat.NO_CONVERT)


if __name__ == "__main__":
    try:
        _main()
        sys.exit(0)
    except Exception as e:
        log.exception(e)
        log.info("Program did not successfully complete (unhandled exception)")
        sys.exit(1)
