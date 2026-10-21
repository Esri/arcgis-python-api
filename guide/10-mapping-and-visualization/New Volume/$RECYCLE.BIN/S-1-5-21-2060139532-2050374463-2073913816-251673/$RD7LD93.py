import datetime
import unittest
from arcgis.gis import GIS, Item
from arcgis.features import FeatureLayer
from arcgis.features.find_locations import derive_new_locations
from .config_tests import setup_profiles, stage_data
from utils.decorators import integration_test

test_items = ["d3cb37b9636d47888268ca086810bd9b"]  # Cougar Habitat
profiles = ["online_test", "ent_test", "kube_test"]
setup_profiles(profiles[0], profiles[1], profiles[2])
stage_data(test_items)


@integration_test
class TestDeriveNewLocations(unittest.TestCase):
    def test_overwrite(self):
        """tests overwriting an Item layer using the context param"""
        for profile in profiles:
            # establish gis connection
            gis = GIS(profile=profile, verify_cert=False)
            print("User: ", gis.users.me.username)
            # gather layers
            if gis._is_agol:
                cougars_item = gis.content.get("d3cb37b9636d47888268ca086810bd9b")
            else:
                cougars_item = gis.content.get("d3cb37b9636d47888268ca086810bd9b")
            assert isinstance(cougars_item, Item)
            vegetation = cougars_item.layers[7]
            slope = cougars_item.layers[5]
            highways = cougars_item.layers[0]
            streams = cougars_item.layers[1]

            # create layer to be overwritten
            test_id = str(datetime.datetime.now().microsecond)
            output_name = "overwrite_test_new_locations_" + test_id
            print("Creating ", output_name)
            target_item = derive_new_locations(
                input_layers=[slope, vegetation, streams, highways],
                expressions=[
                    {
                        "operator": "",
                        "layer": 0,
                        "selectingLayer": 1,
                        "spatialRel": "intersects",
                    }
                ],
                output_name=output_name,
            )
            assert isinstance(target_item, Item)
            target_layer = target_item.layers[0]
            assert isinstance(target_layer, FeatureLayer)
            target_layer_count_1 = len(target_item.layers)
            new_input_layers = [cougars_item.layers[1], cougars_item.layers[3]]

            # perform overwrite
            print("Creating overwrite layer")
            overwrite = derive_new_locations(
                input_layers=[vegetation, streams, highways],
                expressions=[
                    {
                        "operator": "",
                        "layer": 0,
                        "selectingLayer": 1,
                        "spatialRel": "intersects",
                    }
                ],
                output_name=target_layer,
                context={"overwrite": True},
            )
            assert isinstance(overwrite, Item)
            assert target_item.id == overwrite.id
            # only one layer results from overwrite
            assert len(target_item.layers) == target_layer_count_1
            # delete content created by story
            assert target_item.delete()


if __name__ == "__main__":
    unittest.main()
