"""
Use the VersionManager - differences method to find edits made between now and a given time.
Transfer those changes from one set of feature layers to another.

Scenario:
An on-premise server contains a parcel fabric that is routinely edited. Over time, edits
are pushed to default. A scheduled task runs this script.

The script detects version differences that occurred between the current moment
and one day prior. Those changes are then inserted into a companion parcel fabric
hosted in AGOL.

https://developers.arcgis.com/python/latest/api-reference/arcgis.features.managers.html#version
https://developers.arcgis.com/rest/services-reference/enterprise/differences/
"""

import datetime
from datetime import timedelta, timezone

from arcgis.gis import GIS
from arcgis.features import FeatureLayer, FeatureLayerCollection, FeatureSet

# Timestamp for finding version differences:
from_date = datetime.datetime.now(timezone.utc)
from_timestamp = (from_date - timedelta(days=1)).timestamp() * 1000

now = datetime.datetime.now(timezone.utc)
to_timestamp = int(now.timestamp() * 1000)

# Connect to the enterprises
parent_gis = GIS(profile="dev_enterprise_profile")  # prod enterprise
target_gis = GIS(profile="dev_online_parcels")  # public online

# FeatureServer endpoints
source_item = parent_gis.content.get("01a56b31801f445c8c76624a4118094a")  # enterprise
target_item = target_gis.content.get("1bdec1c1fd61433d9da9cda23ea57be0")  # online
source_service_url = source_item.url
target_service_url = target_item.url

# Source parcel fabric feature layer collection
production_parcels = FeatureLayerCollection(source_service_url, parent_gis)

# List of layer IDs for Differences:
# Records, Connection Lines, Points, Tax Lines, Tax Polygons
# Ensure layer Ids are the same between both servers or find a way to
# tie them to each other
fabric_layers = [
    l.properties.id
    for l in production_parcels.layers
    if l.properties.id in [1, 7, 8, 14, 15]
]

# Version management server endpoint
vms = production_parcels.versions

# Get differences
with vms.get_by_name("sde", "DEFAULT", None) as version:
    differences = version.differences(
        result_type="features",
        layers=fabric_layers,
        moment=to_timestamp,
        from_moment=from_timestamp,
        future=False,
    )
    print(differences)

# Parse differences by insert, update and delete
edit_type = {}
for feature in differences["features"]:
    layer_id = feature["layerId"]
    edit_type[layer_id] = {}
    for op in ["inserts", "updates", "deletes"]:
        if op in feature:
            edit_type[layer_id][op] = feature[op]

            features_dict = {
                "features": [
                    {"attributes": feat["attributes"], "geometry": feat["geometry"]}
                    for feat in feature[op]
                ]
            }

            feature_set = FeatureSet.from_dict(features_dict)
            fl = FeatureLayer(f"{target_service_url}/{layer_id}", target_gis)
            if op == "inserts":
                result = fl.edit_features(adds=feature_set, use_global_ids=True, gdb_version=None)
                print("Inserts:", layer_id, result)
            elif op == "updates":
                result = fl.edit_features(updates=feature_set, use_global_ids=True)
                print("Updates:", layer_id, result)
            else:
                result = fl.edit_features(deletes=feature_set, use_global_ids=True)
                print(op, layer_id, result)
        else:
            edit_type[layer_id][op] = []
