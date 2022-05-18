
import unittest
import shopify


class AppTests(unittest.TestCase):
    """Testing Flask server"""
    
    def setUp(self):
        self.client = shopify.app.test_client()
        shopify.app.config["TESTING"] = True

    def test_status_code(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)

    def test_return_value(self):
        result = self.client.get('/view')
        self.assertIn(b"Status", result.data)

    def test_verify_attributes(self):
        assert shopify.verify_attributes("h", "l", "j", {"h": "value", "l": "v2", "j": "value3"}) is True
        assert shopify.verify_attributes("h", "l", "j", {"h": "value", "s": "v2", "j": "value3"}) is False
        assert shopify.verify_attributes("h", "l", "j", {"h": "v", "l": "v2", "j": "v3", "o": "v4"}) is True

    def test_attribute_values(self):
        assert shopify.attribute_values(["two", "three", "four"]) is True
        assert shopify.attribute_values(["1", "2", "3"]) is False
        assert shopify.attribute_values(["hello", "l", "job"]) is False


if __name__ =="__main__":
    unittest.main()