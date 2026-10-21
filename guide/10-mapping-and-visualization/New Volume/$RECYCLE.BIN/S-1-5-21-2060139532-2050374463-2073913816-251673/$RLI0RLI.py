import sys
import json
import os, uuid
import tempfile
import logging
import unittest
from arcgis.auth.tools._util import detect_proxy
from arcgis.gis.agonb import snapshot as _agosnapshot
from arcgis.gis.nb import _snapshot as _entsnapshot
from arcgis.notebook import list_snapshots, create_snapshot
from utils.decorators import integration_test, profiles
from utils._logging import enable_verbose_logging

PROXIES = detect_proxy(True)  # Handles Fiddler when True
enable_verbose_logging()

notebook_json = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": "## Welcome to your notebook.\n",
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": "#### Run this cell to connect to your GIS and get " "started:",
        },
        {
            "cell_type": "code",
            "execution_count": 1,
            "metadata": {"trusted": True},
            "outputs": [
                {
                    "name": "stderr",
                    "output_type": "stream",
                    "text": "Clowns are everywhere! RUN!!!!!\n: "
                    "UserWarning: You are logged on as "
                    "portaladmin with an administrator role, "
                    "proceed with caution.\n"
                    "  self.users.me.username)\n",
                }
            ],
            "source": 'from arcgis.gis import GIS\ngis = GIS("home")',
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": "#### Now you are ready to start!",
        },
        {
            "cell_type": "code",
            "execution_count": 2,
            "metadata": {"trusted": True},
            "outputs": [
                {"name": "stdout", "output_type": "stream", "text": "portaladmin\n"}
            ],
            "source": "print(gis.users.me.username)",
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {"trusted": True},
            "outputs": [],
            "source": "",
        },
    ],
    "metadata": {
        "esriNotebookRuntime": {
            "notebookRuntimeName": "ArcGIS Notebook " "Python 3 " "Advanced",
            "notebookRuntimeVersion": "8.0",
        },
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.7.9",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 2,
}


@integration_test
@profiles.admin_enterprise_and_agol
class TestAGOLNotebookManager(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        assert cls._item.delete()

    @classmethod
    def setUpClass(cls):
        cls._gis = cls.gis
        d = tempfile.gettempdir()
        fp = os.path.join(d, f"test_nbs{uuid.uuid4().hex[:4]}.ipynb")
        writer = open(fp, "w")
        writer.write(json.dumps(notebook_json))
        writer.close()
        if cls._gis._is_agol:
            notebookRuntimeVersion = "8.0"
        else:
            notebookRuntimeVersion = "9.0"

        cls._item = cls._gis.content.add(
            {
                "type": "Notebook",
                "tags": "delete me",
                "title": f"item_{uuid.uuid4().hex[:6]}",
                "properties": {
                    "notebookRuntimeName": "ArcGIS Notebook Python 3 Advanced",
                    "notebookRuntimeVersion": notebookRuntimeVersion,
                },
            },
            data=fp,
        )

    def test_snapshots_agol(self):
        """tests the AGO snapshot function"""
        res = create_snapshot(self._item, name="abcd2")
        assert res
        if self.gis._is_agol:
            assert isinstance(res, _agosnapshot.SnapShot)
        else:
            assert isinstance(res, _entsnapshot.SnapShot)

    def test_list_snapshots(self):
        """tests the list_snapshots method"""
        res = create_snapshot(self._item, name="abcd2")
        assert len(self._item.snapshots) == len(list_snapshots(self._item))


if __name__ == "__main__":
    unittest.main()
