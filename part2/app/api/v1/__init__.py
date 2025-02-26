from flask_restx import Api
from app.api.v1.reviews import api as reviews_api  # Importation de ton namespace de reviews

def create_app():
    app = Flask(__name__)
    api = Api(app)

    # Enregistre le namespace des reviews à l'API
    api.add_namespace(reviews_api, path='/api/v1/reviews')

    return app
