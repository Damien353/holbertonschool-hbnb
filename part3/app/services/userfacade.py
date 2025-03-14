from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User


class UserFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.initialize_admin()

    def initialize_admin(self):
        admin_email = "admin@example.com"
        if self.get_user_by_email(admin_email):
            return

        admin_user = User(
            first_name="Admin",
            last_name="User",
            email=admin_email,
            password="adminpassword",
            is_admin=True
        )
        self.user_repo.add(admin_user)

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        if not self.user_repo.get(user_id):
            return None
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)
