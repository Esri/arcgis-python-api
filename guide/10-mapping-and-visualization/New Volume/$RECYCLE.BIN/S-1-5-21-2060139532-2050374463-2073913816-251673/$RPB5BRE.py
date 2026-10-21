import unittest
import datetime
from arcgis.features import FeatureLayer
from arcgis.gis import Item
from arcgis.gis import GIS
from arcgis.features.manage_data import dissolve_boundaries
from .config_tests import setup_profiles, stage_data
from utils.decorators import integration_test

test_items = ["a6cb2a0688d841fd803cd82b4d8282b4"]  # Boundary Polygon
profiles = ["online_test", "ent_test", "kube_test"]
setup_profiles(profiles[0], profiles[1], profiles[2])
stage_data(test_items)

# Note: for enterprise versions below 11, the second call of this
# method will append, not overwrite. This test will keep the same name
# and not throw an exception for target items with extra layers, as this
# was the previously intended functionality.


@integration_test
class TestDissolveBoundaries(unittest.TestCase):
    def test_overwrite(self):
        # establish gis connection
        for profile in profiles:
            gis = GIS(profile=profile, verify_cert=False)
            print("User: ", gis.users.me.username)
            # gather layer
            merge_item = gis.content.get("a6cb2a0688d841fd803cd82b4d8282b4")
            assert isinstance(merge_item, Item)
            buffer_lyr = merge_item.layers[0]
            assert isinstance(buffer_lyr, FeatureLayer)

            # create layer that will be overwritten
            test_id = str(datetime.datetime.now().microsecond)
            output_name = "overwrite_dissolve_boundaries_" + test_id
            print("Creating ", output_name)
            target_item = dissolve_boundaries(
                input_layer=buffer_lyr,
                multi_part_features=False,
                output_name=output_name,
            )

            # verify layer matches expected types
            assert isinstance(target_item, Item)
            target_lyr = target_item.layers[0]
            assert isinstance(target_lyr, FeatureLayer)

            # test overwriting first test
            print("Creating overwrite layer")
            overwrite = dissolve_boundaries(
                input_layer=buffer_lyr,
                multi_part_features=True,
                output_name=target_lyr,
                context={"overwrite": True},
            )
            assert isinstance(overwrite, Item)
            assert target_item.id == overwrite.id
            assert overwrite.delete()


if __name__ == "__main__":
    unittest.main()
