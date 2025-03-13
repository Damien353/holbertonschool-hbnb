from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services import facade
from app.models.user import User


api = Namespace('admin', description='Admin operations')


@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()

        # Vérifie si l'utilisateur est un administrateur
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        # Vérifie si l'email est unique uniquement si un email est fourni
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        # On peut maintenant mettre à jour les informations de l'utilisateur
        user_data = {}

        # Si un prénom est fourni, on met à jour le prénom
        if 'first_name' in data:
            user_data['first_name'] = data['first_name']

        # Si un nom est fourni, on met à jour le nom
        if 'last_name' in data:
            user_data['last_name'] = data['last_name']

        # Si un email est fourni et qu'il est valide, on met à jour l'email
        if email:
            user_data['email'] = email

        # Mise à jour de l'utilisateur dans la base de données
        updated_user = facade.update_user(user_id, user_data)

        if not updated_user:
            return {'error': 'Failed to update user'}, 500

        return {
            'message': 'User updated successfully',
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200
