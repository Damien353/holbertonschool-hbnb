import unittest
from models.place import Place
from models.user import User
from persistence.repository import InMemoryRepository
import time
from models.review import Review

@classmethod
def setUpClass(cls):
     """Setup d'application avant de démarrer les tests"""
cls.client = app.test_client()

def test_review_creation_valid(self):
        # Créer des objets fictifs pour Place et User
        place = Place(id="place_1", name="Test Place")
        user = User(id="user_1", name="Test User")

class TestReview(unittest.TestCase):
    def setUp(self):
        """Initialisation avant chaque test"""
        self.user_repository = InMemoryRepository()
        self.user = User(first_name="Alice", last_name="Doe",
                         email="alice@example.com")
        # Ajout de l'utilisateur dans le repository
        self.user_repository.add(self.user)

        self.place = Place(
            title="Beautiful House",
            description="A very nice place.",
            price=120,
            latitude=48.8566,
            longitude=2.3522,
            owner_id=self.user.id,
            user_repository=self.user_repository
        )

        self.review = Review(text="Amazing experience!",
                             rating=5, place=self.place, user=self.user)

    def test_review_creation(self):
        """Test que la review est bien créée avec les bonnes valeurs"""
        self.assertEqual(self.review.text, "Amazing experience!")
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.place, self.place)
        self.assertEqual(self.review.user, self.user)

    def test_invalid_rating(self):
        """Test que la validation de la note fonctionne correctement"""
        with self.assertRaises(ValueError):
            Review(text="Too high rating", rating=6,
                   place=self.place, user=self.user)
        with self.assertRaises(ValueError):
            Review(text="Too low rating", rating=0,
                   place=self.place, user=self.user)

        # Tester une review avec un rating invalide (en dehors de la plage [1, 5])
        with self.assertRaises(ValueError) as context:
            review = Review(text="Mauvais endroit", rating=6, place=self.place, user=self.user)
        
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

    def test_empty_text(self):
        """Test que le texte de la review ne peut pas être vide"""
        with self.assertRaises(ValueError):
            Review(text="", rating=3, place=self.place, user=self.user)
        with self.assertRaises(ValueError):
            Review(text="   ", rating=3, place=self.place, user=self.user)

    def test_invalid_place_or_user(self):
        """Test qu'une review sans place ou user valide lève une erreur"""
        with self.assertRaises(ValueError):
            Review(text="No place", rating=3, place=None, user=self.user)
        with self.assertRaises(ValueError):
            Review(text="No user", rating=3, place=self.place, user=None)
        with self.assertRaises(ValueError):
            Review(text="Invalid place", rating=3,
                   place="NotAPlace", user=self.user)
        with self.assertRaises(ValueError):
            Review(text="Invalid user", rating=3,
                   place=self.place, user="NotAUser")

    def test_update_review(self):
        """Test la mise à jour d'une review"""
        time.sleep(1)  # Pause pour observer le changement de timestamp
        old_updated_at = self.review.updated_at
        self.review.update_review("Updated review", 4)

        self.assertEqual(self.review.text, "Updated review")
        self.assertEqual(self.review.rating, 4)
        # Vérifie que updated_at a bien changé
        self.assertGreater(self.review.updated_at, old_updated_at)

if __name__ == '__main__':
    unittest.main()
