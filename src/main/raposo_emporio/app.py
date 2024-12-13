from app_factory import create_app
from flask_cors import CORS


app = create_app()

if __name__ == '__main__':
    print(app.url_map)
    CORS(app)
    app.run(debug=True, port=app.port)