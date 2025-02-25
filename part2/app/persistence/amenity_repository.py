from app.persistence.repository import InMemoryRepository


class AmenityRepository(InMemoryRepository):
    def __init__(self):
        super().__init__()

    def find_by_name(self, name):
        return self.get_by_attribute("name", name)
