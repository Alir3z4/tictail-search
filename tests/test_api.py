import json
import urllib

from flask.ext.testing import TestCase

from server.app import create_app


class TestAPI(TestCase):
    def create_app(self):
        return create_app(
            settings_overrides={
                'TESTING': True,
                'PRESERVE_CONTEXT_ON_EXCEPTION': False
            }
        )

    def test_search(self):
        tags = ['men', 'women']
        radius = 2000
        count = 20
        params = {
            'tags[]': tags,
            'radius': radius,
            'count': count,
            'lat': float(59.33258),
            'lng': float(18.0649)

        }
        params = urllib.urlencode(params, True)

        resp = self.client.get("/search?{0}".format(params))

        self.assertIsNotNone(resp.json)
        self.assertIn('products', resp.json)

        products = resp.json['products']

        self.assertIsNotNone(products)
        self.assertIsInstance(products, list)
        self.assertGreaterEqual(len(products), 1)
        self.assertLessEqual(len(products), count)

        self.assertIsNotNone(products[0])
        self.assertIsInstance(products[0], dict)

        self.assertGreater(
            products[0]['popularity'],
            products[-1]['popularity']
        )
