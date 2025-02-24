from models.BaseModel import BaseModel
from models.user import User
from models.in_memory_repository import InMemoryRepository

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id, user_repository):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

        if not title or len(title) > 100:
            raise ValueError("Le titre doit être compris entre 1 et 100 caractères")
        if price < 0:
            raise ValueError("Le prix doit être positif")
        if not(-90.0 <= latitude <= 90.0):
            raise ValueError("La latitude doit être entre -90 et 90.")
        if not(-180.0 <= longitude <= 180.0):
            raise ValueError("La longitude doit être entre -180 et 180.")
        
        # vérification que l'utilisateur existe dans le repository
        owner = user_repository.get(owner_id)
        if owner is None:
            raise ValueError("L'utilisateur spécifié comme propriétaire existe pas")
        self.owner = owner

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)