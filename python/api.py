import os

import mysql.connector
from convert import CidrMaskConvert
from dotenv import load_dotenv
from flask import Flask, abort, jsonify, make_response, request
from methods import Token, protected_view

# Load the environment variables from the .env file
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

    user = os.getenv("MYSQL_USER")
    db_password = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST_R")
    database = os.getenv("MYSQL_DATABASE")

    cnx = mysql.connector.connect(
        user=user, password=db_password, host=host, database=database
    )
    cursor = cnx.cursor()

    login = Token()

    convert = CidrMaskConvert()

    # Just a health check
    @app.route("/")
    def url_root():
        return "OK"

    # Just a health check
    @app.route("/_health")
    def url_health():
        return "OK"

    # e.g. http://127.0.0.1:8000/login
    @app.route("/login", methods=["POST"])
    def url_login():
        data = request.json
        username = data.get("username", None)
        user_password = data.get("password", None)

        if username is None or user_password is None:
            abort(400, "Bad request")

        query_ = "SELECT salt, password, role from users where username = %s"
        cursor.execute(query_, (username,))
        query = cursor.fetchone()

        token = login.generate_token(
            username=username, input_password=user_password, query=query
        )

        if token is not False:
            r = {"data": token}
            return make_response(r, 200)
        else:
            abort(401, "Invalid username or password")

    # e.g. http://127.0.0.1:8000/cidr-to-mask?value=8
    @app.route("/cidr-to-mask")
    @protected_view
    def url_cidr_to_mask():
        try:
            val = int(request.args.get("value"))
        except TypeError:
            abort(400, "Missing or invalid 'value' parameter")

        r = {
            "function": "cidrToMask",
            "input": val,
            "output": convert.cidr_to_mask(val),
        }
        return jsonify(r)

    # # e.g. http://127.0.0.1:8000/mask-to-cidr?value=255.0.0.0
    @app.route("/mask-to-cidr")
    @protected_view
    def url_mask_to_cidr():
        val = request.args.get("value")
        r = {
            "function": "maskToCidr",
            "input": val,
            "output": convert.mask_to_cidr(val),
        }
        return jsonify(r)

    return app
