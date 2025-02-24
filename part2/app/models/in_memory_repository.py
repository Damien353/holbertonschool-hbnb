class InMemoryRepository:
    def __init__(self):
        self.storage = {}  # Dictionnaire pour stocker les objets

    def add(self, entity):
        """Ajoute un objet au stockage avec son ID unique comme clé."""
        self.storage[str(entity.id)] = entity

    def get(self, entity_id):
        """Récupère un objet en fonction de son ID."""
        return self.storage.get(str(entity_id))

    def get_by_attribute(self, attribute, value):
        """Recherche un objet par un de ses attributs (ex: email, nom)."""
        return next(
            (entity for entity in self.storage.values() if getattr(entity, attribute, None) == value),
            None
        )

    def all(self):
        """Retourne tous les objets stockés."""
        return list(self.storage.values())
