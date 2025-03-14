from app.models.BaseModel import BaseModel
from app.extensions import db


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), nullable=False)

    def __init__(self, title, description, price, latitude, longitude, owner_id, user_repository, amenity_repository, amenities=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []  # Liste pour stocker les avis associés
        self.amenities = []  # Initialisation de la liste des amenities
        # Stocker le repository pour accéder au propriétaire
        self._user_repository = user_repository

        # Vérification des contraintes de validation
        if not title or len(title) > 100:
            raise ValueError(
                "Le titre doit être compris entre 1 et 100 caractères")
        if price < 0:
            raise ValueError("Le prix doit être positif")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("La latitude doit être entre -90 et 90.")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("La longitude doit être entre -180 et 180.")

        # Vérification que l'utilisateur existe dans le repository
        owner = user_repository.get(owner_id)
        if owner is None:
            raise ValueError(
                "L'utilisateur spécifié comme propriétaire n'existe pas")
        self._owner = owner  # Stocker l'objet propriétaire en mémoire

        # Initialiser la liste d'amenities si fournies
        if amenities:
            for amenity_id in amenities:
                amenity_obj = amenity_repository.get(amenity_id)
                if amenity_obj:
                    self.amenities.append(amenity_obj)
                else:
                    print(
                        f"Attention : L'amenity avec l'ID {amenity_id} n'existe pas !")

    @property
    def owner(self):
        """Getter pour l'objet owner pour maintenir la compatibilité avec le code existant"""
        if hasattr(self, '_owner'):
            return self._owner
        # Si l'attribut _owner n'existe pas, le récupérer via le repository
        if hasattr(self, '_user_repository'):
            self._owner = self._user_repository.get(self.owner_id)
            return self._owner
        return None

    def add_review(self, review):
        """Ajouter un avis à la place."""
        if not hasattr(self, 'reviews'):
            self.reviews = []
        if hasattr(review, 'to_dict'):
            self.reviews.append(review)
        else:
            raise ValueError(
                "L'objet review doit posséder une méthode to_dict()")

    def add_amenity(self, amenity):
        """Ajouter un équipement à la place sans doublon."""
        if not hasattr(self, 'amenities'):
            self.amenities = []
        if hasattr(amenity, 'id') and amenity not in self.amenities:
            self.amenities.append(amenity)
        elif not hasattr(amenity, 'id'):
            raise ValueError("L'objet amenity doit avoir un attribut 'id'")

    def to_dict(self):
        # S'assurer que les attributs existent
        if not hasattr(self, 'amenities'):
            self.amenities = []
        if not hasattr(self, 'reviews'):
            self.reviews = []

        # Crée une liste d'objets amenity avec id et name si ce sont des objets avec ces attributs
        amenities_data = []
        for amenity in self.amenities:
            if hasattr(amenity, 'id') and hasattr(amenity, 'name'):
                amenities_data.append({"id": amenity.id, "name": amenity.name})
            elif hasattr(amenity, 'id'):
                amenities_data.append({"id": amenity.id})

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "reviews": [review.to_dict() for review in self.reviews if hasattr(review, 'to_dict')],
            "amenities": amenities_data
        }

    # Cette méthode est appelée lors du chargement de l'objet depuis la base de données
    @classmethod
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        # Initialiser les attributs non-persistants
        instance.reviews = []
        instance.amenities = []
        return instance

    # Cette méthode est utilisée par SQLAlchemy lors du chargement depuis la DB
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        original_init = cls.__init__

        def new_init(self, *args, **kwargs):
            # S'assurer que les attributs non-persistants existent
            self.reviews = []
            self.amenities = []
            # Appeler l'initialisation originale si des arguments sont fournis
            if args or kwargs:
                original_init(self, *args, **kwargs)

        cls.__init__ = new_init
