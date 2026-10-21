import unittest
import datetime
from arcgis.features import FeatureLayer
from arcgis.gis import Item
from arcgis.gis import GIS
from arcgis.features.analyze_patterns import find_point_clusters
from .config_tests import setup_profiles, stage_data
from utils.decorators import integration_test

test_items = ["5183636f099c48789628226e5730fb13"]  # Traffic Collisions
profiles = ["online_test", "ent_test", "kube_test"]
setup_profiles(profiles[0], profiles[1], profiles[2])
stage_data(test_items)

# Note: for enterprise versions below 11, the second call of this
# method will append, not overwrite. This test will keep the same name
# and not throw an exception for target items with extra layers, as this
# was the previously intended functionality.


@integration_test
class TestFindPointClusters(unittest.TestCase):
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
            output_name = "overwrite_find_point_clusters_" + test_id
            print("Creating ", output_name)
            target_item = find_point_clusters(
                analysis_layer=traffic_lyr,
                min_features_cluster=50,
                output_name=output_name,
            )

            # verify layer matches expected types
            assert isinstance(target_item, Item)
            target_lyr = target_item.layers[0]
            assert isinstance(target_lyr, FeatureLayer)

            # test overwriting first test
            print("Creating overwrite layer")
            overwrite = find_point_clusters(
                analysis_layer=traffic_lyr,
                min_features_cluster=200,
                output_name=target_lyr,
                context={"overwrite": True},
            )
            assert isinstance(overwrite, Item)
            assert target_item.id == overwrite.id
            assert overwrite.delete()


if __name__ == "__main__":
    unittest.main()
