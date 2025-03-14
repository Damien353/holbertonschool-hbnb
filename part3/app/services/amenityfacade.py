from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity


class AmenityFacade:
    def __init__(self):
        self.amenity_repo = InMemoryRepository()

    def create_amenity(self, amenity_data):
        if 'name' not in amenity_data:
            raise ValueError("Missing 'name' field")
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all() or []

    def update_amenity(self, amenity_id, amenity_data):
        if not self.amenity_repo.get(amenity_id):
            return None
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)
