from app.persistence.repository import InMemoryRepository
from app.models.review import Review


class ReviewFacade:
    def __init__(self, user_facade, place_facade):
        self.review_repo = InMemoryRepository()
        self.user_facade = user_facade
        self.place_facade = place_facade

    def create_review(self, review_data):
        user = self.user_facade.get_user(review_data['user_id'])
        place = self.place_facade.get_place(review_data['place_id'])

        if not user or not place:
            return None

        rating = review_data.get('rating')
        if not rating or rating < 1 or rating > 5:
            return None

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        if not self.review_repo.get(review_id):
            return None
        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        if not self.review_repo.get(review_id):
            return None
        self.review_repo.delete(review_id)
        return {"message": "Review successfully deleted"}, 200
