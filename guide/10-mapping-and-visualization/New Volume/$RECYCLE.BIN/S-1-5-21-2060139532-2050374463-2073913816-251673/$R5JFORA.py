import unittest
import datetime
from arcgis.gis import GIS, Item
from arcgis.features import FeatureLayer
from arcgis.features.use_proximity import create_drive_time_areas
from .config_tests import setup_profiles, stage_data
from utils.decorators import integration_test

test_items = ["435fcf6cff1f4f34989e151c1f25d64a"]  # Esri Offices
profiles = ["online_test", "ent_test", "kube_test"]
setup_profiles(profiles[0], profiles[1], profiles[2])
stage_data(test_items)


@integration_test
class TestCreateDriveTimeAreas(unittest.TestCase):
    def test_overwrite(self):
        """tests overwriting an Item layer using the context param"""
        for profile in profiles:
            # establish gis connection
            gis = GIS(profile=profile, verify_cert=False)
            print("User: ", gis.users.me.username)
            # gather layer
            if gis._is_agol:
                office_item = gis.content.get("435fcf6cff1f4f34989e151c1f25d64a")
            else:
                office_item = gis.content.get("435fcf6cff1f4f34989e151c1f25d64a")
            assert isinstance(office_item, Item)
            office_lyr = office_item.layers[0]
            assert isinstance(office_lyr, FeatureLayer)

            # create layer that will be overwritten
            test_id = str(datetime.datetime.now().microsecond)
            output_name = "overwrite_test_drive_times_" + test_id
            print("Creating ", output_name)
            target_item = create_drive_time_areas(
                input_layer=office_lyr, output_name=output_name
            )
            assert isinstance(target_item, Item)
            target_layer = target_item.layers[0]
            assert isinstance(target_layer, FeatureLayer)
            target_layer_count_1 = len(target_item.layers)

            # perform overwrite
            print("Creating overwrite layer")
            overwrite = create_drive_time_areas(
                input_layer=office_lyr,
                break_values=[2],
                break_units="Hours",
                output_name=target_layer,
                context={"overwrite": True},
            )
            assert isinstance(overwrite, Item)
            assert target_item.id == overwrite.id
            # overwrite only produces one layer
            assert len(target_item.layers) == target_layer_count_1
            # delete content created by test
            assert target_item.delete()


if __name__ == "__main__":
    unittest.main()
