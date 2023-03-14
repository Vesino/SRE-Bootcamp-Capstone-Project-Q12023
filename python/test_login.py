import hashlib
import os
import unittest

from dotenv import load_dotenv
from flask import Flask, current_app
from methods import Restricted, Token


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")
        self.app.config["SALT"] = os.environ.get("SALT")
        self.app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.convert = Token()
        self.validate = Restricted()
        self.convert = Token()
        self.validate = Restricted()

    def test_generate_token(self):
        salt = current_app.config["SALT"]
        password = current_app.config["MYSQL_PASSWORD"]
        query = (salt, hashlib.sha512((password + salt).encode()).hexdigest(), "admin")
        self.assertEqual(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIn0.XhVMUrOzNwvDfTk1LzB8Es_cBbESVoyZYFuX_dxD2IY",  # noqa: E501
            self.convert.generate_token("admin", password, query),
        )

    def test_access_data(self):
        self.assertEqual(
            True,
            self.validate.access_data(
                "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIn0.XhVMUrOzNwvDfTk1LzB8Es_cBbESVoyZYFuX_dxD2IY"  # noqa: E501
            ),
        )


if __name__ == "__main__":
    unittest.main()
