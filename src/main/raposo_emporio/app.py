from app_factory import create_app
from flask_cors import CORS


app = create_app()

if __name__ == '__main__':
    CORS(app)
    app.run(host=app.host, debug=True, port=app.port)