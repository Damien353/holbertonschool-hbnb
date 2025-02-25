from app.persistence.repository import InMemoryRepository


class ReviewRepository(InMemoryRepository):
    def __init__(self):
        super().__init__()

    def find_by_rating(self, rating):
        return [review for review in self.get_all() if review.rating == rating]
