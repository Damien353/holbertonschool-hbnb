from app.services.repositories.place_repository import PlaceRepository
from app.models.place import Place


class PlaceFacade:
    def __init__(self, user_facade, amenity_facade):
        self.place_repo = PlaceRepository()
        self.user_facade = user_facade
        self.amenity_facade = amenity_facade

    def create_place(self, place_data):
        """Crée un lieu et retourne l'objet du lieu créé"""
        owner_id = place_data.get('owner_id')
        amenities_ids = place_data.get('amenities', [])

        # Vérifier si l'utilisateur existe
        owner = self.user_facade.get_user(owner_id)
        if not owner:
            return {"error": "Owner not found"}, 404

        # Supprimer les reviews s'ils existent dans les données (on ne les gère pas ici)
        place_data.pop("reviews", None)

        # Créer un objet Place avec les repository requis
        new_place = Place(
            title=place_data.get('title'),
            description=place_data.get('description', ''),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner_id=owner_id,
            user_repository=self.user_facade.user_repo,
            amenity_repository=self.amenity_facade.amenity_repo,
            amenities=amenities_ids
        )

        # S'assurer que l'attribut amenities existe
        if not hasattr(new_place, 'amenities'):
            new_place.amenities = []

        # Vérifier les amenities et les ajouter
        for amenity_id in amenities_ids:
            amenity = self.amenity_facade.get_amenity(amenity_id)
            if amenity:
                new_place.add_amenity(amenity)

        # Enregistrer le lieu
        self.place_repo.add(new_place)
        return new_place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            # Assurer que l'attribut amenities existe toujours
            if not hasattr(place, 'amenities'):
                place.amenities = []

            # Assurer que l'attribut reviews existe toujours
            if not hasattr(place, 'reviews'):
                place.reviews = []

            # Charger les reviews associées à cette place
            from app.services import get_facade
            facade = get_facade()
            if hasattr(facade, 'review_facade'):
                reviews = facade.review_facade.get_reviews_by_place(place_id)
                if reviews:
                    for review in reviews:
                        if review not in place.reviews:
                            place.add_review(review)
        return place

    def get_all_places(self):
        places = self.place_repo.get_all()
        # S'assurer que chaque place a les attributs amenities et reviews
        for place in places:
            if not hasattr(place, 'amenities'):
                place.amenities = []
            if not hasattr(place, 'reviews'):
                place.reviews = []
        return places

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        # S'assurer que l'attribut amenities existe
        if not hasattr(place, 'amenities'):
            place.amenities = []

        # Mettre à jour les attributs de base
        if 'title' in place_data:
            place.title = place_data['title']
        if 'description' in place_data:
            place.description = place_data['description']
        if 'price' in place_data:
            place.price = place_data['price']
        if 'latitude' in place_data:
            place.latitude = place_data['latitude']
        if 'longitude' in place_data:
            place.longitude = place_data['longitude']

        # Gestion des amenities si présentes
        if 'amenities' in place_data:
            # Réinitialiser les amenities (nous les redéfinirons)
            place.amenities = []

            for amenity_id in place_data['amenities']:
                amenity = self.amenity_facade.get_amenity(amenity_id)
                if amenity:
                    place.add_amenity(amenity)

        # Sauvegarder les modifications
        place.save()
        return place

    def delete_place(self, place_id):
        if not self.place_repo.get(place_id):
            return {"error": "Place not found"}, 404
        self.place_repo.delete(place_id)
        return {"message": "Place successfully deleted"}, 200
