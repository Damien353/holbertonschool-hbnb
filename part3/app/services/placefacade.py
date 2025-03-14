from app.persistence.repository import InMemoryRepository
from app.models.place import Place


class PlaceFacade:
    def __init__(self, user_facade, amenity_facade):
        self.place_repo = InMemoryRepository()
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

        place_data.pop("reviews", None)

        valid_amenities = []
        for amenity_id in amenities_ids:
            amenity = self.amenity_facade.get_amenity(
                amenity_id)  # Récupérer l'objet Amenity
            if not amenity:
                return {"error": f"Amenity {amenity_id} not found"}, 400
            valid_amenities.append(amenity)

        # Créer un objet Place avec les repository requis
        new_place = Place(
            **place_data,
            # Passez le repository des utilisateurs
            user_repository=self.user_facade.user_repo,
            # Passez le repository des amenities
            amenity_repository=self.amenity_facade.amenity_repo,
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
        if not self.place_repo.get(place_id):
            return {"error": "Place not found"}, 404
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)

    def delete_place(self, place_id):
        if not self.place_repo.get(place_id):
            return {"error": "Place not found"}, 404
        self.place_repo.delete(place_id)
        return {"message": "Place successfully deleted"}, 200
