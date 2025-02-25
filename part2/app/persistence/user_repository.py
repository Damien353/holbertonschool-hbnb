from app.persistence.repository import InMemoryRepository


class UserRepository(InMemoryRepository):
    def __init__(self):
        super().__init__()

    def find_by_email(self, email):
        return self.get_by_attribute("email", email)
