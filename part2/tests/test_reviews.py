import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1/reviews/"
USER_URL = "http://localhost:5000/api/v1/users/"
PLACE_URL = "http://localhost:5000/api/v1/places/"


class TestReviewAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Créer un utilisateur et un lieu avant de créer un avis."""
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

        # Créer un lieu via l'API
        if cls.user_id:
            place_response = requests.post(PLACE_URL, json=cls.test_place)
            if place_response.status_code == 201:
                cls.place_id = place_response.json().get("id")
            else:
                cls.place_id = None
        else:
            cls.place_id = None

        # Préparer les données pour un avis
        cls.test_review = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": cls.user_id,
            "place_id": cls.place_id
        }

        # Créer un avis via l'API
        if cls.user_id and cls.place_id:
            review_response = requests.post(BASE_URL, json=cls.test_review)
            if review_response.status_code == 201:
                cls.review_id = review_response.json().get("id")
            else:
                cls.review_id = None
        else:
            cls.review_id = None

    def test_1_create_duplicate_review(self):
        """Test de création d'un avis en double."""
        if not self.test_review.get("user_id") or not self.test_review.get("place_id"):
            self.skipTest("L'utilisateur ou le lieu n'a pas été créé")
        response = requests.post(BASE_URL, json=self.test_review)
        self.assertIn(response.status_code, [
                      400, 500], "Unexpected response code")

    def test_2_get_review_by_id(self):
        """Test de récupération d'un avis par ID."""
        if not self.review_id:
            self.skipTest("L'avis n'a pas été créé")
        response = requests.get(f"{BASE_URL}{self.review_id}")
        self.assertEqual(response.status_code, 200)

    def test_3_get_all_reviews(self):
        """Test de récupération de tous les avis."""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_4_update_review(self):
        """Test de mise à jour d'un avis."""
        if not self.review_id:
            self.skipTest("L'avis n'a pas été créé")
        updated_review = {
            "text": "Updated review text",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        response = requests.put(
            f"{BASE_URL}{self.review_id}", json=updated_review)
        self.assertEqual(response.status_code, 200)

    def test_5_get_updated_review(self):
        """Vérifie si la mise à jour a bien été effectuée."""
        if not self.review_id:
            self.skipTest("L'avis n'a pas été créé")
        response = requests.get(f"{BASE_URL}{self.review_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["text"], "Updated review text")

    def test_6_get_nonexistent_review(self):
        """Test de récupération d'un avis inexistant."""
        response = requests.get(f"{BASE_URL}nonexistent-id")
        self.assertEqual(response.status_code, 404)

    def test_7_update_nonexistent_review(self):
        """Test de mise à jour d'un avis inexistant."""
        response = requests.put(
            f"{BASE_URL}nonexistent-id", json=self.test_review)
        self.assertEqual(response.status_code, 404)

    def test_8_create_review_with_invalid_data(self):
        """Test pour créer un avis avec des données invalides."""
        invalid_review = {
            "text": "",  # Texte vide
            "rating": 6,  # Note invalide
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        response = requests.post(BASE_URL, json=invalid_review)
        self.assertEqual(response.status_code, 400)  # Doit renvoyer une erreur

    def test_9_get_reviews_for_place(self):
        """Test de récupération des avis pour un lieu spécifique."""
        if not self.place_id:
            self.skipTest("Le lieu n'a pas été créé")
        response = requests.get(f"{BASE_URL}places/{self.place_id}/reviews")
        self.assertEqual(response.status_code, 200)

    def test_10_delete_review(self):
        """Test de suppression d'un avis."""
        if not self.review_id:
            self.skipTest("L'avis n'a pas été créé")
        response = requests.delete(f"{BASE_URL}{self.review_id}")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
