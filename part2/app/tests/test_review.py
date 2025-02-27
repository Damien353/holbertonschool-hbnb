import unittest
from datetime import datetime
from models.user import User
from models.place import Place
from models.review import Review
from app import app  # Assure-toi d'importer ton application Flask
import json

class TestReviewAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup d'application avant de démarrer les tests"""
        cls.client = app.test_client()

    def test_review_creation_valid(self):
        # Créer des objets fictifs pour Place et User
        place = Place(id="place_1", name="Test Place")
        user = User(id="user_1", name="Test User")

        # Créer une Review valide
        review = Review(text="Super endroit", rating=4, place=place, user=user)

        # Vérifier que l'objet Review a bien été créé avec les bons attributs
        self.assertEqual(review.text, "Super endroit")
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.place.id, "place_1")
        self.assertEqual(review.user.id, "user_1")
        self.assertTrue(isinstance(review.created_at, datetime))
        self.assertTrue(isinstance(review.updated_at, datetime))

    def test_invalid_rating(self):
        # Créer des objets fictifs pour Place et User
        place = Place(id="place_1", name="Test Place")
        user = User(id="user_1", name="Test User")

        # Tester une review avec un rating invalide (en dehors de la plage [1, 5])
        with self.assertRaises(ValueError) as context:
            review = Review(text="Mauvais endroit", rating=6, place=place, user=user)
        
        self.assertEqual(str(context.exception), "Rating must be between 1 and 5")

    def test_create_review_api_valid(self):
        """Test de la création d'une review via l'API"""
        data = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        response = self.client.post('/api/v1/reviews/', json=data)

        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)  # Vérifie que l'ID de la review est renvoyé
        self.assertEqual(response.json['text'], data['text'])
        self.assertEqual(response.json['rating'], data['rating'])

    def test_create_review_api_invalid_data(self):
        """Tester la création d'une review avec des données invalides"""
        # Données invalides : rating en dehors de la plage [1, 5]
        data = {
            "text": "Horrible place",
            "rating": 6,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        response = self.client.post('/api/v1/reviews/', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid data')

    def test_get_all_reviews(self):
        """Test de la récupération de toutes les reviews"""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_review_by_id(self):
        """Test de la récupération d'une review par ID"""
        review_id = "2fa85f64-5717-4562-b3fc-2c963f66afa6"
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], review_id)

        # ID invalide
        invalid_id = "nonexistent_id"
        response_invalid = self.client.get(f'/api/v1/reviews/{invalid_id}')
        self.assertEqual(response_invalid.status_code, 404)
        self.assertEqual(response_invalid.json['message'], 'Review not found')

    def test_update_review(self):
        """Test de la mise à jour d'une review"""
        update_data = {
            'text': 'Amazing place!',
            'rating': 5
        }

        review_id = "2fa85f64-5717-4562-b3fc-2c963f66afa6"
        response = self.client.put(f'/api/v1/reviews/{review_id}', json=update_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Review updated successfully')

        # Tentative de mise à jour avec des données invalides
        invalid_data = {
            'text': '',
            'rating': 6
        }
        response_invalid = self.client.put(f'/api/v1/reviews/{review_id}', json=invalid_data)
        self.assertEqual(response_invalid.status_code, 400)

        # Tentative de mise à jour avec un ID non existant
        response_not_found = self.client.put(f'/api/v1/reviews/nonexistent_id', json=update_data)
        self.assertEqual(response_not_found.status_code, 404)
        self.assertEqual(response_not_found.json['message'], 'Review not found')

    def test_delete_review(self):
        """Test de la suppression d'une review"""
        review_id = "2fa85f64-5717-4562-b3fc-2c963f66afa6"
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Review deleted successfully')

        # Tentative de suppression avec un ID non existant
        response_not_found = self.client.delete(f'/api/v1/reviews/nonexistent_id')
        self.assertEqual(response_not_found.status_code, 404)
        self.assertEqual(response_not_found.json['message'], 'Review not found')

    def test_get_reviews_for_place(self):
        """Test de la récupération des reviews pour un lieu spécifique"""
        place_id = "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        response = self.client.get(f'/api/v1/places/{place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

        # Tester pour un lieu qui n'existe pas
        invalid_place_id = "nonexistent_place_id"
        response_not_found = self.client.get(f'/api/v1/places/{invalid_place_id}/reviews')
        self.assertEqual(response_not_found.status_code, 404)
        self.assertEqual(response_not_found.json['message'], 'Place not found')

if __name__ == '__main__':
    unittest.main()
