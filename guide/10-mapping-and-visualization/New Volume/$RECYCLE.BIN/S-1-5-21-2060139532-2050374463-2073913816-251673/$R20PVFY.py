import unittest
import datetime
from arcgis.features import FeatureLayer
from arcgis.gis import Item
from arcgis.gis import GIS
from arcgis.features.manage_data import extract_data
from .config_tests import setup_profiles, stage_data
from utils.decorators import integration_test

test_items = [
    "d3cb37b9636d47888268ca086810bd9b",  # Cougar Habitat
    "a6cb2a0688d841fd803cd82b4d8282b4",  # Boundary Polygon
]
profiles = ["online_test", "ent_test", "kube_test"]
setup_profiles(profiles[0], profiles[1], profiles[2])
stage_data(test_items)


@integration_test
class TestExtractData(unittest.TestCase):
    def test_extracting(self):
        # establish gis connection
        for profile in profiles:
            gis = GIS(profile=profile, verify_cert=False)
            print("User: ", gis.users.me.username)
            # gather layers
            cougar_item = gis.content.get("d3cb37b9636d47888268ca086810bd9b")
            boundary_item = gis.content.get("a6cb2a0688d841fd803cd82b4d8282b4")
            assert isinstance(cougar_item, Item)
            assert isinstance(boundary_item, Item)
            highway_lyr = cougar_item.layers[0]
            boundary_lyr = boundary_item.layers[0]
            assert isinstance(highway_lyr, FeatureLayer)
            assert isinstance(boundary_lyr, FeatureLayer)

            # create layer that will be overwritten
            test_id = str(datetime.datetime.now().microsecond)
            output_name = "test_extract_data_" + test_id
            print("Creating ", output_name)
            target_item = extract_data(
                input_layers=[highway_lyr],
                extent=boundary_lyr,
                clip=True,
                data_format="shapefile",
                output_name=output_name,
            )

            # verify output exists and can be deleted
            assert isinstance(target_item, Item)
            assert target_item.delete()


if __name__ == "__main__":
    unittest.main()
