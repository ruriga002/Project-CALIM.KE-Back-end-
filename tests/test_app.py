import unittest

from app import app


class AppSmokeTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'Healthy')

    def test_products_endpoint(self):
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn('products', payload)
        self.assertGreaterEqual(len(payload['products']), 1)
        self.assertTrue(all(product['id'] > 0 for product in payload['products']))

    def test_collections_endpoint(self):
        response = self.client.get('/api/collections')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn('collections', payload)
        self.assertGreaterEqual(len(payload['collections']), 1)
        self.assertTrue(all(collection['id'] > 0 for collection in payload['collections']))


if __name__ == '__main__':
    unittest.main()
