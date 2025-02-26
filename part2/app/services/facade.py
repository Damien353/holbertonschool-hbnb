from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        """Récupère la liste de tous les utilisateurs."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Met à jour les informations d'un utilisateur."""
        user = self.user_repo.get(user_id)
        if not user:
            return None  # Si l'utilisateur n'existe pas
        for key, value in user_data.items():
            setattr(user, key, value)
        self.user_repo.update(user)
        return user

    def get_place(self, place_id):
        pass

    # Méthodes pour gérer les avis (reviews)
    def create_review(self, review_data):
        """Crée un avis après validation des données."""
        # Validation : vérifier que l'utilisateur et le lieu existent
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])
        
        if not user or not place:
            return None  # Si l'utilisateur ou le lieu n'existent pas, retournera None
        
        # Validation de la note
        rating = review_data.get('rating')
        if not rating or rating < 1 or rating > 5:
            return None  # La note doit être entre 1 et 5
        
        # Création de l'avis
        review = Review(**review_data)
        self.review_repo.add(review)
        return review
    
    def get_review(self, review_id):
        """Récupère un avis par son ID."""
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        """Récupère tous les avis."""
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        """Récupère tous les avis pour un lieu spécifique."""
        reviews = self.review_repo.get_all()
        # Filtre les avis pour ne garder que ceux liés au lieu spécifié
        return [review.to_dict() for review in reviews if review.place_id == place_id]
    
    def update_review(self, review_id, review_data):
        """Met à jour un avis existant."""
        review = self.review_repo.get(review_id)
        if not review:
            return None  # Si l'avis n'existe pas, retournera None
        
        # Mise à jour des données de l'avis
        for key, value in review_data.items():
            setattr(review, key, value)
        self.review_repo.update(review)
        return review
    
    def delete_review(self, review_id):
        """Supprime un avis."""
        review = self.review_repo.get(review_id)
        if not review:
            return None  # Si l'avis n'existe pas, retournera None
        self.review_repo.delete(review)
        return review