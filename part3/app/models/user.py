#!/usr/bin/python3
import re
from app.models.BaseModel import BaseModel
from app.extensions import db, jwt, bcrypt


class User(BaseModel):

    existing_emails = []

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = None  # Initialize password as None
        self.validate_email(email)
        self.validate_name(first_name, last_name)
        self.check_email_uniqueness(email)
        User.existing_emails.append(email)

        if password:
            self.hash_password(password)  # Hash the password if provided

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def validate_email(self, email):
        email_regex = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        if not re.match(email_regex, email):
            raise ValueError("Email invalide")

    def validate_name(self, first_name, last_name):
        if not first_name or not last_name:
            raise ValueError("Le nom et le prénom ne doivent pas être vides.")
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError(
                "Le nom ou prénom ne doit pas dépasser 50 caractères.")

    def check_email_uniqueness(self, email):
        if email in User.existing_emails:
            raise ValueError(f"L'email {email} est déjà utilisé.")

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
