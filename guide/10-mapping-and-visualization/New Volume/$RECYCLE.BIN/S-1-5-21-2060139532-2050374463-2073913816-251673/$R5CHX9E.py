import datetime
import unittest
import pandas as pd
from arcgis.gis import GIS, Item
from arcgis.features import FeatureLayer
from arcgis.features.use_proximity import plan_routes
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
class TestPlanRoutes(unittest.TestCase):
    def test_overwrite(self):
        """tests overwriting an Item layer using the context param"""
        for profile in profiles:
            # establish gis connection
            gis = GIS(profile=profile, verify_cert=False)
            print("User: ", gis.users.me.username)
            # gather layers
            if gis._is_agol:
                hq_item = gis.content.get("c7665d3c8e6f48a79f07b79677996bed")
                office_item = gis.content.get("435fcf6cff1f4f34989e151c1f25d64a")
            else:
                hq_item = gis.content.get("c7665d3c8e6f48a79f07b79677996bed")
                office_item = gis.content.get("435fcf6cff1f4f34989e151c1f25d64a")
            assert isinstance(hq_item, Item)
            assert isinstance(office_item, Item)
            hq_lyr = hq_item.layers[0]
            office_lyr = office_item.layers[0]
            assert isinstance(hq_lyr, FeatureLayer)
            assert isinstance(office_lyr, FeatureLayer)

            # create layer that will be overwritten
            test_id = str(datetime.datetime.now().microsecond)
            output_name = "test_plan_routes_" + test_id
            print("Creating ", output_name)
            target_item = plan_routes(
                stops_layer=office_lyr,
                route_count=1,
                max_stops_per_route=6,
                route_start_time=datetime.datetime(2019, 6, 20, 6, 0),
                start_layer=hq_lyr,
                output_name=output_name,
            )
            assert isinstance(target_item, Item)
            target_layer = target_item.layers[0]
            assert isinstance(target_layer, FeatureLayer)
            target_layer_count_1 = len(target_item.layers)

            # perform overwrite
            overwrite = plan_routes(
                stops_layer=office_lyr,
                route_count=1,
                max_stops_per_route=10,
                route_start_time=datetime.datetime(2019, 6, 20, 6, 0),
                start_layer=hq_lyr,
                output_name=target_layer,
                context={"overwrite": True},
            )
            assert isinstance(overwrite, Item)
            assert target_item.id == overwrite.id
            # overwrite should not append. Only one layer should be present
            assert len(target_item.layers) == target_layer_count_1
            # delete items that were added for test purposes
            assert target_item.delete()


if __name__ == "__main__":
    unittest.main()
