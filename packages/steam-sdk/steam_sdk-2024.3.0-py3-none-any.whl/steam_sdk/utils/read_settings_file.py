import os
from pathlib import Path

from steam_sdk.data.DataSettings import DataSettings
from steam_sdk.parsers.ParserYAML import yaml_to_data


def read_settings_file(relative_path_settings: str = None, verbose: bool = False):
    user_name = os.getlogin()
    if verbose:
        print('user_name:   {}'.format(user_name))
    if not relative_path_settings:
        relative_path_settings = '../'
    path_settings = Path(os.getcwd() / Path(relative_path_settings)).resolve()
    settings_file = Path.joinpath(path_settings, f"settings.{user_name}.yaml")
    if not Path.exists(settings_file):
        raise Exception(f'Settings file not found at this path: {settings_file}')
        # settings_file = Path.joinpath(Path(os.getcwd()).parent, "settings.SYSTEM.yaml")
    data_settings = yaml_to_data(settings_file, DataSettings)

    # Display defined paths
    if verbose:
        print(f'path_settings: {path_settings}')
        print(f'path to settings file: {settings_file}')

    return path_settings, data_settings
