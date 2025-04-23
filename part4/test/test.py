import pytest
import json
from flask_jwt_extended import create_access_token
from app import create_app
from app.extensions import db
from app.services import get_facade

# ============= FIXTURES =============


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "DEBUG": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        # Initialize test data
        initialize_test_data()
        yield app
        # Clean up
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_token(app):
    with app.app_context():
        facade = get_facade()
        admin = facade.user_facade.get_user_by_email("admin@example.com")
        if not admin:
            # Create admin if doesn't exist
            admin_data = {
                'first_name': 'Admin',
                'last_name': 'User',
                'email': 'admin@example.com',
                'password': 'adminpassword',
                'is_admin': True
            }
            admin = facade.user_facade.create_user(admin_data)

        access_token = create_access_token(
            identity=admin.id, additional_claims={"is_admin": True})
        return access_token


@pytest.fixture
def user_token(app):
    with app.app_context():
        facade = get_facade()
        user = facade.user_facade.get_user_by_email("user@example.com")
        if not user:
            # Create regular user if doesn't exist
            user_data = {
                'first_name': 'Regular',
                'last_name': 'User',
                'email': 'user@example.com',
                'password': 'userpassword',
                'is_admin': False
            }
            user = facade.user_facade.create_user(user_data)

        access_token = create_access_token(
            identity=user.id, additional_claims={"is_admin": False})
        return access_token


@pytest.fixture
def sample_place_id(app, user_token):
    with app.app_context():
        facade = get_facade()
        user = facade.user_facade.get_user_by_email("user@example.com")

        # Create a sample place
        place_data = {
            'title': 'Test Place',
            'description': 'A place for testing',
            'price': 100.0,
            'latitude': 40.712776,
            'longitude': -74.005974,
            'owner_id': user.id,
            'amenities': []
        }

        place = facade.place_facade.create_place(place_data)
        if isinstance(place, tuple):  # If it returned an error response
            return None
        return place.id


@pytest.fixture
def sample_amenity_id(app, admin_token):
    with app.app_context():
        facade = get_facade()

        # Create a sample amenity
        amenity_data = {
            'name': 'Test Amenity',
            'description': 'An amenity for testing'
        }

        amenity = facade.amenity_facade.create_amenity(amenity_data)
        return amenity.id


# Helper function to initialize test data
def initialize_test_data():
    facade = get_facade()
    # Initialize admin user
    facade.user_facade.initialize_admin()


# ============= AUTH TESTS =============

def test_login_success(client, app):
    """Test successful login"""
    with app.app_context():
        # First make sure admin exists
        facade = get_facade()
        facade.user_facade.initialize_admin()

    response = client.post('/api/v1/auth/login', json={
        'email': 'admin@example.com',
        'password': 'adminpassword'
    })

    assert response.status_code == 200
    assert 'access_token' in response.get_json()


def test_login_invalid_credentials(client, app):
    """Test login with invalid credentials"""
    response = client.post('/api/v1/auth/login', json={
        'email': 'admin@example.com',
        'password': 'wrongpassword'
    })

    assert response.status_code == 401
    assert 'error' in response.get_json()


def test_access_protected_endpoint_without_token(client):
    """Test accessing protected endpoint without token"""
    response = client.get('/api/v1/protected')
    assert response.status_code == 401


def test_access_protected_endpoint_with_token(client, user_token):
    """Test accessing protected endpoint with token"""
    headers = {'Authorization': f'Bearer {user_token}'}
    response = client.get('/api/v1/protected', headers=headers)
    assert response.status_code == 200


# ============= USER TESTS =============

def test_create_user_as_admin(client, admin_token):
    """Test creating a user as admin"""
    headers = {'Authorization': f'Bearer {admin_token}'}
    user_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    }

    response = client.post('/api/v1/users/', json=user_data, headers=headers)
    assert response.status_code == 201
    assert 'id' in response.get_json()


def test_get_user_list(client, admin_token):
    """Test getting list of users"""
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.get('/api/v1/users/', headers=headers)

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_update_own_profile(client, user_token, app):
    """Test updating own profile"""
    with app.app_context():
        facade = get_facade()
        user = facade.user_facade.get_user_by_email("user@example.com")

    headers = {'Authorization': f'Bearer {user_token}'}
    update_data = {
        'first_name': 'Updated',
        'last_name': 'User'
    }

    response = client.put(
        f'/api/v1/users/{user.id}', json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.get_json().get('first_name') == 'Updated'


def test_update_other_user_as_regular_user(client, user_token, admin_token, app):
    """Test regular user trying to update another user"""
    # Get admin user id
    with app.app_context():
        facade = get_facade()
        admin = facade.user_facade.get_user_by_email("admin@example.com")

    headers = {'Authorization': f'Bearer {user_token}'}
    update_data = {
        'first_name': 'Hacked',
        'last_name': 'Admin'
    }

    response = client.put(
        f'/api/v1/users/{admin.id}', json=update_data, headers=headers)
    assert response.status_code == 403


# ============= PLACE TESTS =============

def test_create_place(client, user_token):
    """Test creating a place"""
    headers = {'Authorization': f'Bearer {user_token}'}
    place_data = {
        'title': 'New Place',
        'description': 'A beautiful place to stay',
        'price': 150.0,
        'latitude': 48.8566,
        'longitude': 2.3522,
        'amenities': []
    }

    response = client.post('/api/v1/places/', json=place_data, headers=headers)
    assert response.status_code == 201
    assert 'id' in response.get_json()


def test_get_place_list(client):
    """Test getting list of places"""
    response = client.get('/api/v1/places/')

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_update_own_place(client, user_token, sample_place_id):
    """Test updating own place"""
    if not sample_place_id:
        pytest.skip("Failed to create sample place")

    headers = {'Authorization': f'Bearer {user_token}'}
    update_data = {
        'title': 'Updated Place',
        'price': 200.0
    }

    response = client.put(
        f'/api/v1/places/{sample_place_id}', json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.get_json().get('title') == 'Updated Place'


# ============= REVIEW TESTS =============

def test_create_review(client, admin_token, sample_place_id):
    """Test creating a review"""
    if not sample_place_id:
        pytest.skip("Failed to create sample place")

    headers = {'Authorization': f'Bearer {admin_token}'}
    review_data = {
        'text': 'Great place!',
        'rating': 5
    }

    response = client.post(
        f'/api/v1/places/{sample_place_id}/reviews', json=review_data, headers=headers)
    assert response.status_code == 201
    assert 'id' in response.get_json()


def test_get_place_reviews(client, sample_place_id):
    """Test getting reviews for a place"""
    if not sample_place_id:
        pytest.skip("Failed to create sample place")

    response = client.get(f'/api/v1/places/{sample_place_id}/reviews')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_cannot_review_own_place(client, user_token, sample_place_id):
    """Test that a user cannot review their own place"""
    if not sample_place_id:
        pytest.skip("Failed to create sample place")

    headers = {'Authorization': f'Bearer {user_token}'}
    review_data = {
        'text': 'My place is great!',
        'rating': 5
    }

    response = client.post(
        f'/api/v1/places/{sample_place_id}/reviews', json=review_data, headers=headers)
    assert response.status_code == 400
    assert 'error' in response.get_json()


# ============= AMENITY TESTS =============

def test_create_amenity_as_admin(client, admin_token):
    """Test creating an amenity as admin"""
    headers = {'Authorization': f'Bearer {admin_token}'}
    amenity_data = {
        'name': 'Swimming Pool',
        'description': 'A beautiful swimming pool'
    }

    response = client.post('/api/v1/amenities/',
                           json=amenity_data, headers=headers)
    assert response.status_code == 201
    assert 'id' in response.get_json()


def test_create_amenity_as_regular_user(client, user_token):
    """Test regular user trying to create an amenity"""
    headers = {'Authorization': f'Bearer {user_token}'}
    amenity_data = {
        'name': 'Spa',
        'description': 'A relaxing spa'
    }

    response = client.post('/api/v1/amenities/',
                           json=amenity_data, headers=headers)
    assert response.status_code == 403


def test_get_amenity_list(client):
    """Test getting list of amenities"""
    response = client.get('/api/v1/amenities/')

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_add_amenity_to_place(client, user_token, sample_place_id, sample_amenity_id):
    """Test adding an amenity to a place"""
    if not sample_place_id or not sample_amenity_id:
        pytest.skip("Failed to create sample place or amenity")

    headers = {'Authorization': f'Bearer {user_token}'}

    # First get the place
    place_response = client.get(f'/api/v1/places/{sample_place_id}')
    place_data = place_response.get_json()

    # Add the amenity to the place's amenities list
    place_data['amenities'] = [sample_amenity_id]

    # Update the place
    response = client.put(
        f'/api/v1/places/{sample_place_id}', json=place_data, headers=headers)
    assert response.status_code == 200

    # Check if amenity is in the place's amenities
    updated_place = response.get_json()
    amenity_ids = [a['id'] for a in updated_place['amenities']]
    assert sample_amenity_id in amenity_ids


# ============= INTEGRATION TESTS =============

def test_full_user_flow(client, app):
    """Test full user flow: register, login, create place, add review"""
    with app.app_context():
        facade = get_facade()
        # Clean up any existing test data
        existing_user = facade.user_facade.get_user_by_email(
            "flowtest@example.com")
        if existing_user:
            facade.user_facade.delete_user(existing_user.id)

    # 1. Create admin token
    admin_response = client.post('/api/v1/auth/login', json={
        'email': 'admin@example.com',
        'password': 'adminpassword'
    })
    admin_token = admin_response.get_json()['access_token']
    admin_headers = {'Authorization': f'Bearer {admin_token}'}

    # 2. Admin creates a new user
    user_data = {
        'first_name': 'Flow',
        'last_name': 'Test',
        'email': 'flowtest@example.com',
        'password': 'flowtestpass'
    }
    client.post('/api/v1/users/', json=user_data, headers=admin_headers)

    # 3. User logs in
    user_login_response = client.post('/api/v1/auth/login', json={
        'email': 'flowtest@example.com',
        'password': 'flowtestpass'
    })
    user_token = user_login_response.get_json()['access_token']
    user_headers = {'Authorization': f'Bearer {user_token}'}

    # 4. User creates a place
    place_data = {
        'title': 'Flow Test Place',
        'description': 'A place for flow testing',
        'price': 120.0,
        'latitude': 34.0522,
        'longitude': -118.2437,
        'amenities': []
    }
    place_response = client.post(
        '/api/v1/places/', json=place_data, headers=user_headers)
    place_id = place_response.get_json()['id']

    # 5. Admin creates an amenity
    amenity_data = {
        'name': 'Flow Test Amenity',
        'description': 'An amenity for flow testing'
    }
    amenity_response = client.post(
        '/api/v1/amenities/', json=amenity_data, headers=admin_headers)
    amenity_id = amenity_response.get_json()['id']

    # 6. User adds amenity to their place
    place_data = place_response.get_json()
    place_data['amenities'] = [amenity_id]
    update_response = client.put(
        f'/api/v1/places/{place_id}', json=place_data, headers=user_headers)

    # 7. Admin adds a review to the user's place
    review_data = {
        'text': 'Great flow test place!',
        'rating': 5
    }
    review_response = client.post(
        f'/api/v1/places/{place_id}/reviews', json=review_data, headers=admin_headers)

    # 8. Get the place with reviews and amenities
    final_response = client.get(f'/api/v1/places/{place_id}')
    final_place = final_response.get_json()

    # Verify everything is connected properly
    assert final_place['title'] == 'Flow Test Place'
    assert len(final_place['amenities']) == 1
    assert final_place['amenities'][0]['name'] == 'Flow Test Amenity'
    assert len(final_place['reviews']) == 1
    assert final_place['reviews'][0]['rating'] == 5


if __name__ == "__main__":
    pytest.main()
