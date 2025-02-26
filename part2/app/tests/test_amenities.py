import unittest
from flask import Flask
from flask_restx import Api
from app.api.v1.amenities import api as amenities_ns
from app.services import facade


class AmenityTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup for the test case. This runs once before all tests."""
        # Initialize your Flask app
        app = Flask(__name__)
        api = Api(app, version='1.0', title='HBnB API',
                  description='HBnB Application API', doc='/api/v1/')
        api.add_namespace(amenities_ns, path='/api/v1/amenities')

        cls.client = app.test_client()
        cls.app = app

    def setUp(self):
        """Setup for each test case. This runs before every test."""
        # Clear any existing amenities (for testing purposes)
        self.amenity_repo = facade.amenity_repo
        self.amenity_repo._data = {}

    def test_create_amenity(self):
        """Test creating a new amenity."""
        # Test valid creation of amenity
        payload = {'name': 'Swimming Pool'}
        response = self.client.post('/api/v1/amenities/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn('name', response.json)
        self.assertEqual(response.json['name'], 'Swimming Pool')

        # Test invalid creation (missing name)
        payload = {}
        response = self.client.post('/api/v1/amenities/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], "Missing 'name' field")

    def test_get_amenity(self):
        """Test retrieving an amenity by ID."""
        # First, create an amenity
        amenity_data = {'name': 'Hot Tub'}
        create_response = self.client.post(
            '/api/v1/amenities/', json=amenity_data)
        amenity_id = create_response.json["id"]

        # Now, get the amenity by ID
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Hot Tub')

        # Test retrieving a non-existent amenity
        response = self.client.get('/api/v1/amenities/nonexistent_id')
        self.assertEqual(response.status_code, 404)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Amenity not found')

    def test_get_all_amenities(self):
        """Test retrieving all amenities."""
        # Add amenities to the repo
        self.client.post('/api/v1/amenities/', json={'name': 'Barbecue'})
        self.client.post('/api/v1/amenities/', json={'name': 'Fitness Center'})

        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_update_amenity(self):
        """Test updating an amenity."""
        # First, create an amenity
        amenity_data = {'name': 'Sauna'}
        create_response = self.client.post(
            '/api/v1/amenities/', json=amenity_data)
        amenity_id = create_response.json["id"]

        # Now, update the amenity
        updated_data = {'name': 'Luxury Sauna'}
        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Luxury Sauna')

        # Test updating a non-existent amenity
        response = self.client.put(
            '/api/v1/amenities/nonexistent_id', json=updated_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Amenity not found')


if __name__ == '__main__':
    unittest.main()
