import datetime
import unittest
import pandas as pd
from arcgis.gis import GIS, Item
from arcgis.features import FeatureLayer
from arcgis.features.summarize_data import summarize_within
from .config_tests import setup_profiles, stage_data
from utils.decorators import integration_test


data = [
    {
        "FID": 1,
        "NAME": "MARKET FRESH GRILL CAFE",
        "ADDR": "221 W ORANGETHORPE AVE",
        "PHONE": "(714) 528-1977",
        "DAYS": "Mon - Sun",
        "HOURS": "7 AM - 9 PM",
        "OPTIONS": "Takeout, Delivery, Drive-Thru",
        "DISCOUNTS": "(School, Fire/Police, Senior Discounts)",
        "NOTES": "*Grubhub, Postmates, Doordash",
        "DEL_OPTS": "Grubhub, Postmates, Doordash",
        "TYPE": "American",
        "WEBSITE": "https://marketfreshgrillcafe.com",
        "Doordash": " ",
        "Grubhub": "https://www.grubhub.com/restaurant/market-fresh-grill-cafe-221-w-orangethorpe-ave-placentia/1290830",
        "Postmates": "https://postmates.com/merchant/toms-place-placentia",
        "Other": " ",
        "OUTDINE": "Open",
        "SHAPE": {
            "x": -13121824.265019992,
            "y": 4010311.1421616497,
            "spatialReference": {"wkid": 102100, "latestWkid": 3857},
        },
    },
    {
        "FID": 2,
        "NAME": "301 CAFE",
        "ADDR": "301 W SANTA FE AVE",
        "PHONE": "(714) 996-8001",
        "DAYS": "Mon - Sat",
        "HOURS": "10 AM - 9:30 PM",
        "OPTIONS": "Takeout, 3rd party Delivery",
        "DISCOUNTS": "None",
        "NOTES": " ",
        "DEL_OPTS": "Doordash",
        "TYPE": "Mexican",
        "WEBSITE": " ",
        "Doordash": "https://www.doordash.com/store/301-cafe-placentia-723324/en-US",
        "Grubhub": " ",
        "Postmates": " ",
        "Other": " ",
        "OUTDINE": "Open",
        "SHAPE": {
            "x": -13121629.643094601,
            "y": 4011297.297220264,
            "spatialReference": {"wkid": 102100, "latestWkid": 3857},
        },
    },
    {
        "FID": 3,
        "NAME": "Q TORTAS",
        "ADDR": "220 S BRADFORD AVE",
        "PHONE": "(714) 993-3270",
        "DAYS": "Tue - Friday, Sat - Sun",
        "HOURS": "11 AM - 8 PM, 9 AM - 8 PM",
        "OPTIONS": "Takeout",
        "DISCOUNTS": "None",
        "NOTES": " ",
        "DEL_OPTS": " ",
        "TYPE": "Mexican",
        "WEBSITE": " ",
        "Doordash": " ",
        "Grubhub": " ",
        "Postmates": " ",
        "Other": " ",
        "OUTDINE": "Open",
        "SHAPE": {
            "x": -13121342.054302571,
            "y": 4011316.8427645396,
            "spatialReference": {"wkid": 102100, "latestWkid": 3857},
        },
    },
    {
        "FID": 4,
        "NAME": "THE WHOLE ENCHILADA",
        "ADDR": "106 E YORBA LINDA BLVD",
        "PHONE": "(714) 961-9123",
        "DAYS": "Mon - Sun",
        "HOURS": "11 AM - 8 PM",
        "OPTIONS": "Takeout, Delivery",
        "DISCOUNTS": "None",
        "NOTES": "*Doordash",
        "DEL_OPTS": "Doordash",
        "TYPE": "Mexican",
        "WEBSITE": "https://wholeenchilada.com",
        "Doordash": "https://www.doordash.com/store/the-whole-enchilada-placentia-56007/en-US",
        "Grubhub": " ",
        "Postmates": " ",
        "Other": " ",
        "OUTDINE": "Open",
        "SHAPE": {
            "x": -13120774.654751526,
            "y": 4013636.1349284584,
            "spatialReference": {"wkid": 102100, "latestWkid": 3857},
        },
    },
]

# download shapefile and upload to respective portal if not already present
polygon_data = "https://earthworks.stanford.edu/catalog/stanford-dc841dq9031"


test_items = ["1ac6896bcafc4dccb29c70f45c442b00"]  # Polygon Zips
profiles = ["online_test", "ent_test", "kube_test"]
setup_profiles(profiles[0], profiles[1], profiles[2])
stage_data(test_items)


@integration_test
class TestSummarizeWithin(unittest.TestCase):
    def test_overwrite(self):
        """tests overwriting an Item layer using the context param"""
        for profile in profiles:
            # establish gis connection
            gis = GIS(profile=profile, verify_cert=False)
            print("User: ", gis.users.me.username)
            # create point layer in portal
            sdf = pd.DataFrame(data)
            fs = gis.content.import_data(sdf)
            # gather layers
            point_item = gis.content.get(fs.id)
            if gis._is_agol:
                polygon_item = gis.content.get("1ac6896bcafc4dccb29c70f45c442b00")
            else:
                polygon_item = gis.content.get("1ac6896bcafc4dccb29c70f45c442b00")
            assert isinstance(point_item, Item)
            assert isinstance(polygon_item, Item)
            point_layer = point_item.layers[0]
            polygon_layer = polygon_item.layers[0]
            assert isinstance(point_layer, FeatureLayer)
            assert isinstance(polygon_layer, FeatureLayer)

            # create layer that will be overwritten
            test_id = str(datetime.datetime.now().microsecond)
            output_name = "test_summarize_within_" + test_id
            print("Creating ", output_name)
            target_item = summarize_within(
                sum_within_layer=polygon_layer,
                summary_layer=point_layer,
                sum_shape=True,
                minority_majority=True,
                percent_shape=True,
                output_name=output_name,
            )
            assert isinstance(target_item, Item)
            target_layer = target_item.layers[0]
            assert isinstance(target_layer, FeatureLayer)

            # perform overwrite
            print("Overwriting target layer")
            overwrite = summarize_within(
                sum_within_layer=polygon_layer,
                summary_layer=point_layer,
                sum_shape=True,
                minority_majority=True,
                percent_shape=True,
                output_name=target_layer,
                context={"overwrite": True},
            )
            assert isinstance(overwrite, Item)
            assert target_item.id == overwrite.id
            # overwrite should not append. Only one layer should be present
            assert len(target_item.layers) == 1

            # delete items that were added for test purposes
            assert target_item.delete()
            assert fs.delete()


if __name__ == "__main__":
    unittest.main()
