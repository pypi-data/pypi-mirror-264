import os
import unittest
from pathlib import Path

from steam_sdk.utils.MTF_reading_functions import read_MTF_equipment
from steam_sdk.data.DataSettings import DataSettings
from steam_sdk.parsers.ParserYAML import yaml_to_data
from steam_sdk.utils.read_settings_file import read_settings_file


class Test_MTF_reading_functions(unittest.TestCase):

    def setUp(self) -> None:
        """
            This function is executed before each test in this class
        """
        self.current_path = os.getcwd()
        os.chdir(os.path.dirname(__file__))  # move to the directory where this file is located
        print('\nCurrent folder:          {}'.format(self.current_path))
        print('\nTest is run from folder: {}'.format(os.getcwd()))

    def tearDown(self) -> None:
        """
            This function is executed after each test in this class
        """
        os.chdir(self.current_path)  # go back to initial folder

    def test_read_settings_file(self):
        # assign
        relative_path_settings = '../'

        # act
        path_settings, data_settings = read_settings_file(relative_path_settings=relative_path_settings, verbose=True)

        # assert
        print(
            'REMEMBER: for this test to pass, the local settings file must contain all keys defined in the DataSettings class, i.e.')
        print(list(dict(DataSettings()).keys()))

        self.assertEqual(path_settings, Path(os.getcwd() / Path(relative_path_settings)).resolve())
        self.assertListEqual(list(dict(DataSettings()).keys()), list(dict(data_settings).keys()))
        # Check that all values in data_settings are not None
        for key, value in dict(data_settings).items():
            self.assertIsNotNone(value, f"Value for key '{key}' is None")

    def test_read_settings_file_error(self):
        wrong_relative_path_settings = 'WRONG_PATH'
        with self.assertRaises(Exception) as context:
            path_settings, data_settings = read_settings_file(relative_path_settings=wrong_relative_path_settings,
                                                              verbose=True)
        self.assertTrue(
            f'Settings file not found at this path: {Path(os.getcwd() / Path(wrong_relative_path_settings)).resolve()}' in str(
                context.exception))
        print(f'This exception was correctly raised: {context.exception}')
