"""Test the utils.config subpackage"""
import unittest
import configparser
import pathlib

import stereoid.utils.config as st_config


class TestDefaults(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(__file__).parent.parent
        self.config = st_config.parse(self.root / "PAR" / "user_defaults.cfg")

    def test_read_main(self):
        self.assertEqual(
            self.config["main"],
            self.root / "./",  # assume we run the test runner from project root
            "did not read path properly from config file",
        )

    def test_read_data(self):
        self.assertEqual(
            self.config["data"],
            self.root / "./Data",  # assume we run the test runner from project root
            "did not read path properly from config file",
        )

    def test_read_par(self):
        self.assertEqual(
            self.config["par"],
            self.root / "./PAR",  # assume we run the test runner from project root
            "did not read path properly from config file",
        )

    def test_read_par(self):
        self.assertEqual(
            self.config["results"],
            self.root / "./Results",  # assume we run the test runner from project root
            "did not read path properly from config file",
        )


class TestDefaultDatatypes(unittest.TestCase):
    def setUp(self):
        config = configparser.ConfigParser()
        config["Test"] = {
            "main": "./",
            "data": "./data",
            "par": "./PAR",
            "results": "./data",
        }
        # Assume that the testrunner starts at the project top level
        self.path = pathlib.Path("./tests/test_param.ini")
        with open(self.path, "w") as configfile:
            config.write(configfile)
        self.root = pathlib.Path(__file__).parent.parent
        self.config = st_config.parse(self.path, "Test")

    def takeDown(self):
        try:
            self.path.unlink()
        except FileNotFoundError as err:
            print("Error: %s - %s." % (err.filename, err.strerror))

    def test_read(self):
        self.assertEqual(
            self.config["main"],
            self.root / "./",
            "did not read path properly from config file",
        )


class TestReadConfig(unittest.TestCase):
    def setUp(self):
        config = configparser.ConfigParser()
        config["Test"] = {
            "string": "hello",
            "int": "2",
            "boolean": "True",
            "float": "9.0",
            "float_scientific": "6.62607e-34",
            "list": "[9.0, 9.3, 10.5]",
            "path": "./PAR",
        }
        # Assume that the testrunner starts at the project top level
        self.path = pathlib.Path("./tests/test_param.ini")
        with open(self.path, "w") as configfile:
            config.write(configfile)
        datatypes = {
            "string": "str",
            "boolean": "bool",
            "int": "int",
            "float": "float",
            "float_scientific": "float",
            "list": "list",
            "path": "path",
        }
        self.root = pathlib.Path(__file__).parent.parent
        self.config = st_config.parse(self.path, "Test", datatypes)

    def takeDown(self):
        try:
            self.path.unlink()
        except FileNotFoundError as err:
            print("Error: %s - %s." % (err.filename, err.strerror))

    def test_read_path(self):
        self.assertEqual(
            self.config["path"],
            self.root / "./PAR",
            "did not read path properly from config file",
        )

    def test_read_string(self):
        self.assertEqual(
            self.config["string"],
            "hello",
            "did not read string properly from config file",
        )

    def test_read_bool(self):
        self.assertTrue(
            self.config["boolean"], "did not read bool properly from config file",
        )

    def test_read_float(self):
        self.assertAlmostEqual(
            self.config["float"], 9.0, "did not read float properly from file",
        )

    def test_read_float_scientific(self):
        self.assertAlmostEqual(
            self.config["float_scientific"],
            6.62607e-34,
            "did not read float properly from file",
        )

    def test_read_list(self):
        self.assertListEqual(
            self.config["list"],
            ["9.0", "9.3", "10.5"],
            "did not read float properly from file",
        )
