
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description="Nom de l'amenity"),
    'description': fields.String(required=False, description="Description de l'amenity")
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, "Amenity créé avec succès")
    @api.response(400, "Données invalides")
    def post(self):
        """Créer une nouvelle commodité"""
        data = request.json
        return facade.create_amenity(data)

    @api.response(200, "Liste des commodités récupérée avec succès")
    def get(self):
        """Récupérer toutes les commodités"""
        return facade.get_all_amenities()


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, "Détails de l’amenity récupérés avec succès")
    @api.response(404, "Amenity non trouvé")
    def get(self, amenity_id):
        """Récupérer une commodité par ID"""
        return facade.get_amenity(amenity_id)

    @api.expect(amenity_model)
    @api.response(200, "Amenity mis à jour avec succès")
    @api.response(404, "Amenity non trouvé")
    @api.response(400, "Données invalides")
    def put(self, amenity_id):
        """Mettre à jour une commodité"""
        data = request.json
        return facade.update_amenity(amenity_id, data)
