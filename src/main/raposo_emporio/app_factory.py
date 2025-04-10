from dotenv import load_dotenv
import os
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from business.user.UserController import UserController
from business.batch.BatchController import BatchController
from business.product.ProductController import ProductController
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
    batch_controller = BatchController()
    product_controller = ProductController()

    print(db)
    print(os.getenv('DATABASE_URI'))

    app.register_blueprint(swaggerui_blueprint)
    app.register_blueprint(user_controller.register_routes(), url_prefix=user_controller.USER__ROUTES_PREFIX)
    app.register_blueprint(batch_controller.register_routes(), url_prefix=BatchController.BATCH__ROUTES_PREFIX)
    app.register_blueprint(product_controller.register_routes(), url_prefix=ProductController.PRODUCT__ROUTES_PREFIX)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

def config_swagger():
    return get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Raposo Emporio"
    }
)

