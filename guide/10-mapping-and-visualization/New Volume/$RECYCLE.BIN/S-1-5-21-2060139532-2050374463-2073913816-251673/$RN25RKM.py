import unittest
from utils.decorators import integration_test, profiles
from integration.config import INTEGRATION_TEST_ITEM_TAG


@profiles.admin_all
@integration_test
class TestGroupManagerSearch(unittest.TestCase):
    """ GroupManager class, search() tests """

    @classmethod
    def setUpClass(cls):
        cls.groups = []
        for id in range(150):
            group = cls.gis.groups.create(
                title="GroupManager_test_group_" + str(id), tags=INTEGRATION_TEST_ITEM_TAG
            )
            cls.groups.append(group)

    @classmethod
    def tearDownClass(cls):
        for group in cls.groups:
            group.delete()

    def test_search_groups_150_default(self):
        """
        Number of groups exceeds the amount returned in a single call. Paging gets implemented. This test checks if
        GroupManager class works under paging using default parameters.
        """
        group_search_result = self.gis.groups.search(query="")
        self.assertGreaterEqual(
            len(group_search_result), 150, "Search did not return all groups when used with default parameters"
        )

    def test_search_groups_150_owner(self):
        """if GroupManager works under paging when using a query that returns greater than 100 results"""
        group_search_result = self.gis.groups.search(query="owner: " + self.gis._username)
        self.assertGreaterEqual(
            len(group_search_result),150,"Search did not return >= 150 groups when used with query parameters"
        )

    def test_search_groups_150_le100(self):
        """checks if GroupManager class works under paging when using a query that returns less than 100 results"""
        group_search_result = self.gis.groups.search(query="title: GroupManager_test_group_14*")
        self.assertLessEqual(
            len(group_search_result), 100, "Search did not return <=100 when used with query parameters",
        )
        self.assertEqual(
            len(group_search_result), 11, "Group search did not return exactly 11 groups",
        )

    def test_search_groups_150_max50(self):
        """checks if GroupManager class works under paging when max results is reduced to 50 from a default 2000"""
        group_search_result = self.gis.groups.search(query="owner: " + self.gis._username, max_groups=50)
        self.assertLessEqual(
            len(group_search_result), 50, "Search did not return <= 50 groups when used with max_groups=50",
        )

    def test_search_groups_150_max110(self):
        """checks if GroupManager class works under paging when max results is reduced to 110 from a default 2000"""
        group_search_result = self.gis.groups.search(query="owner: " + self.gis._username, max_groups=110)
        self.assertLessEqual(
            len(group_search_result), 110, "Search did not return <= 110 groups when used with max_groups=110",
        )


if __name__ == "__main__":
    unittest.main()
