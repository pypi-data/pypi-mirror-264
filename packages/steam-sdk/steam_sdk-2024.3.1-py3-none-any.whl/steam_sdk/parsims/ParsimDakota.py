import os
from pathlib import Path

from steam_sdk.data.DataModelParsimDakota import DataModelParsimDakota
from steam_sdk.data.DataAnalysis import DataAnalysis
from steam_sdk.data.DataSettings import DataSettings
from steam_sdk.drivers.DriverDakota import DriverDakota
from steam_sdk.parsers.ParserDakota import ParserDakota
from steam_sdk.parsers.ParserYAML import yaml_to_data, model_data_to_yaml

class ParsimDakota:
    """
    Main class for running parametric simulations with Dakota
    """

    def __init__(self, input_DAKOTA_yaml: str = None, verbose: bool = True):
        """
        This is paramat
        If verbose is set to True, additional information will be displayed
        """
        # Read dakota yaml and analysis yaml
        data_model_dakota: DataModelParsimDakota = yaml_to_data(input_DAKOTA_yaml, DataModelParsimDakota)
        analysis_file_path = os.path.join(os.path.dirname(input_DAKOTA_yaml), f'{data_model_dakota.analysis_yaml_file_name}.yaml')
        data_model_analysis: DataAnalysis = yaml_to_data(analysis_file_path, DataAnalysis)

        # deal with settings cases for either from analysis or from setting file
        settings_file = f"settings.{os.getlogin()}.yaml"
        if data_model_analysis.GeneralParameters.flag_permanent_settings: # use settings from analysis file and
            settings: DataSettings = DataSettings(**data_model_analysis.PermanentSettings.__dict__)
        else:
            full_path_file_settings = os.path.join(Path(os.path.dirname(input_DAKOTA_yaml), Path(data_model_analysis.GeneralParameters.relative_path_settings)).resolve(), settings_file)  # use settings file from the tests folder of the SDK
            if not os.path.isfile(full_path_file_settings):
                raise Exception(f'Local setting file {full_path_file_settings} not found. This file must be provided when flag_permanent_settings is set to False.')
            settings: DataSettings = yaml_to_data(full_path_file_settings, DataSettings)

        # write settings to local_Dakota_folder
        #model_data_to_yaml(settings, os.path.join(settings.local_Dakota_folder, data_model_dakota.parsim_name, settings_file)) # write a dedicated settings file into local_Dakota_folder folder for use by Dakota. This is ugly, but not easy way around it.

        # write dakota input file (.in) from yaml Dakota parametric study definition
        ParserDakota().assemble_in_file(data_model_dakota=data_model_dakota, settings=settings)

        # run analysis with pre iterable steps and iterables steps via dakota and its input file
        DriverDakota(analysis_yaml_path=analysis_file_path, data_model_dakota=data_model_dakota, settings=settings)


