import datetime
import unittest
import pandas as pd
from arcgis.gis import GIS, Item
from arcgis.features import FeatureLayer
from arcgis.features.manage_data import overlay_layers
from .config_tests import setup_profiles, stage_data
from utils.decorators import integration_test

test_items = ["d3cb37b9636d47888268ca086810bd9b"]  # Cougar Habitat
profiles = ["online_test", "ent_test", "kube_test"]
setup_profiles(profiles[0], profiles[1], profiles[2])
stage_data(test_items)


@integration_test
class TestOverlayLayers(unittest.TestCase):
    def test_overwrite(self):
        """tests overwriting an Item layer using the context param"""
        for profile in profiles:
            # establish gis connection
            gis = GIS(profile=profile, verify_cert=False)
            print("User: ", gis.users.me.username)
            # gather layers
            if gis._is_agol:
                cougar_item = gis.content.get("d3cb37b9636d47888268ca086810bd9b")
                park = cougar_item.layers[4]
                watershed = cougar_item.layers[6]
            else:
                cougar_item = gis.content.get("d3cb37b9636d47888268ca086810bd9b")
                park = cougar_item.layers[4]
                watershed = cougar_item.layers[6]
            # create layer that will be overwritten
            test_id = str(datetime.datetime.now().microsecond)
            output_name = "test_overlay_layers_" + test_id
            print("Creating ", output_name)
            target_item = overlay_layers(
                input_layer=park,
                overlay_layer=watershed,
                overlay_type="Intersect",
                output_name=output_name,
            )
            assert isinstance(target_item, Item)
            target_layer = target_item.layers[0]
            assert isinstance(target_layer, FeatureLayer)
            target_layer_count_1 = len(target_item.layers)

            # perform overwrite
            print("Overwrite")
            overwrite = overlay_layers(
                input_layer=park,
                overlay_layer=watershed,
                overlay_type="Union",
                output_name=target_layer,
                context={
                    "overwrite": True,
                },
            )
            assert isinstance(overwrite, Item)
            assert target_item.id == overwrite.id
            # overwrite should not append. Only one layer should be present
            assert len(target_item.layers) == target_layer_count_1
            # delete items that were added for test purposes
            assert target_item.delete()


if __name__ == "__main__":
    unittest.main()
