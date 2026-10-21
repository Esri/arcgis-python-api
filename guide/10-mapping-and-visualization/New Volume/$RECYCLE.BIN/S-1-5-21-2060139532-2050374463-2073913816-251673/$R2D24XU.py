import os
import unittest
import pandas as pd
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from utils.decorators import integration_test



RUN = os.path.dirname(os.path.realpath(__file__))


@unittest.skipIf(RUN == False, "missing data")
@integration_test
class TestFromFeatureClass(unittest.TestCase):
    def test_from_string_fc(self):
        """tests reading a SHP/FGDB"""
        fc = os.path.join(RUN, "world30.shp")
        assert isinstance(pd.DataFrame.spatial.from_featureclass(fc), pd.DataFrame)

    def test_from_path_fc(self):
        """tests reading a SHP/FGDB"""
        from pathlib import Path

        fc = os.path.join(RUN, "world30.shp")
        assert isinstance(
            pd.DataFrame.spatial.from_featureclass(Path(fc)), pd.DataFrame
        )

    def test_failure_path_fc(self):
        """tests that ValueError is raised"""
        with self.assertRaises(ValueError):
            pd.DataFrame.spatial.from_featureclass(12345)


if __name__ == "__main__":
    unittest.main()
