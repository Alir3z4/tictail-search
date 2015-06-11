from unittest import TestCase

import scipy

from server.models import Shops
from server.search import Search


class TestSearch(TestCase):
    def test_get_locations(self):
        search = Search()
        search.set_shops(Shops().objects.all())
        locations = search.get_locations()

        self.assertIsNotNone(locations)
        self.assertIsInstance(locations, list)

    def test_get_ckdtree(self):
        search = Search()
        shops = Shops().objects.all()
        search.set_shops(shops)
        ckdtree = search.get_ckdtree()

        self.assertIsNotNone(ckdtree)
        self.assertIsInstance(ckdtree, scipy.spatial.ckdtree.cKDTree)

    def test_get_last_points(self):
        search = Search()
        shops = Shops().objects.all()
        search.set_shops(shops)
        MAX_LOCATIONS = 250

        search.query(
            latitude=59.338298666466834,
            longitude=18.11972347031265,
            max_locations=MAX_LOCATIONS
        )

        points = search.get_last_points()

        self.assertIsNotNone(points)
        self.assertIsInstance(points, list)
        self.assertEqual(len(points), MAX_LOCATIONS)

    def test_get_nearby_shops(self):
        search = Search()
        shops = Shops().objects.all()
        search.set_shops(shops)

        MAX_LOCATIONS = 250

        search.query(
            latitude=59.338298666466834,
            longitude=18.11972347031265,
            max_locations=MAX_LOCATIONS
        )
        shops = search.get_nearby_shops()

        self.assertIsNotNone(shops)
        self.assertIsInstance(shops, list)
        self.assertEqual(len(shops), MAX_LOCATIONS)
