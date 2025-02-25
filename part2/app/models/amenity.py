#!/usr/bin/python3
from models.BaseModel import BaseModel


class Amenity(BaseModel):
    def __init__(self, name: str, description: str = ""):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError(
                "Le nom de l'amenity ne doit pas être vide et doit comporter au maximum 50 caractères.")
        self.name = name
        self.description = description
