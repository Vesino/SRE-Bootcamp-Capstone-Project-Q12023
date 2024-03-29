import os
import unittest

from convert import CidrMaskConvert, IpValidate
from flask import Flask


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.environ.get("MY_APP_SECRET_KEY")
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.convert = CidrMaskConvert()
        self.validate = IpValidate()

    def test_valid_cidr_to_mask(self):
        self.assertEqual("128.0.0.0", self.convert.cidr_to_mask("1"))

    def test_valid_mask_to_cidr(self):
        self.assertEqual("1", self.convert.mask_to_cidr("128.0.0.0"))

    def test_invalid_cidr_to_mask(self):
        self.assertEqual("Invalid", self.convert.cidr_to_mask("0"))

    def test_invalid_mask_to_cidr(self):
        self.assertEqual("0", self.convert.mask_to_cidr("0.0.0.0"))

    def test_valid_ipv4(self):
        self.assertTrue(self.validate.ipv4_validation("127.0.0.1"))

    def test_invalid_ipv4(self):
        self.assertFalse(self.validate.ipv4_validation("192.168.1.2.3"))


if __name__ == "__main__":
    unittest.main()
