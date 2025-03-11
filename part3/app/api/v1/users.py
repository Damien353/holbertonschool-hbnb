from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.user import User

api = Namespace('users', description='User operations')

# Modèle utilisateur pour la documentation et la validation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Email already registered')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Vérifier que les champs ne sont pas vides
        if not user_data['first_name'].strip() or not user_data['last_name'].strip():
            return {'error': 'First name and last name cannot be empty'}, 400
        if not user_data['password'].strip():
            return {'error': 'Password cannot be empty'}, 400

        # Vérifier que l'email est valide
        try:
            User.validate_email(None, user_data['email'])
        except ValueError as e:
            return {'error': str(e)}, 400

        # Vérifier si l'email est déjà utilisé
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Créer l'utilisateur sans hasher le mot de passe ici
        new_user = facade.create_user(user_data)

        # Ne pas retourner le mot de passe dans la réponse
        return {'id': new_user.id, 'message': 'User successfully created'}, 201

    @api.response(200, 'List of users retrieved successfully')
    @api.response(404, 'No users found')
    def get(self):
        """Get the list of users"""
        users = facade.get_all_users()
        if not users:
            return {'message': 'No users found'}, 404
        return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Ne pas inclure le mot de passe dans la réponse
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model, validate=True)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    @api.response(200, 'User successfully updated')
    def put(self, user_id):
        """Update user details"""
        user_data = api.payload

        # Vérifier que les champs ne sont pas vides
        if not user_data['first_name'].strip() or not user_data['last_name'].strip():
            return {'error': 'First name and last name cannot be empty'}, 400

        # Vérifier que l'email est valide
        try:
            User.validate_email(None, user_data['email'])
        except ValueError as e:
            return {'error': str(e)}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        updated_user = facade.update_user(user_id, user_data)

        if not updated_user:
            return {'error': 'Failed to update user'}, 500

        return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200


@api.route('/email/<email>')
class UserByEmailResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, email):
        """Get user details by email"""
        user = facade.get_user_by_email(email)
        if not user:
            return {'error': 'User not found'}, 404

        # Ne pas inclure le mot de passe dans la réponse
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200
