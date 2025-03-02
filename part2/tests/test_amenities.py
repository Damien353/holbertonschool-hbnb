import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1/amenities/"


class TestAmenitiesAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_amenity = {'name': 'Test Amenity'}

        # Création de l'amenity de test
        response = requests.post(BASE_URL, json=cls.test_amenity)
        if response.status_code == 201:
            cls.test_amenity_id = response.json().get('id')
        else:
            cls.test_amenity_id = None

        cls.updated_amenity = {'name': 'Updated Amenity'}

    @classmethod
    def tearDownClass(cls):
        """Supprimer l'amenity créée après les tests."""
        if cls.test_amenity_id:
            requests.delete(f"{BASE_URL}{cls.test_amenity_id}")

    def test_0_check_api_availability(self):
        """Vérifier si l'API est accessible."""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_1_create_valid_amenity(self):
        """Test de création d'une amenity valide."""
        response = requests.post(BASE_URL, json=self.test_amenity)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())
        self.assertEqual(response.json()['name'], self.test_amenity['name'])

    def test_2_create_empty_amenity(self):
        """Test de création d'une amenity avec un champ 'name' vide."""
        response = requests.post(BASE_URL, json={"name": ""})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()[
                         'message'], "Le champ 'name' est requis et ne doit pas être vide.")

    def test_3_get_amenity_by_id(self):
        """Test de récupération d'une amenity par ID."""
        if not self.test_amenity_id:
            self.skipTest("L'amenity de test n'a pas été créée")
        response = requests.get(f"{BASE_URL}{self.test_amenity_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())
        self.assertIn('name', response.json())

    def test_4_update_amenity(self):
        """Test de mise à jour d'une amenity."""
        if not self.test_amenity_id:
            self.skipTest("L'amenity de test n'a pas été créée")
        response = requests.put(
            f"{BASE_URL}{self.test_amenity_id}", json=self.updated_amenity)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['message'], 'Amenity updated successfully')

    def test_5_get_updated_amenity(self):
        """Vérifie si la mise à jour a bien été effectuée."""
        if not self.test_amenity_id:
            self.skipTest("L'amenity de test n'a pas été créée")
        response = requests.get(f"{BASE_URL}{self.test_amenity_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], self.updated_amenity["name"])

    def test_6_get_nonexistent_amenity(self):
        """Test de récupération d'une amenity inexistante."""
        response = requests.get(f"{BASE_URL}nonexistent-id")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['message'], 'Amenity not found')

    def test_7_update_nonexistent_amenity(self):
        """Test de mise à jour d'une amenity inexistante."""
        response = requests.put(
            f"{BASE_URL}nonexistent-id", json=self.updated_amenity)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['message'], 'Amenity not found')


if __name__ == "__main__":
    unittest.main()
