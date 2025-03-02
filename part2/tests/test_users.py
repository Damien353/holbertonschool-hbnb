import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1/users/"


class TestUserAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Créer un utilisateur pour les tests."""
        cls.test_user = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com"
        }

        # Créer un utilisateur via l'API
        response = requests.post(BASE_URL, json=cls.test_user)
        if response.status_code == 201:
            cls.user_id = response.json().get("id")
        else:
            cls.user_id = None

    def test_1_create_user(self):
        """Test de création d'un utilisateur."""
        response = requests.post(BASE_URL, json=self.test_user)
        self.assertEqual(response.status_code, 201)

    def test_2_create_user_with_duplicate_email(self):
        """Test de création d'un utilisateur avec un email déjà enregistré."""
        response = requests.post(BASE_URL, json=self.test_user)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email already registered", response.json().get("error"))

    def test_3_get_user_by_id(self):
        """Test de récupération d'un utilisateur par ID."""
        if not self.user_id:
            self.skipTest("L'utilisateur n'a pas été créé")
        response = requests.get(f"{BASE_URL}{self.user_id}")
        self.assertEqual(response.status_code, 200)

    def test_4_get_nonexistent_user(self):
        """Test de récupération d'un utilisateur inexistant."""
        response = requests.get(f"{BASE_URL}nonexistent-id")
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.json().get("error"))

    def test_5_get_all_users(self):
        """Test de récupération de tous les utilisateurs."""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_6_update_user(self):
        """Test de mise à jour d'un utilisateur."""
        if not self.user_id:
            self.skipTest("L'utilisateur n'a pas été créé")
        updated_user_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janedoe@example.com"
        }
        response = requests.put(
            f"{BASE_URL}{self.user_id}", json=updated_user_data)
        self.assertEqual(response.status_code, 200)

    def test_7_get_updated_user(self):
        """Vérifie si la mise à jour a bien été effectuée."""
        if not self.user_id:
            self.skipTest("L'utilisateur n'a pas été créé")
        response = requests.get(f"{BASE_URL}{self.user_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["first_name"], "Jane")
        self.assertEqual(data["last_name"], "Doe")
        self.assertEqual(data["email"], "janedoe@example.com")

    def test_8_update_user_with_invalid_data(self):
        """Test de mise à jour d'un utilisateur avec des données invalides."""
        if not self.user_id:
            self.skipTest("L'utilisateur n'a pas été créé")
        invalid_user_data = {
            "first_name": "",  # Nom vide
            "last_name": "",  # Prénom vide
            "email": "invalidemail.com"  # Email invalide
        }
        response = requests.put(
            f"{BASE_URL}{self.user_id}", json=invalid_user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input data", response.json().get("error"))

    def test_9_delete_user(self):
        """Test de suppression d'un utilisateur."""
        if not self.user_id:
            self.skipTest("L'utilisateur n'a pas été créé")
        response = requests.delete(f"{BASE_URL}{self.user_id}")
        self.assertEqual(response.status_code, 200)

    def test_10_get_deleted_user(self):
        """Test de récupération d'un utilisateur supprimé."""
        if not self.user_id:
            self.skipTest("L'utilisateur n'a pas été créé")
        # Suppression de l'utilisateur
        requests.delete(f"{BASE_URL}{self.user_id}")
        response = requests.get(f"{BASE_URL}{self.user_id}")
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.json().get("error"))


if __name__ == "__main__":
    unittest.main()
