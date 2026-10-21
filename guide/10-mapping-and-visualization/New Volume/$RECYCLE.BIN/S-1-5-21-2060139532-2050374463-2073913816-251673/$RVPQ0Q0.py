import unittest
import datetime
from arcgis.features import FeatureLayer
from arcgis.gis import Item
from arcgis.gis import GIS
from arcgis.features.find_locations import find_similar_locations
from .config_tests import setup_profiles, stage_data
from utils.decorators import integration_test

test_items = [
    "00fbc412f68645958520d946806f90c0",  # Tennessee Town
    "4147267f9bcc46e79825950d800c1e6a",  # Comparison US Towns
]
profiles = ["online_test", "ent_test", "kube_test"]
setup_profiles(profiles[0], profiles[1], profiles[2])
stage_data(test_items)

# Note: until overwrite functionality is added, the second
# call of this method will just append another layer to the
# target item in enterprise. As this is the intended functionality,
# the name will remain the same and adding an extra layer will not
# throw an exception until overwriting has been implemented.


@integration_test
class TestFindSimilarLocations(unittest.TestCase):
    def test_overwrite(self):
        # establish gis connection
        for profile in profiles:
            gis = GIS(profile=profile, verify_cert=False)
            print("User: ", gis.users.me.username)
            # gather layer
            tenn_item = gis.content.get("00fbc412f68645958520d946806f90c0")
            towns_item = gis.content.get("4147267f9bcc46e79825950d800c1e6a")
            assert isinstance(tenn_item, Item)
            assert isinstance(towns_item, Item)
            tenn_lyr = tenn_item.layers[0]
            towns_lyr = towns_item.layers[0]
            assert isinstance(tenn_lyr, FeatureLayer)
            assert isinstance(towns_lyr, FeatureLayer)

            # create layer that will be overwritten
            test_id = str(datetime.datetime.now().microsecond)
            output_name = "overwrite_find_similar_locations_" + test_id
            print("Creating ", output_name)
            target_item = find_similar_locations(
                input_layer=tenn_lyr,
                search_layer=towns_lyr,
                analysis_fields=[
                    "THH17",
                    "THH35",
                    "THH02",
                    "THH05",
                    "POPDENS14",
                    "FAMGRW10_14",
                    "UNEMPRT_CY",
                ],
                number_of_results=4,
                output_name=output_name,
            )

            # verify layer matches expected types
            assert isinstance(target_item, dict)
            target_lyr = target_item["similar_result_layer"].layers[0]
            assert isinstance(target_lyr, FeatureLayer)

            # test overwriting first test
            print("Creating overwrite layer")
            overwrite = find_similar_locations(
                input_layer=tenn_lyr,
                search_layer=towns_lyr,
                analysis_fields=[
                    "THH35",
                    "THH02",
                    "THH05",
                    "POPDENS14",
                    "FAMGRW10_14",
                    "UNEMPRT_CY",
                ],
                number_of_results=5,
                output_name=target_lyr,
                context={"overwrite": True},
            )
            assert isinstance(overwrite, dict)
            assert (
                target_item["similar_result_layer"].id
                == overwrite["similar_result_layer"].id
            )
            assert overwrite["similar_result_layer"].delete()


if __name__ == "__main__":
    unittest.main()
