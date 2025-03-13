from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from app.models.user import User

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden')
    def post(self):
        """Register a new user (Admin only)"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {'error': 'Forbidden'}, 403

        user_data = api.payload

        if not user_data['first_name'].strip() or not user_data['last_name'].strip():
            return {'error': 'First name and last name cannot be empty'}, 400
        if not user_data['password'].strip():
            return {'error': 'Password cannot be empty'}, 400

        try:
            User.validate_email(None, user_data['email'])
        except ValueError as e:
            return {'error': str(e)}, 400

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'message': 'User successfully created'}, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get the list of users"""
        users = facade.get_all_users()
        return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @jwt_required()
    @api.expect(user_model, validate=False)
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'You cannot modify email or password')
    def put(self, user_id):
        """Update user details (Self or Admin)"""
        current_user = get_jwt_identity()
        claims = get_jwt()

        if current_user != str(user_id) and not claims.get("is_admin"):
            return {'message': 'Unauthorized action'}, 403

        user_data = api.payload
        update_fields = {}

        if 'first_name' in user_data and user_data['first_name'].strip():
            update_fields['first_name'] = user_data['first_name'].strip()
        if 'last_name' in user_data and user_data['last_name'].strip():
            update_fields['last_name'] = user_data['last_name'].strip()
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        updated_user = facade.update_user(user_id, update_fields)
        return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200

    @jwt_required()
    @api.response(200, 'User successfully deleted')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user (Self or Admin)"""
        current_user = get_jwt_identity()
        claims = get_jwt()

        if current_user != str(user_id) and not claims.get("is_admin"):
            return {'message': 'Unauthorized action'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        facade.delete_user(user_id)
        return {'message': 'User successfully deleted'}, 200
