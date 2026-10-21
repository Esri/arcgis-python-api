import unittest
import datetime
from arcgis.features import FeatureLayer
from arcgis.gis import Item
from arcgis.gis import GIS
from arcgis.features.summarize_data import summarize_center_and_dispersion
from .config_tests import setup_profiles, stage_data
from utils.decorators import integration_test

test_items = ["5183636f099c48789628226e5730fb13"]  # Traffic Collisions
profiles = ["online_test", "ent_test", "kube_test"]
setup_profiles(profiles[0], profiles[1], profiles[2])
stage_data(test_items)


@integration_test
class TestSummarizeCenterAndDispersion(unittest.TestCase):
    def test_overwrite(self):
        # establish gis connection
        for profile in profiles:
            gis = GIS(profile=profile, verify_cert=False)
            print("User: ", gis.users.me.username)
            # gather layer
            traffic_item = gis.content.get("5183636f099c48789628226e5730fb13")
            assert isinstance(traffic_item, Item)
            traffic_lyr = traffic_item.layers[0]
            assert isinstance(traffic_lyr, FeatureLayer)

            # create layer that will be overwritten
            test_id = str(datetime.datetime.now().microsecond)
            output_name = "overwrite_summarize_center_and_dispersion_" + test_id
            print("Creating ", output_name)
            target_item = summarize_center_and_dispersion(
                analysis_layer=traffic_lyr,
                summarize_type=["CentralFeature", "MeanCenter", "Ellipse"],
                ellipse_size="2 standard deviations",
                output_name=output_name,
            )

            # verify layer matches expected types
            assert isinstance(target_item, Item)
            target_lyr = target_item.layers[0]
            assert isinstance(target_lyr, FeatureLayer)

            # test overwriting first test
            print("Creating overwrite layer")
            overwrite = summarize_center_and_dispersion(
                analysis_layer=traffic_lyr,
                summarize_type=["CentralFeature", "MeanCenter", "Ellipse"],
                ellipse_size="3 standard deviations",
                output_name=target_lyr,
                context={"overwrite": True},
            )
            assert isinstance(overwrite, Item)
            assert target_item.id == overwrite.id
            assert overwrite.delete()


if __name__ == "__main__":
    unittest.main()
