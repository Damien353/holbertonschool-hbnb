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

        # Vérifier les amenities
        valid_amenities = []
        for amenity_id in amenities_ids:
            amenity = self.amenity_facade.get_amenity(amenity_id)
            if not amenity:
                return {"error": f"Amenity {amenity_id} not found"}, 400
            valid_amenities.append(amenity)

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

        # Ajouter les amenities valides
        for amenity in valid_amenities:
            new_place.add_amenity(amenity)

        # Enregistrer le lieu
        self.place_repo.add(new_place)

        return new_place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return {"error": "Place not found"}, 404

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
