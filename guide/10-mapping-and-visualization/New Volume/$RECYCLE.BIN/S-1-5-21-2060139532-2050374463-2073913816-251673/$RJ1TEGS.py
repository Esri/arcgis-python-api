import unittest
import datetime
import pandas as pd
from arcgis.features.layer import FeatureLayer
from arcgis.gis import GIS, Item
from arcgis.geometry import Geometry
from arcgis.features.use_proximity import find_nearest
from .config_tests import setup_profiles
from utils.decorators import integration_test

profiles = ["online_test", "ent_test", "kube_test"]
setup_profiles(profiles[0], profiles[1], profiles[2])


@integration_test
class TestFindNearest(unittest.TestCase):
    def test_overwrite(self):
        """tests overwriting an Item layer using the context param"""
        for profile in profiles:
            # establish gis connection
            gis = GIS(profile=profile, verify_cert=False)
            print("User: ", gis.users.me.username)

            # create content to be used
            g1 = Geometry(
                {"x": -118.15, "y": 33.80, "spatialReference": {"wkid": 4326}}
            )
            g2 = Geometry(
                {"x": -118.14, "y": 33.81, "spatialReference": {"wkid": 4326}}
            )
            data1 = {"OBJECTID": [1], "SHAPE": [g1], "MARKERID": [1]}
            data2 = {"OBJECTID": [1], "SHAPE": [g2], "MARKERID": [1]}
            sdf1 = pd.DataFrame(data1)
            sdf1.spatial.name
            sdf2 = pd.DataFrame(data2)
            name = sdf2.spatial.name
            origin1 = gis.content.import_data(
                sdf1, title=f"dataset_{datetime.datetime.now().microsecond}"
            )
            dest1 = gis.content.import_data(
                sdf2, title=f"dataset_{datetime.datetime.now().microsecond}"
            )

            # create layer that will be overwritten
            test_id = str(datetime.datetime.now().microsecond)
            output_name = "test_find_nearest_" + test_id
            print("Creating ", output_name)
            target_item = find_nearest(
                dest1.layers[0],
                origin1.layers[0],
                measurement_type="Driving Time",
                output_name=output_name,
            )
            assert isinstance(target_item, Item)
            target_layer = target_item.layers[0]
            assert isinstance(target_layer, FeatureLayer)
            target_layer_count_1 = len(target_item.layers)

            # perform overwrite
            overwrite = find_nearest(
                dest1.layers[0],
                origin1.layers[0],
                output_name=target_layer,
                context={"overwrite": True},
            )
            assert isinstance(overwrite, Item)
            assert target_item.id == overwrite.id
            # overwrite should not append. Only one layer should be present
            assert len(target_item.layers) == target_layer_count_1
            # delete items that were added for test purposes
            assert target_item.delete()
            assert origin1.delete()
            assert dest1.delete()


if __name__ == "__main__":
    unittest.main()
