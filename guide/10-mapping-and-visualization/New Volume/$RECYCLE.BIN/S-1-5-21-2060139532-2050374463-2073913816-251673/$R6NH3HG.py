import unittest
import datetime
from arcgis.features import FeatureLayer
from arcgis.gis import Item
from arcgis.gis import GIS
from arcgis.features.enrich_data import enrich_layer
from .config_tests import setup_profiles, stage_data
from utils.decorators import integration_test

test_items = ["435fcf6cff1f4f34989e151c1f25d64a"]  # Esri Offices
profiles = ["online_test", "ent_test", "kube_test"]
setup_profiles(profiles[0], profiles[1], profiles[2])
stage_data(test_items)

# Note: for enterprise versions below 11, the second call of this
# method will append, not overwrite. This test will keep the same name
# and not throw an exception for target items with extra layers, as this
# was the previously intended functionality.


@integration_test
class TestEnrichLayer(unittest.TestCase):
    def test_overwrite(self):
        # establish gis connection
        for profile in profiles:
            gis = GIS(profile=profile, verify_cert=False)
            print("User: ", gis.users.me.username)
            # gather layer
            office_item = gis.content.get("435fcf6cff1f4f34989e151c1f25d64a")
            assert isinstance(office_item, Item)
            office_lyr = office_item.layers[0]
            assert isinstance(office_lyr, FeatureLayer)

            # create layer that will be overwritten
            test_id = str(datetime.datetime.now().microsecond)
            output_name = "overwrite_enrich_layer_" + test_id
            print("Creating ", output_name)
            target_item = enrich_layer(
                input_layer=office_lyr,
                analysis_variables=["AtRisk.MP27002A_B"],
                country="US",
                buffer_type="Walking Distance",
                distance=4,
                units="Meters",
                output_name=output_name,
                return_boundaries=True,
            )

            # verify layer matches expected types
            assert isinstance(target_item, Item)
            target_lyr = target_item.layers[0]
            assert isinstance(target_lyr, FeatureLayer)

            # test overwriting first test
            print("Creating overwrite layer")
            overwrite = enrich_layer(
                input_layer=office_lyr,
                analysis_variables=["crime.CRMCYTOTC"],
                country="US",
                buffer_type="Driving Distance",
                distance=3,
                units="Miles",
                output_name=target_lyr,
                return_boundaries=True,
                context={"overwrite": True},
            )
            assert isinstance(overwrite, Item)
            assert target_item.id == overwrite.id
            assert overwrite.delete()


if __name__ == "__main__":
    unittest.main()
