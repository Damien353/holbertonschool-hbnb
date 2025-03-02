import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1/places/"
USER_URL = "http://localhost:5000/api/v1/users/"


class TestPlaceAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Créer un utilisateur avant de créer un lieu."""
        cls.test_user = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com"
        }

        # Créer un utilisateur via l'API
        user_response = requests.post(USER_URL, json=cls.test_user)
        if user_response.status_code == 201:
            cls.user_id = user_response.json().get("id")
        else:
            cls.user_id = None

        cls.test_place = {
            "title": "Test Place",
            "description": "A nice place",
            "price": 100,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": cls.user_id,
            "amenities": ["1", "2"]
        }
        cls.updated_place = {
            "title": "Updated Place",
            "description": "Updated description",
            "price": 120,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": cls.user_id,
            "amenities": ["1", "3"]
        }

        # Si l'utilisateur a été créé, on crée un lieu
        if cls.user_id:
            response = requests.post(BASE_URL, json=cls.test_place)
            if response.status_code == 201:
                cls.place_id = response.json().get("id")
            else:
                cls.place_id = None
        else:
            cls.place_id = None

    def test_1_create_duplicate_place(self):
        """Test de création d'un lieu avec des données similaires."""
        if not self.test_place.get("owner_id"):
            self.skipTest("L'utilisateur n'a pas pu être créé")
        response = requests.post(BASE_URL, json=self.test_place)
        self.assertIn(response.status_code, [
                      400, 500], "Unexpected response code")

    def test_2_get_place_by_id(self):
        """Test de récupération d'un lieu par ID."""
        if not self.place_id:
            self.skipTest("Le lieu n'a pas été créé")
        response = requests.get(f"{BASE_URL}{self.place_id}")
        self.assertEqual(response.status_code, 200)

    def test_3_get_all_places(self):
        """Test de récupération de tous les lieux."""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_4_update_place(self):
        """Test de mise à jour d'un lieu."""
        if not self.place_id:
            self.skipTest("Le lieu n'a pas été créé")
        response = requests.put(
            f"{BASE_URL}{self.place_id}", json=self.updated_place)
        self.assertEqual(response.status_code, 200)

    def test_5_get_updated_place(self):
        """Vérifie si la mise à jour a bien été effectuée."""
        if not self.place_id:
            self.skipTest("Le lieu n'a pas été créé")
        response = requests.get(f"{BASE_URL}{self.place_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], self.updated_place["title"])

    def test_6_get_nonexistent_place(self):
        """Test de récupération d'un lieu inexistant."""
        response = requests.get(f"{BASE_URL}nonexistent-id")
        self.assertEqual(response.status_code, 404)

    def test_7_update_nonexistent_place(self):
        """Test de mise à jour d'un lieu inexistant."""
        response = requests.put(
            f"{BASE_URL}nonexistent-id", json=self.updated_place)
        self.assertEqual(response.status_code, 404)

    def test_8_create_place_with_invalid_data(self):
        """Test pour créer un lieu avec des données invalides."""
        invalid_place = {
            "title": "",  # Titre vide
            "description": "Invalid place",
            "price": 100,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user_id,
            "amenities": ["1", "2"]
        }
        response = requests.post(BASE_URL, json=invalid_place)
        self.assertEqual(response.status_code, 400)  # Doit renvoyer une erreur


if __name__ == "__main__":
    unittest.main()
