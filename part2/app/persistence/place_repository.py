from app.persistence.repository import InMemoryRepository


class PlaceRepository(InMemoryRepository):
    def __init__(self):
        super().__init__()

    def find_by_location(self, location):
        return self.get_by_attribute("location", location)
