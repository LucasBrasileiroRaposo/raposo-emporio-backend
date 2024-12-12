import jwt
from flask import request, jsonify, make_response
from functools import wraps
import os

SECRET_KEY = os.getenv("SECRET_KEY")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return make_response(jsonify({"message": "Token is missing! You must be logged in to do this request!"}), 401)

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            kwargs['username'] = decoded_token.get("username", None)
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({"message": "Token has expired!"}), 401)
        except jwt.InvalidTokenError:
            return make_response(jsonify({"message": "Token is invalid!"}), 401)

        return f(*args, **kwargs)
    return decorated
