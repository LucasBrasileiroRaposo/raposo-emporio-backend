from dotenv import load_dotenv
import os
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from business.user.UserController import UserController
from database import db

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

def create_app():

    load_dotenv('.env')

    app = Flask(__name__)


    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

    app.port = os.environ.get('PORT')

    swaggerui_blueprint = config_swagger()
    user_controller = UserController()

    app.register_blueprint(swaggerui_blueprint)
    app.register_blueprint(user_controller.register_routes(), url_prefix=user_controller.USER__ROUTES_PREFIX)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

def config_swagger():
    return get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Raposo Emporio"
    }
)

