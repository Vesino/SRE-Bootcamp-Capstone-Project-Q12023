import hashlib
from functools import wraps

import jwt
from flask import abort, current_app, request
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, InvalidTokenError


class Token:
    def __init__(self):
        self.HASH_ALGORITHM = "HS256"

    def generate_token(self, username, input_password, query):
        """
        Generate a JWT token for the given username and input password, using the
        salt and password obtained from the database query.

        :param self:
        :param username: the username to generate a token for
        :param input_password: the password provided by the user
        :param query: a tuple containing the salt, password, and role for the user
        :return: a JWT token if the password is correct, or False otherwise
        """
        if not query:
            return False
        useful_key = current_app.config["SECRET_KEY"]
        salt, password, role = query
        hash_pass = hashlib.sha512((input_password + salt).encode()).hexdigest()
        if hash_pass != password:
            return False

        en_jwt = jwt.encode(
            {"username": username, "role": role},
            useful_key,
            algorithm=self.HASH_ALGORITHM,
        )
        return en_jwt


class Restricted:
    @staticmethod
    def access_data(authorization):
        secret_key = current_app.config["SECRET_KEY"]
        try:
            payload = jwt.decode(
                authorization.replace("Bearer", "")[1:],
                secret_key,
                algorithms=["HS256"],
            )
        except (
            AttributeError,
            ExpiredSignatureError,
            InvalidSignatureError,
            InvalidTokenError,
        ):
            return False

        if "role" in payload:
            return True
        else:
            return False


def protected_view(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization = request.headers.get("Authorization")
        if not Restricted.access_data(authorization):
            abort(401)
        return f(*args, **kwargs)

    return decorated
