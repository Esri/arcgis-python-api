import datetime
import unittest
import pandas as pd
from arcgis.gis import GIS, Item
from arcgis.features import FeatureLayer
from arcgis.features.find_locations import choose_best_facilities
from .config_tests import setup_profiles, stage_data
from utils.decorators import integration_test

test_items = [
    "435fcf6cff1f4f34989e151c1f25d64a",  # Esri Offices
    "c7665d3c8e6f48a79f07b79677996bed",  # Esri HQ
]
profiles = ["online_test", "ent_test", "kube_test"]
setup_profiles(profiles[0], profiles[1], profiles[2])
stage_data(test_items)


@integration_test
class TestChooseBestFacilities(unittest.TestCase):
    def test_overwrite(self):
        """tests overwriting an Item layer using the context param"""
        for profile in profiles:
            # establish gis connection
            gis = GIS(profile=profile, verify_cert=False)
            print("User: ", gis.users.me.username)
            # gather layer
            if gis._is_agol:
                office_item = gis.content.get("435fcf6cff1f4f34989e151c1f25d64a")
                hq_item = gis.content.get("c7665d3c8e6f48a79f07b79677996bed")
            else:
                office_item = gis.content.get("435fcf6cff1f4f34989e151c1f25d64a")
                hq_item = gis.content.get("c7665d3c8e6f48a79f07b79677996bed")
            assert isinstance(office_item, Item)
            office_lyr = office_item.layers[0]
            esri_hq = hq_item.layers[0]
            assert isinstance(office_lyr, FeatureLayer)

            # create layer that will be overwritten
            test_id = str(datetime.datetime.now().microsecond)
            output_name = "test_best_facilities_" + test_id
            print("Creating ", output_name)
            target_item = choose_best_facilities(
                demand_locations_layer=office_lyr,
                max_travel_range=30,
                travel_mode="Driving Time",
                required_facilities_layer=esri_hq,
                output_name=output_name,
            )
            assert isinstance(target_item, Item)
            target_layer = target_item.layers[0]
            assert isinstance(target_layer, FeatureLayer)
            target_layer_count_1 = len(target_item.layers)

            # perform overwrite
            print("Overwritting")
            overwrite = choose_best_facilities(
                demand_locations_layer=office_lyr,
                max_travel_range=30,
                travel_mode="Driving Time",
                required_facilities_layer=esri_hq,
                output_name=target_layer,
                context={"overwrite": True},
            )
            assert isinstance(overwrite, Item)
            assert target_item.id == overwrite.id
            # overwrite should not append. Only three layers should be present in this case
            assert len(target_item.layers) == target_layer_count_1
            # delete items that were added for test purposes
            assert target_item.delete()


if __name__ == "__main__":
    unittest.main()
