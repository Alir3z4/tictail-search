from flask.ext.testing import TestCase
from urllib import urlencode

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

        resp = self.client.get("/search?{0}".format(urlencode(params, True)))

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

        # If tags is not passed into request, still should get results
        params = {
            'tags[]': '',
            'radius': radius,
            'count': count,
            'lat': float(59.33258),
            'lng': float(18.0649)

        }

        resp = self.client.get("/search?{0}".format(urlencode(params, True)))

        self.assertIsNotNone(resp.json)
        self.assertIn('products', resp.json)

        products = resp.json['products']

        self.assertIsNotNone(products)
        self.assertIsInstance(products, list)

        # No param should result in 400
        resp = self.client.get("/search")
        self.assertEqual(resp.status_code, 400)

        # Broken params should results in 400
        params = {
            'tags[]': tags,
            'radius': radius,
            'count': count,
            'lat': '59x',
            'lng': float(18.0649)
        }
        resp = self.client.get("/search?{0}".format(urlencode(params, True)))
        self.assertEqual(resp.status_code, 400)

        # lat and lng are required params, if it's not passed
        # should result in 400
        params = {
            'tags[]': tags,
            'radius': radius,
            'count': count,
            'lat': '',
            'lng': ''
        }
        resp = self.client.get("/search?{0}".format(urlencode(params, True)))
        self.assertEqual(resp.status_code, 400)

        # Count should be passed as integer or be able to be casted
        # into integer, otherwise should result in 404
        params = {
            'tags[]': tags,
            'radius': radius,
            'count': '',
            'lat': float(59.33258),
            'lng': float(18.0649)

        }
        resp = self.client.get("/search?{0}".format(urlencode(params, True)))
        self.assertEqual(resp.status_code, 404)

        # Passing count as something that can't be casted into integer
        # should result in 404
        params = {
            'tags[]': tags,
            'radius': radius,
            'count': 'k',
            'lat': float(59.33258),
            'lng': float(18.0649)

        }
        resp = self.client.get("/search?{0}".format(urlencode(params, True)))
        self.assertEqual(resp.status_code, 404)


