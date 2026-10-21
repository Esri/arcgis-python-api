import datetime
import unittest
import pandas as pd
from arcgis.gis import GIS, Item
from arcgis.features import FeatureLayer
from arcgis.features.analysis import calculate_composite_index
from .config_tests import setup_profiles

from arcgis.gis import ProfileManager

profiles = ["online_test", "ent_test", "kube_test"]
setup_profiles(profiles[0], profiles[1], profiles[2])


class TestCalculateCompositeIndex(unittest.TestCase):
    def test_overwrite(self):
        """tests overwriting an Item layer using the context param"""
        for profile in profiles:
            # establish gis connection
            gis = GIS(profile=profile, verify_cert=False)
            print("User: ", gis.users.me.username)

            test_id = str(datetime.datetime.now().microsecond)
            output_name = "test_calc_comp_idx_" + test_id
            target_item = calculate_composite_index(
                input_layer={
                    "url": "https://servicesdev.arcgis.com/b5ADkBof6gCHCFQm/arcgis/rest/services/LB_PovertyVariables_GreaterLA_2017to2021/FeatureServer/0"
                },
                input_variables=[
                    {
                        "field": "SOfLiving_GT50PctIncHousing",
                        "reverseVariable": False,
                        "weight": 2,
                    },
                    {
                        "field": "Education_DidNotCompleteHSPct",
                        "reverseVariable": False,
                        "weight": 1,
                    },
                    {
                        "field": "EconomicInsecurity_NoHealthIns",
                        "reverseVariable": False,
                        "weight": 1,
                    },
                    {
                        "field": "Housing_MoreThan1PersonPerRoom",
                        "reverseVariable": False,
                        "weight": 1,
                    },
                    {
                        "field": "Health_PoorOrFairHealthPct",
                        "reverseVariable": False,
                        "weight": 1,
                    },
                ],
                index_method="geomeanScaled",
                output_index_reverse=True,
                output_index_min_max=[{"min": 0, "max": 100}],
                output_name=output_name,
            )
            assert isinstance(target_item, Item)
            target_layer = target_item.layers[0]
            assert isinstance(target_layer, FeatureLayer)

            # delete items that were added for test purpose
            assert target_item.delete()


if __name__ == "__main__":
    unittest.main()
