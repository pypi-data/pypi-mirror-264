import csv
import importlib
import importlib.util
import os.path
import pathlib
import pickle
import re
import sys
import warnings
from copy import deepcopy
from typing import Union, List

import numpy as np

from steam_sdk.analyses.AnalysisEvent import find_IPQ_circuit_type_from_IPQ_parameters_table, \
    get_circuit_name_from_eventfile, get_circuit_family_from_circuit_name, create_two_csvs_from_odd_and_even_rows, \
    get_number_of_apertures_from_circuit_family_name, get_number_of_quenching_magnets_from_layoutdetails, \
    get_magnet_types_list, get_number_of_magnets, get_magnet_name, get_circuit_type_from_circuit_name, \
    determine_config_path_and_configuration, write_config_file_for_viewer, \
    generate_unique_event_identifier_from_eventfile
from steam_sdk.builders.BuilderCosim import BuilderCosim
from steam_sdk.builders.BuilderModel import BuilderModel
from steam_sdk.cosims.CoSimPyCoSim import CosimPyCoSim
from steam_sdk.data.DataAnalysis import DataAnalysis, ModifyModel, ModifyModelMultipleVariables, ParametricSweep, \
    LoadCircuitParameters, WriteStimulusFile, SetUpFolder, MakeModel, ParsimEvent, DefaultParsimEventKeys, RunSimulation
from steam_sdk.data.DataSettings import DataSettings
from steam_sdk.drivers.DriverFiQuS import DriverFiQuS
from steam_sdk.drivers.DriverLEDET import DriverLEDET
from steam_sdk.drivers.DriverPSPICE import DriverPSPICE
from steam_sdk.drivers.DriverPyBBQ import DriverPyBBQ
from steam_sdk.drivers.DriverPySIGMA import DriverPySIGMA
from steam_sdk.drivers.DriverXYCE import DriverXYCE
from steam_sdk.parsers.ParserPSPICE import writeStimuliFromInterpolation
from steam_sdk.parsers.ParserXYCE import *
from steam_sdk.parsers.ParserYAML import yaml_to_data
from steam_sdk.parsims.ParsimConductor import ParsimConductor
from steam_sdk.parsims.ParsimEventCircuit import ParsimEventCircuit
from steam_sdk.parsims.ParsimEventMagnet import ParsimEventMagnet
from steam_sdk.plotters.PlotterMap2d import export_B_field_txt_to_map2d_SIGMA
from steam_sdk.plotters.PlotterMap2d import generate_report_from_map2d
from steam_sdk.postprocs.PostprocsMetrics import PostprocsMetrics
from steam_sdk.utils import parse_str_to_list
from steam_sdk.utils.attribute_model import set_attribute_model, get_attribute_model
from steam_sdk.utils.make_folder_if_not_existing import make_folder_if_not_existing
from steam_sdk.utils.parse_str_to_list import parse_str_to_list
from steam_sdk.utils.read_settings_file import read_settings_file
from steam_sdk.utils.rgetattr import rgetattr
from steam_sdk.utils.rhasattr import rhasattr
from steam_sdk.utils.sgetattr import rsetattr
from steam_sdk.viewers.Viewer import Viewer


class AnalysisSTEAM:
    """
        Class to run analysis based on STEAM_SDK
    """

    def __init__(self,
                 file_name_analysis: str = None,
                 file_path_list_models: str = '',
                 verbose: bool = False):
        """
        Analysis based on STEAM_SDK
        :param file_name_analysis: full path to analysis.yaml input file  # object containing the information read from the analysis input file
        :param verbose: if true, more information is printed to the console
        """

        # Initialize
        self.settings = DataSettings()  # object containing the settings acquired during initialization
        self.library_path = None
        if file_path_list_models:
            with open(file_path_list_models, 'rb') as input_dict:
                self.list_models = pickle.load(input_dict)
        else:
            self.list_models = {}  # this dictionary will be populated with BuilderModel objects and their names

        self.list_sims = []  # this list will be populated with integers indicating simulations to run
        self.list_viewers = {}  # this dictionary will be populated with Viewer objects and their names
        self.list_metrics = {}  # this dictionary will be populated with calculated metrics
        self.verbose = verbose
        self.summary = None  # float representing the overall outcome of a simulation for parsims
        self.postprocess_output = None
        self.file_name_analysis = file_name_analysis
        self.path_analysis_file = Path(self.file_name_analysis).parent  # Find folder where the input file is located, which will be used as the "anchor" for all input files
        if isinstance(file_name_analysis, str) or isinstance(file_name_analysis, pathlib.PurePath):
            self.data_analysis: DataAnalysis = yaml_to_data(file_name_analysis, DataAnalysis)  # Load yaml keys into DataAnalysis dataclass
            # Read analysis settings
            self._load_settings(self.data_analysis.GeneralParameters.relative_path_settings)
            # Read working folders and set them up
            self._set_library_folder()
        elif file_name_analysis is None:
            self.data_analysis = DataAnalysis()
            if verbose: print('Empty AnalysisSTEAM() object generated.')


    def setAttribute(self, dataclassSTEAM, attribute: str, value):
        try:
            setattr(dataclassSTEAM, attribute, value)
        except:
            setattr(getattr(self, dataclassSTEAM), attribute, value)

    def getAttribute(self, dataclassSTEAM, attribute):
        try:
            return getattr(dataclassSTEAM, attribute)
        except:
            return getattr(getattr(self, dataclassSTEAM), attribute)

    def _load_settings(self, relative_path_settings: str):
        """
            ** Read analysis settings **
            They will be read either form a local settings file (if flag_permanent_settings=False)
            or from the keys in the input analysis file (if flag_permanent_settings=True)
            :param relative_path_settings: only used if flag_permanent_settings=False and allows to specify folder containing settings.user_name.yaml
            :rtype: nothing, saves temporary settings.user_name.yaml on disk
        """

        if self.data_analysis.GeneralParameters.flag_permanent_settings:
            # Read settings from analysis input file (yaml file)
            if self.verbose:
                print('flag_permanent_settings is set to True')
            data_settings = self.data_analysis.PermanentSettings.__dict__
        else:
            # Read settings from local settings file (yaml file)
            path_settings, data_settings = read_settings_file(relative_path_settings=relative_path_settings, verbose=False)  # Information will be displayed later, to verbose=False here
            if self.verbose:
                user_name = os.getlogin()
                print('flag_permanent_settings is set to False')
                print('user_name:               {}'.format(user_name))
                print('relative_path_settings:  {}'.format(relative_path_settings))
                print('full_path_file_settings: {}'.format(path_settings))

        # Assign the keys read either from permanent-settings or local-settings
        for name, _ in self.settings.__dict__.items():
            if name in dict(data_settings):
                value = dict(data_settings)[name]
                self.setAttribute(self.settings, name, value)
                if value:
                    if self.verbose: print('{} : {}. Added.'.format(name, value))
            else:
                if self.verbose: print('{}: not found in the settings. Skipped.'.format(name))

    def _set_library_folder(self):
        """
            ** Check if model library folder is present. If not, raise an exception. **
        """
        # Resolve the library path
        if self.settings.local_library_path:
            self.library_path = Path(self.settings.local_library_path).resolve()
            if not os.path.isdir(self.library_path):
                raise Exception(f'Defined library folder {self.library_path} does not exist. Key to change: "local_library_path" in the settings.')
        else:
            raise Exception(f'Library folder must be defined. Key to change: "local_library_path" in the settings.')

        if self.verbose:
            print('Model library path:    {}'.format(self.library_path))

    def store_model_objects(self, path_output_file: str):
        """
        ** Stores the dictionary of BuilderModel objects in a pickle file at the specified path **
        This can be helpful to load the list of models instead of generating it at every iteration of a parametric simulation or cooperative simulation
        :param path_output_file: full path of file to write
        :type path_output_file str
        :return: Nothing, writes pickle file on disk
        :rtype None
        """
        # Make sure the target folder exists
        make_folder_if_not_existing(os.path.dirname(path_output_file), verbose=self.verbose)

        # Store the objects as pickle file
        with open(path_output_file, 'wb') as output:
            pickle.dump(self.list_models, output, pickle.HIGHEST_PROTOCOL)

        if self.verbose: print(f'File {path_output_file} saved.')

    def write_analysis_file(self, path_output_file: str, verbose: bool = None):
        """
        ** Write the analysis data in the target file **
        This can be helpful to keep track of the final state of the DataAnalysis object before running it, especially if it was modified programmatically.
        :param path_output_file: string to the file to write
        :return: None
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        # Make sure the target folder exists
        make_folder_if_not_existing(os.path.dirname(path_output_file), verbose=verbose)

        #print(self.data_analysis.PermanentSettings.PSPICE_path)
        # Write the STEAM analysis data to a yaml file
        dict_to_yaml({**self.data_analysis.dict()}, path_output_file, list_exceptions=['AnalysisStepSequence',
                                                                                       'variables_to_change'])
        if verbose: print(f'File {path_output_file} saved.')

    def run_analysis(self, verbose: bool = None):
        """
            ** Run the analysis **
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        # Unpack and assign default values
        step_definitions = self.data_analysis.AnalysisStepDefinition

        # Print the selected analysis steps
        if verbose:
            print('Defined analysis steps (not in sequential order):')
            for def_step in step_definitions:
                print(f'{def_step}')

        # Print analysis sequence
        if verbose: print('Defined sequence of analysis steps:')
        for s, seq_step in enumerate(self.data_analysis.AnalysisStepSequence):
            if verbose: print('Step {}/{}: {}'.format(s + 1, len(self.data_analysis.AnalysisStepSequence), seq_step))

        # Run analysis (and re-print analysis steps)
        if verbose: print('Analysis started.')
        for s, seq_step in enumerate(self.data_analysis.AnalysisStepSequence):
            if verbose: print('Step {}/{}: {}'.format(s + 1, len(self.data_analysis.AnalysisStepSequence), seq_step))
            step = step_definitions[seq_step]  # this is the object containing the information about the current step
            if step.type == 'MakeModel':
                self.step_make_model(step, verbose=verbose)
            elif step.type == 'ModifyModel': #
                self.step_modify_model(step, verbose=verbose)
            elif step.type == 'ModifyModelMultipleVariables':  #
                self.step_modify_model_multiple_variables(step, verbose=verbose)
            elif step.type == 'RunSimulation':
                self.step_run_simulation(step, verbose=verbose)
            elif step.type == 'PostProcess':
                self.postprocess_output = self.step_postprocess(step, verbose=verbose)
            elif step.type == 'SetUpFolder':
                # self.step_setup_folder(step, verbose=verbose)
                pass  # trying to see which tests pass without this step being enabled
            elif step.type == 'AddAuxiliaryFile':
                # self.add_auxiliary_file(step, verbose=verbose)
                pass  # trying to see which tests pass without this step being enabled
            elif step.type == 'CopyFile':
                self.copy_file_to_target(step, verbose=verbose)
            elif step.type == 'CopyFileRelative':
                self.copy_file_relative(step, verbose=verbose)
            elif step.type == 'RunCustomPyFunction':
                self.run_custom_py_function(step, verbose=verbose)
            elif step.type == 'RunViewer':
                self.run_viewer(step, verbose=verbose) # Add elif plot_map2d,  two paths save plot to folder png
            elif step.type == 'CalculateMetrics':
                self.calculate_metrics(step, verbose=verbose)
            elif step.type == 'LoadCircuitParameters':
                self.load_circuit_parameters(step, verbose=verbose)
            elif step.type == 'WriteStimulusFile':
                self.write_stimuli_from_interpolation(step, verbose=verbose)
            elif step.type == 'ParsimEvent':
                self.run_parsim_event(step, verbose=verbose)
            elif step.type == 'ParametricSweep':
                self.run_parsim_sweep(step, verbose=verbose)
            elif step.type == 'ParsimConductor':
                self.run_parsim_conductor(step, verbose=verbose)
            else:
                raise Exception('Unknown type of analysis step: {}'.format(step.type))

    def step_make_model(self, step, verbose: bool = None):
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self
        if verbose:
            print('Making model object named {}'.format(str(step.model_name)))
        # Always assume the STEAM models folder structure, which contains subfolders "circuits", "conductors", "cosims", "magnets"
        file_model_data = os.path.join(self.library_path, f'{step.case_model}s', step.file_model_data, 'input', f'modelData_{step.file_model_data}.yaml')

        # Build the model
        if step.case_model == 'cosim':
            BM = BuilderCosim(file_model_data=file_model_data, data_settings=self.settings, verbose=step.verbose)
        else:
            BM = BuilderModel(file_model_data=file_model_data, case_model=step.case_model, data_settings=self.settings,
                              results_folder_name='output', verbose=step.verbose)

        # Build simulation file (Call the model builder of the selected tools)
        if step.simulation_number is not None:
            BM = self.setup_sim(BM=BM, step=step, sim_number=step.simulation_number, verbose=step.verbose)

        # Add the reference to the model in the dictionary
        self.list_models[step.model_name] = BM

    def step_modify_model(self, step, verbose: bool = None):
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self
        if verbose:
            print('Modifying model object named {}'.format(str(step.model_name)))

        # Check inputs
        if step.model_name not in self.list_models:
            raise Exception(f'Name of the model to modify ({step.model_name}) does not correspond to any of the defined models.')
        len_variable_value = len(step.variable_value)
        len_simulation_numbers = len(step.simulation_numbers)
        len_new_model_name = len(step.new_model_name)
        if len_new_model_name > 0 and not len_new_model_name == len_variable_value:
            raise Exception(f'The length of new_model_name and variable_value must be the same, but they are {len_new_model_name} and {len_variable_value} instead.')
        if len_simulation_numbers > 0 and not len_simulation_numbers == len_variable_value:
            print(f'simulation_numbers: {step.simulation_numbers}')
            print(f'variable_value: {step.variable_value}')
            print(f'type: {step.type}')
            raise Exception(f'The length of simulation_numbers and variable_value must be the same, but they are {len_simulation_numbers} and {len_variable_value} instead.')

        # Change the value of the selected variable
        for v, value in enumerate(step.variable_value):
            BM: Union[BuilderModel, BuilderCosim] = self.list_models[
                step.model_name]  # original BuilderModel or BuilderCosim object
            case_model = BM.case_model  # model case (magnet, conductor, circuit, cosim)

            if 'Conductors[' in step.variable_to_change:  # Special case when the variable to change is the Conductors key
                if verbose:
                    idx_conductor = int(step.variable_to_change.split('Conductors[')[1].split(']')[0])
                    conductor_variable_to_change = step.variable_to_change.split('].')[1]
                    print(f'Variable {step.variable_to_change} is treated as a Conductors key. Conductor index: #{idx_conductor}. Conductor variable to change: {conductor_variable_to_change}.')

                    old_value = get_attribute_model(case_model, BM, conductor_variable_to_change, idx_conductor)
                    print('Variable {} changed from {} to {}.'.format(conductor_variable_to_change, old_value, value))

                if len_new_model_name > 0:  # Make a new copy of the BuilderModel object, and change it
                    self.list_models[step.new_model_name[v]] = deepcopy(BM)
                    BM = self.list_models[step.new_model_name[v]]

                    if case_model == 'conductor':
                        rsetattr(BM.conductor_data.Conductors[idx_conductor], conductor_variable_to_change, value)
                    else:
                        rsetattr(BM.model_data.Conductors[idx_conductor], conductor_variable_to_change, value)

                    if verbose:
                        print(f'Model {step.model_name} copied to model {step.new_model_name[v]}.')
                else:  # Change the original BuilderModel object
                    if case_model == 'conductor':
                        rsetattr(BM.conductor_data.Conductors[idx_conductor], conductor_variable_to_change, value)
                    else:
                        rsetattr(BM.model_data.Conductors[idx_conductor], conductor_variable_to_change, value)

            else:  # Standard case when the variable to change is not the Conductors key
                if verbose:
                    old_value = get_attribute_model(case_model, BM, step.variable_to_change)
                    print('Variable {} changed from {} to {}.'.format(step.variable_to_change, old_value, value))

                if len_new_model_name > 0:  # Make a new copy of the BuilderModel object, and change it
                    self.list_models[step.new_model_name[v]] = deepcopy(BM)
                    BM = self.list_models[step.new_model_name[v]]
                    set_attribute_model(case_model, BM, step.variable_to_change, value)
                    if verbose:
                        print('Model {} copied to model {}.'.format(step.model_name, step.new_model_name[v]))

                else:  # Change the original BuilderModel object
                    set_attribute_model(case_model, BM, step.variable_to_change, value)

            # Special case: If the sub-keys of "Source" are changed, a resetting of the input paths is triggered
            if step.variable_to_change.startswith('Sources.'):
                BM.set_input_paths()

            # Build simulation file
            if len_simulation_numbers > 0:
                # Set paths of input files
                BM.set_input_paths()
                BM = self.setup_sim(BM=BM, step=step, sim_number=step.simulation_numbers[v], verbose=step.verbose)

    def step_modify_model_multiple_variables(self, step, verbose: bool = None):
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self
        if verbose:
            print('Modifying model object named {}'.format(str(step.model_name)))

        # Check inputs
        if step.model_name not in self.list_models:
            raise Exception(f'Name of the model to modify ({step.model_name}) does not correspond to any of the defined models.'.format(step.model_name))
        len_variables_to_change = len(step.variables_to_change)
        len_variables_value = len(step.variables_value)
        if not len_variables_to_change == len_variables_value:
            raise Exception('The length of variables_to_change and variables_value must be the same, but they are {} and {} instead.'.format(len_variables_to_change, len_variables_value))

        # Loop through the list of variables to change
        for v, variable_to_change in enumerate(step.variables_to_change):
            # For each variable to change, make an instance of an ModifyModel step and call the step_modify_model() method
            next_step = ModifyModel(type='ModifyModel')
            next_step.model_name = step.model_name
            next_step.variable_to_change = variable_to_change
            next_step.variable_value = step.variables_value[v]
            if v + 1 == len_variables_to_change:
                # If this is the last variable to change, import new_model_name and simulation_numbers from the step
                next_step.new_model_name = step.new_model_name
                next_step.simulation_numbers = step.simulation_numbers
            else:
                # else, set new_model_name and simulation_numbers to empty lists to avoid making models/simulations for intermediate changes
                next_step.new_model_name = []
                next_step.simulation_numbers = []
            next_step.simulation_name = step.simulation_name
            next_step.software = step.software
            next_step.flag_plot_all = step.flag_plot_all
            next_step.flag_json = step.flag_json
            self.step_modify_model(next_step, verbose=verbose)
        if verbose:
            print('All variables of step {} were changed.'.format(step))

    def step_run_simulation(self, step, verbose: bool = None):
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self
        software = step.software
        simulation_name = step.simulation_name
        simFileType = step.simFileType
        sim_numbers = step.simulation_numbers
        if simulation_name == 'from_last_parametric_list':
            sim_numbers = list(self.input_parsim_sweep_df.simulation_number.to_numpy())
            sim_names = list(self.input_parsim_sweep_df.simulation_name.to_numpy())
        elif simulation_name == 'from_SetUpFolder_step':
            sim_numbers = list(self.input_parsim_sweep_df.simulation_number.to_numpy())
            for step_data in self.data_analysis.AnalysisStepDefinition.values():
                if step_data.type == 'SetUpFolder':
                    sim_name = step_data.simulation_name
            sim_names = len(sim_numbers) * [sim_name]
        elif simulation_name == 'from_ParsimEvent_step':
            for step_data in self.data_analysis.AnalysisStepDefinition.values():
                if step_data.type == 'ParsimEvent':
                    sim_numbers = step_data.simulation_numbers
                    sim_name = step_data.simulation_name
            sim_names = len(sim_numbers) * [sim_name]
        else:
            sim_names = [simulation_name] * len(sim_numbers)

        if len(sim_numbers) != len(set(sim_numbers)):
            raise Exception('Simulation numbers must be unique!')

        for sim_name, sim_number in zip(sim_names, sim_numbers):
            if verbose:
                print('Running simulation of model {} #{} using {}.'.format(simulation_name, sim_number, software))
            # Run simulation
            self.run_sim(software, sim_name, sim_number, simFileType, verbose)

    def step_postprocess(self, step, verbose: bool = None):  # run sequence variable
        """
        The postprocessing method is for comparing map2d files between FiQuS, SIGMA and ROXIE. It generates 5 difference plots:
        1) Absolute Bmod difference.
        2) Difference in Bx and By
        3) Bx and By
        4) Bmod
        5) relative error in Bx and By
        :param step:
        :param verbose:
        :return:
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self
        if verbose: print('postprocessing')
        map2d_to_compare = dict()

        if step.sources:
            # For now, only two sources can be compared at the same time.
            if len(step.sources) != 2:
                raise ValueError("For now it's only supported to compare two map2d files. Change sources in your yaml file.")

            # Unwrap numbers per source
            for source, source_sim_nbr, fiqus_csv_idx in zip(step.sources, step.sources_sim_nrs, step.sources_FiQuS_csv_idx):
                source_sim_nbr = source_sim_nbr[0]

                if source.lower() == 'sigma':
                    if len(fiqus_csv_idx) > 0:
                        fiqus_csv_idx = fiqus_csv_idx[0]
                        if fiqus_csv_idx is not None:
                            warnings.warn(
                                f"Fiqus csv index is set to other than None for {source}. Observe this is only applicable to FiQuS")
                    # Check if files exist from SIGMA simulation
                    local_SIGMA_folder = self._get_local_folder('local_SIGMA_folder')
                    path_result_txt_Bx = os.path.join(local_SIGMA_folder, f"{step.simulation_name}_{source_sim_nbr}", "output", "mf.Bx.txt")
                    path_result_txt_By = os.path.join(local_SIGMA_folder, f"{step.simulation_name}_{source_sim_nbr}", "output", "mf.By.txt")
                    path_new_file = os.path.join(local_SIGMA_folder, f"{step.simulation_name}_{source_sim_nbr}", "output", "B_field_map2d.map2d")
                    path_reference_roxie = os.path.join(local_SIGMA_folder, f"{step.simulation_name}_{source_sim_nbr}", f"{step.simulation_name}_ROXIE_REFERENCE.map2d")

                    if not os.path.exists(path_result_txt_Bx):
                        raise Warning(f"No Bx file is found: {path_result_txt_Bx}, please check that simulation ran successfully.")
                    elif not os.path.exists(path_result_txt_By):
                        raise Warning(f"No By file is found: {path_result_txt_By}, please check that simulation ran successfully.")
                    elif not os.path.exists(path_reference_roxie):
                        print(path_reference_roxie)
                        raise Warning(f"No Roxie reference file is found: {path_reference_roxie}, please check model_data.yaml in options_sigma that key map2d is specified.")
                    else:
                        # Export results to map2d file
                        try:
                            export_B_field_txt_to_map2d_SIGMA(path_reference_roxie, path_result_txt_Bx, path_result_txt_By, path_new_file)
                        except:
                            print(f"Can't generate map2d output. This can only be done for stationary studies and with the same coordinate in output files and roxie reference")

                elif source.lower() == 'fiqus':
                    fiqus_csv_idx = fiqus_csv_idx[0]
                    # Take latest run by reading file.
                    local_FiQuS_folder = self._get_local_folder('local_FiQuS_folder')
                    path_log = os.path.join(local_FiQuS_folder, step.simulation_name, f"{step.simulation_name}_{source_sim_nbr}", "csv_run_log.csv")
                    with open(path_log, 'r', newline='') as csv_file:
                        reader = csv.reader(csv_file)
                        rows = list(reader)

                    flattened_rows = [value for sublist in rows for value in sublist]
                    if fiqus_csv_idx is not None:
                    # Retrieve the last value from the flattened list
                        last_line_value = flattened_rows[fiqus_csv_idx]
                    # If fiqus_csv_idx is None, take latest index
                    else:
                        last_line_value = flattened_rows[-1]
                    path_new_file = os.path.join(last_line_value, step.simulation_name+".map2d")
                    if not os.path.exists(path_new_file):
                        raise Warning(f"Output FiQuS file in the location {path_new_file} is not present.")

                elif source.lower() == 'roxie':
                    # Take latest run by reading file.
                    if len(fiqus_csv_idx) > 0:
                        fiqus_csv_idx = fiqus_csv_idx[0]
                        if fiqus_csv_idx is not None:
                            warnings.warn(
                                f"Fiqus csv index is set to other than None for {source}. Observe this is only applicable to FiQuS")
                    path_new_file = os.path.join(self.library_path, 'magnets', step.simulation_name, 'input',
                                                 step.simulation_name + ".map2d")

                else:
                    raise ValueError("Invalid source name.")

                map2d_to_compare[source] = path_new_file

            keys_list = list(map2d_to_compare.keys())
            key1 = keys_list[0]
            key2 = keys_list[1]
            value1 = map2d_to_compare[key1]
            value2 = map2d_to_compare[key2]
            prefix = f"{step.simulation_name}"
            exported_stats = generate_report_from_map2d(prefix, step.path_to_saved_files,
                                                        value1, key1, value2, key2, "coil", save=True)
            return exported_stats

        else:
            return None

    # def step_setup_folder(self, step, verbose: bool = None):
    #     """
    #     Set up simulation working folder.
    #     The function applies a different logic for each simulation software.
    #     """
    #     verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self
    #     if verbose:
    #         print(f'Set up folder of model {step.simulation_name} for {step.software}.')
    #
    #     if step.software == 'FiQuS':
    #         # make top level output folder
    #         local_FiQuS_folder = self._get_local_folder('local_FiQuS_folder')
    #         make_folder_if_not_existing(local_FiQuS_folder, verbose=verbose)
    #
    #         # make simulation name folder inside top level folder
    #         make_folder_if_not_existing(os.path.join(local_FiQuS_folder, step.simulation_name))
    #
    #     elif step.software == 'LEDET':
    #         local_LEDET_folder = self._get_local_folder('local_LEDET_folder')
    #         # Make magnet input folder and its subfolders
    #         make_folder_if_not_existing(Path(local_LEDET_folder / step.simulation_name / 'Input').resolve(), verbose=verbose)
    #         make_folder_if_not_existing(Path(local_LEDET_folder / step.simulation_name / 'Input' / 'Control current input').resolve(), verbose=verbose)
    #         make_folder_if_not_existing(Path(local_LEDET_folder / step.simulation_name / 'Input' / 'Initialize variables').resolve(), verbose=verbose)
    #         make_folder_if_not_existing(Path(local_LEDET_folder / step.simulation_name / 'Input' / 'InitializationFiles').resolve(), verbose=verbose)
    #
    #         # # Copy csv files from the output folder
    #         # list_csv_files = [entry for entry in os.listdir(self.output_path) if (step.simulation_name in entry) and ('.csv' in entry)]
    #         # for csv_file in list_csv_files:
    #         #     file_to_copy = os.path.join(self.output_path, csv_file)
    #         #     file_copied = os.path.join(Path(local_LEDET_folder / step.simulation_name / 'Input').resolve(), csv_file)
    #         #     shutil.copyfile(file_to_copy, file_copied)
    #         #     if verbose: print(f'Csv file {file_to_copy} copied to {file_copied}.')
    #         #
    #         # # Make magnet field-map folder
    #         # field_maps_folder = Path(local_LEDET_folder / '..' / 'Field maps' / step.simulation_name).resolve()
    #         # make_folder_if_not_existing(field_maps_folder, verbose=verbose)
    #         #
    #         # # Copy field-map files from the output folder
    #         # list_field_maps = [entry for entry in os.listdir(self.output_path) if (step.simulation_name in entry) and ('.map2d' in entry)]
    #         # for field_map in list_field_maps:
    #         #     file_to_copy = os.path.join(self.output_path, field_map)
    #         #     file_copied = os.path.join(field_maps_folder, field_map)
    #         #     shutil.copyfile(file_to_copy, file_copied)
    #         #     if verbose: print(f'Field map file {file_to_copy} copied to {file_copied}.')
    #
    #     elif step.software == 'PSPICE':
    #         local_PSPICE_folder = self._get_local_folder('local_PSPICE_folder')
    #         local_model_folder = Path(local_PSPICE_folder / step.simulation_name).resolve()
    #         # Make magnet input folder
    #         make_folder_if_not_existing(local_model_folder, verbose=verbose)
    #
    #         # Copy lib files from the output folder
    #         list_lib_files = [entry for entry in os.listdir(self.output_path) if
    #                           (step.simulation_name in entry) and ('.lib' in entry)]
    #         for lib_file in list_lib_files:
    #             file_to_copy = os.path.join(self.output_path, lib_file)
    #             file_copied = os.path.join(local_model_folder, lib_file)
    #             shutil.copyfile(file_to_copy, file_copied)
    #             if verbose: print('Lib file {} copied to {}.'.format(file_to_copy, file_copied))
    #
    #         # Copy stl files from the output folder
    #         list_stl_files = [entry for entry in os.listdir(self.output_path) if
    #                           (step.simulation_name in entry) and ('.stl' in entry)]
    #         for stl_file in list_stl_files:
    #             file_to_copy = os.path.join(self.output_path, stl_file)
    #             file_copied = os.path.join(local_model_folder, stl_file)
    #             shutil.copyfile(file_to_copy, file_copied)
    #             if verbose: print('Stl file {} copied to {}.'.format(file_to_copy, file_copied))
    #
    #     elif step.software == 'SIGMA':
    #         pass  # folder is generated later
    #
    #     elif step.software == 'XYCE':
    #         local_XYCE_folder = self._get_local_folder('local_XYCE_folder')
    #         local_model_folder = str(Path(local_XYCE_folder / step.simulation_name).resolve())
    #         # Make circuit input folder
    #         make_folder_if_not_existing(local_model_folder, verbose=verbose)
    #
    #         # Copy lib files from the output folder
    #         list_lib_files = [entry for entry in os.listdir(self.output_path) if
    #                           (step.simulation_name in entry) and ('.lib' in entry)]
    #         for lib_file in list_lib_files:
    #             file_to_copy = os.path.join(self.output_path, lib_file)
    #             file_copied = os.path.join(local_model_folder, lib_file)
    #             shutil.copyfile(file_to_copy, file_copied)
    #             if verbose: print('Lib file {} copied to {}.'.format(file_to_copy, file_copied))
    #
    #         # Set default value to output_path if it has not been specified
    #         if not self.output_path and self.data_analysis.PermanentSettings.local_XYCE_folder:
    #             self.output_path = self.data_analysis.PermanentSettings.local_XYCE_folder
    #
    #         # Copy stl files from the output folder
    #         stl_path = os.path.join(self.output_path, 'Stimulus')
    #         if not os.path.exists(stl_path):
    #             os.makedirs(stl_path)
    #         list_stl_files = [entry for entry in os.listdir(stl_path) if
    #                           (step.simulation_name in entry) and ('.csv' in entry)]
    #         stl_path_new = os.path.join(local_model_folder, 'Stimulus')
    #         if os.path.exists(stl_path_new):
    #             shutil.rmtree(stl_path_new)
    #         os.mkdir(stl_path_new)
    #
    #         for stl_file in list_stl_files:
    #             file_to_copy = os.path.join(self.output_path, stl_file)
    #             file_copied = os.path.join(stl_path_new, stl_file)
    #             shutil.copyfile(file_to_copy, file_copied)
    #             if verbose: print('Stl file {} copied to {}.'.format(file_to_copy, file_copied))
    #
    #     else:
    #         raise Exception(f'Software {step.software} not supported for automated folder setup.')

    # def add_auxiliary_file(self, step, verbose: bool = None):
    #     """
    #     Copy the desired auxiliary file to the output folder
    #     """
    #     verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self
    #     # Unpack
    #     full_path_aux_file = Path(step.full_path_aux_file).resolve()
    #     new_file_name = step.new_file_name
    #     output_path = self.output_path
    #
    #     # If no new name is provided, use the old file name
    #     if new_file_name == None:
    #         new_file_name = ntpath.basename(full_path_aux_file)
    #
    #     # Copy auxiliary file to the output folder
    #     full_path_output_file = os.path.join(output_path, new_file_name)
    #     make_folder_if_not_existing(os.path.dirname(full_path_output_file))  # in case the output folder does not exist, make it
    #     shutil.copyfile(full_path_aux_file, full_path_output_file)
    #     if verbose: print(f'File {full_path_aux_file} was copied to {full_path_output_file}.')
    #
    #     # Build simulation file
    #     BM = self.list_models['BM']
    #     len_simulation_numbers = len(step.simulation_numbers)
    #     if len_simulation_numbers > 0:
    #         for simulation_number in step.simulation_numbers:
    #             if step.software == 'FiQuS':
    #                 self.setup_sim_FiQuS(simulation_name=step.simulation_name, sim_number=simulation_number)
    #             elif step.software == 'LEDET':
    #                 BM = self.setup_sim_LEDET(BM=BM, simulation_name=step.simulation_name, sim_number=simulation_number,
    #                                           flag_json=step.flag_json, flag_plot_all=step.flag_plot_all, verbose=step.verbose)
    #             elif step.software == 'PSPICE':
    #                 BM = self.setup_sim_PSPICE(BM=BM, simulation_name=step.simulation_name, sim_number=step.simulation_number,
    #                                            verbose=step.verbose)
    #             elif step.software == 'PyBBQ':
    #                 BM = self.setup_sim_PyBBQ(BM=BM, simulation_name=step.simulation_name, sim_number=step.simulation_number, verbose=step.verbose)
    #             elif step.software == 'XYCE':
    #                 BM = self.setup_sim_XYCE(BM=BM, simulation_name=step.simulation_name, sim_number=step.simulation_number, verbose=step.verbose)

    def copy_file_relative(self, step, verbose: bool = None):
        """
            Copy one file from a location to another (the destination folder can be different from the analysis output folder)
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        def get_full_path(obj):
            paths_out = []
            for local_tool_folder, simulation_name, remaining_path in zip(obj.local_tool_folders, obj.simulation_names, obj.reminder_paths):
                if not hasattr(self.data_analysis.PermanentSettings, local_tool_folder):
                    raise Exception(f'Key {local_tool_folder} is not found in the analysis permanent settings.')
                if self.data_analysis.GeneralParameters.flag_permanent_settings:
                    abs_tool_path = self.data_analysis.PermanentSettings.__dict__[local_tool_folder]
                else:
                    abs_tool_path = self.settings.__dict__[local_tool_folder]
                if local_tool_folder == 'local_library_path':
                    abs_tool_path = os.path.join(abs_tool_path, f"{self.data_analysis.AnalysisStepDefinition['makeModel'].case_model}s")
                paths_out.append(str(Path(os.path.join(os.getcwd(), abs_tool_path, simulation_name, remaining_path)).resolve()))
            return paths_out

        for full_path_file_to_copy, full_path_file_target in zip(get_full_path(step.copy_from), get_full_path(step.copy_to)):
            print(f'Coping from: {full_path_file_to_copy}')
            print(f'Coping to: {full_path_file_target}')
            # Make sure the target folder exists
            make_folder_if_not_existing(os.path.dirname(full_path_file_target), verbose=verbose)

            # Copy file
            try:
                shutil.copyfile(full_path_file_to_copy, full_path_file_target)
            except shutil.SameFileError:
                if verbose: print(f'File {full_path_file_to_copy} is the same as {full_path_file_target}, so no need to copy it.')

    @staticmethod
    def copy_file_to_target(step, verbose: bool = False):
        """
            Copy one file from a location to another (the destination folder can be different from the analysis output folder)
        """
        # Unpack
        full_path_file_to_copy = Path(step.full_path_file_to_copy).resolve()
        full_path_file_target = Path(step.full_path_file_target).resolve()

        # Make sure the target folder exists
        make_folder_if_not_existing(os.path.dirname(full_path_file_target), verbose=verbose)

        # Copy file
        try:
            shutil.copyfile(full_path_file_to_copy, full_path_file_target)
        except shutil.SameFileError:
            if verbose: print(f'File {full_path_file_to_copy} is the same as {full_path_file_target}, so no need to copy it.')

    def run_custom_py_function(self, step, verbose: bool = None):
        """
            Run a custom Python function with given arguments
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self
        # If the step is not enabled, the function will not be run
        if not step.flag_enable:
            if verbose: print(f'flag_enable set to False. Custom function {step.function_name} will not be run.')
            return

        # Unpack variables
        function_name = step.function_name
        function_arguments = step.function_arguments
        if step.path_module:
            # Import the custom function from a specified location different from the default location
            # This Python magic comes from: https://stackoverflow.com/questions/67631/how-do-i-import-a-module-given-the-full-path
            path_module = os.path.join(Path(step.path_module).resolve())
            custom_module = importlib.util.spec_from_file_location('custom_module',
                                                                   os.path.join(path_module, function_name + '.py'))
            custom_function_to_load = importlib.util.module_from_spec(custom_module)
            sys.modules['custom_module'] = custom_function_to_load
            custom_module.loader.exec_module(custom_function_to_load)
            custom_function = getattr(custom_function_to_load, function_name)
        else:
            # Import the custom function from the default location
            path_module = f'steam_sdk.analyses.custom_analyses.{function_name}.{function_name}'
            custom_module = importlib.import_module(path_module)
            custom_function = getattr(custom_module, function_name)

        # Run custom function with the given argument
        if verbose: print(
            f'Custom function {function_name} from module {path_module} will be run with arguments: {function_arguments}.')
        output = custom_function(function_arguments)
        return output

    def run_viewer(self, step, verbose: bool = None):
        """
            Make a steam_sdk.viewers.Viewer.Viewer() object and run its analysis
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        # Unpack variables
        viewer_name = step.viewer_name

        if verbose: print(f'Making Viewer object named {viewer_name}.')

        # Make a steam_sdk.viewers.Viewer.Viewer() object and run its analysis
        V = Viewer(file_name_transients=step.file_name_transients,
                   list_events=step.list_events,
                   flag_analyze=step.flag_analyze,
                   flag_display=step.flag_display,
                   flag_save_figures=step.flag_save_figures,
                   path_output_html_report=step.path_output_html_report,
                   path_output_pdf_report=step.path_output_pdf_report,
                   figure_types=step.figure_types,
                   verbose=step.verbose)

        # Add the reference to the Viewer object in the dictionary
        self.list_viewers[viewer_name] = V

    def calculate_metrics(self, step, verbose: bool = None):
        """
        Calculate metrics (usually to compare two or more measured and/or simulated signals)
        :param step: STEAM analysis step of type CalculateMetrics, which has attributes:
        - viewer_name: the name of the Viewer object containing the data to analyze
        - metrics_to_calculate: list that defines the type of calculation to perform for each metric.
        - variables_to_analyze: list
        :param verbose:
        :return:
        """
        """
            
            The metrics to calculate are indicated in the list metrics_to_calculate, which defines the type of calculation of each metric.

        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self
        if verbose: print(f'Calculate metrics.')

        # Unpack variables
        viewer_name = step.viewer_name
        metrics_name = step.metrics_name
        metrics_to_calculate = step.metrics_to_calculate
        variables_to_analyze = step.variables_to_analyze
        # Note: Avoid unpacking "list_viewers = self.list_viewers" since the variable usually has large size

        # Check input
        if not viewer_name in self.list_viewers:
            raise Exception(
                f'The selected Viewer object named {viewer_name} is not present in the current Viewer list: {self.list_viewers}. Add an analysis step of type RunViewer to define a Viewer object.')
        # if len(metrics_to_calculate) != len(variables_to_analyze):
        #     raise Exception(f'The lengths of the lists metrics_to_calculate and variables_to_analyze must match, but are {len(metrics_to_calculate)} and {len(variables_to_analyze)} instead.')

        # If the Analysis object contains a metrics set with the selected metrics_name, retrieve it: the new metrics entries will be appended to it
        if metrics_name in self.list_metrics:
            current_list_output_metrics = self.list_metrics[metrics_name]
        else:
            # If not, make a new metrics set
            current_list_output_metrics = {}

        # Loop through all events listed in the selected Viewer object
        for event_id in self.list_viewers[viewer_name].list_events:
            event_label = self.list_viewers[viewer_name].dict_events['Event label'][event_id - 1]
            if verbose: print(f'Event #{event_id}: "{event_label}".')
            current_list_output_metrics[event_label] = {}

            # For each selected pair of variables to analyze, calculate metrics
            for pair_var in variables_to_analyze:
                var_to_analyze = pair_var[0]
                var_reference = pair_var[1]

                # Check that the selected signal to analyze and its reference signal (if they are defined) exist in the current event
                if len(var_to_analyze) > 0:
                    if var_to_analyze in self.list_viewers[viewer_name].dict_data[event_label]:
                        if 'x_sim' in self.list_viewers[viewer_name].dict_data[event_label][
                            var_to_analyze]:  # usually the variable to analyze is a simulated signal
                            x_var_to_analyze = self.list_viewers[viewer_name].dict_data[event_label][var_to_analyze][
                                'x_sim']
                            y_var_to_analyze = self.list_viewers[viewer_name].dict_data[event_label][var_to_analyze][
                                'y_sim']
                        elif 'x_meas' in self.list_viewers[viewer_name].dict_data[event_label][
                            var_to_analyze]:  # but a measured signal is also supported
                            x_var_to_analyze = self.list_viewers[viewer_name].dict_data[event_label][var_to_analyze][
                                'x_meas']
                            y_var_to_analyze = self.list_viewers[viewer_name].dict_data[event_label][var_to_analyze][
                                'y_meas']
                        else:
                            print(
                                f'WARNING: Viewer {viewer_name}: Event "{event_label}": Signal label "{var_to_analyze}" not found. Signal skipped.')
                            continue
                    else:
                        print(
                            f'WARNING: Viewer "{viewer_name}": Event "{event_label}": Signal label "{var_to_analyze}" not found. Signal skipped.')
                        continue
                else:
                    raise Exception(
                        f'Viewer "{viewer_name}": Event "{event_label}": The first value of each pair in variables_to_analyze cannot be left empty, but {pair_var} was found.')

                if len(var_reference) > 0:  # if the string is empty, skip this check (it is possible to run the metrics calculation on one variable only)
                    if var_reference in self.list_viewers[viewer_name].dict_data[event_label]:
                        if 'x_meas' in self.list_viewers[viewer_name].dict_data[event_label][
                            var_reference]:  # usually the variable to analyze is a measured signal
                            x_var_reference = self.list_viewers[viewer_name].dict_data[event_label][var_reference][
                                'x_meas']
                            y_var_reference = self.list_viewers[viewer_name].dict_data[event_label][var_reference][
                                'y_meas']
                        elif 'x_sim' in self.list_viewers[viewer_name].dict_data[event_label][
                            var_reference]:  # but a simulated signal is also supported
                            x_var_reference = self.list_viewers[viewer_name].dict_data[event_label][var_reference][
                                'x_sim']
                            y_var_reference = self.list_viewers[viewer_name].dict_data[event_label][var_reference][
                                'y_sim']
                        else:
                            print(
                                f'WARNING: Viewer "{viewer_name}": Event "{event_label}": Signal label "{var_reference}" not found. Signal skipped.')
                            continue
                    else:
                        print(
                            f'WARNING: Viewer "{viewer_name}": Event "{event_label}": Signal label "{var_reference}" not found. Signal skipped.')
                        continue
                else:  # It is possible to run the metrics calculation on one variable only, without a reference signal
                    x_var_reference = None
                    y_var_reference = None

                # Perform the metrics calculation
                if verbose: print(
                    f'Viewer "{viewer_name}": Event "{event_label}": Metrics calculated using signals "{var_to_analyze}" and "{var_reference}".')

                # Calculate the metrics
                # output_metric = PostprocsMetrics(
                #     metrics_to_calculate=metrics_to_calculate,
                #     x_value=x_var_to_analyze,
                #     y_value=y_var_to_analyze,
                #     x_ref=x_var_reference,
                #     y_ref=y_var_reference,
                #     flag_run=True)

                #output metric is a list, containing
                output_metric = PostprocsMetrics(metrics_to_do=metrics_to_calculate,
                                                 var_to_interpolate=y_var_to_analyze,
                                                 var_to_interpolate_ref=y_var_reference, time_vector=x_var_to_analyze,
                                                 time_vector_ref=x_var_reference)

                # dictionary that contains several metrics of a signal (var_to_analyze) for one event (event_label)
                current_list_output_metrics[event_label][var_to_analyze] = output_metric.metrics_result

        # Add the reference to the Viewer object in the dictionary, here they are now saved with a name e.g. "metrics_1"
        self.list_metrics[metrics_name] = current_list_output_metrics

        ################################################################################################################
        ## return a summary across all signals, across all keys in the metrics --> this is needed for Dakota
        list_metric_values = []
        # calculate mean value across all values in the metrics:
        for event_label, metrics_for_a_event_label in current_list_output_metrics.items():
            for var_to_analyze, metrics_for_a_var_to_analyze in  current_list_output_metrics[event_label].items():
                # this should be a list across all metrics to calculate:
                list_metric_values.extend(metrics_for_a_var_to_analyze)
        software = "PSPICE" #TODO: add software here as a key for a dict, that is passed
        self.summary =np.mean(list_metric_values)
        ################################################################################################################

        return current_list_output_metrics

    def load_circuit_parameters(self, step, verbose: bool = None):
        """
        Load global circuit parameters from a .csv file into an existing BuilderModel circuit model
        :param step: STEAM analysis step of type LoadCircuitParameters, which has attributes:
        - model_name: BuilderModel object to edit - THIS MUST BE OF TYPE CIRCUIT
        - path_file_circuit_parameters: the name of the .csv file containing the circuit parameters
        - selected_circuit_name: name of the circuit name whose parameters will be loaded
        :param verbose: display additional logging info
        :return:
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self
        if verbose: print(f'Load circuit parameters.')

        # Unpack variables
        model_name = step.model_name
        path_file_circuit_parameters = step.path_file_circuit_parameters
        selected_circuit_name = step.selected_circuit_name

        BM = self.list_models[model_name]

        # Call function to load the parameters into the object
        BM.load_circuit_parameters_from_csv(input_file_name=path_file_circuit_parameters,
                                            selected_circuit_name=selected_circuit_name, verbose=verbose)

        # Update the BuilderModel object
        self.list_models[model_name] = BM

        return

    def setup_sim(self, BM: Union[BuilderModel, BuilderCosim], step, sim_number: int, verbose: bool = None):
        """
        Set up a model in the respective local working folder
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        if step.software == 'COSIM':
            BM = self.setup_sim_COSIM(BM=BM, simulation_name=step.simulation_name, sim_number=sim_number, verbose=verbose)
        elif step.software == 'FiQuS':
            BM = self.setup_sim_FiQuS(BM=BM, simulation_name=step.simulation_name, sim_number=sim_number, verbose=verbose)
        elif step.software == 'LEDET':
            BM = self.setup_sim_LEDET(BM=BM, simulation_name=step.simulation_name, sim_number=sim_number,
                                      flag_json=step.flag_json, flag_plot_all=step.flag_plot_all, verbose=verbose)
        elif step.software == 'PSPICE':
            BM = self.setup_sim_PSPICE(BM=BM, simulation_name=step.simulation_name, sim_number=sim_number, verbose=verbose)
        elif step.software == 'SIGMA':
            BM = self.setup_sim_SIGMA(BM=BM, simulation_name=step.simulation_name, sim_number=sim_number,
                                      flag_plot_all=step.flag_plot_all, verbose=verbose)
        elif step.software == 'PyBBQ':
            BM = self.setup_sim_PyBBQ(BM=BM, simulation_name=step.simulation_name, sim_number=sim_number, verbose=verbose)
        elif step.software == 'PyCoSim':
            BM = self.setup_sim_PyCoSim(BM=BM, simulation_name=step.simulation_name, sim_number=sim_number, verbose=verbose)
        elif step.software == 'XYCE':
            BM = self.setup_sim_XYCE(BM=BM, simulation_name=step.simulation_name, sim_number=sim_number, verbose=verbose)
        return BM

    def setup_sim_COSIM(self, BM: BuilderCosim, simulation_name, sim_number, verbose: bool = None):
        """
        Set up a COSIM model in the local COSIM working folder
        Note: The sim_number is assigned to the subfolder name, not to the file name
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        local_COSIM_folder = self._get_local_folder('local_COSIM_folder')
        local_model_folder = os.path.join(local_COSIM_folder, simulation_name)
        BM.buildCOSIM(sim_name=simulation_name, sim_number=sim_number, output_path=local_model_folder, verbose=verbose)

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        return BM

    def setup_sim_FiQuS(self, BM: BuilderModel, simulation_name, sim_number, flag_plot_all: bool = False, verbose: bool = None):
        """
        Set up a FiQuS simulation by copying the last file generated by BuilderModel to the output folder and to the
        local FiQuS working folder.
        The original file is then deleted.
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        local_FiQuS_folder = self._get_local_folder('local_FiQuS_folder')
        BM.buildFiQuS(sim_name=simulation_name, sim_number=sim_number, output_path=os.path.join(local_FiQuS_folder, simulation_name),
                      flag_plot_all=flag_plot_all, verbose=verbose)

        # Make simulation folder
        #local_model_folder = os.path.join(self.settings.local_FiQuS_folder, simulation_name, f'{simulation_name}_{str(sim_number)}')
        local_model_folder = os.path.join(local_FiQuS_folder, simulation_name)
        make_folder_if_not_existing(local_model_folder)
        sources_folder = os.path.join(local_model_folder, 'sources')
        make_folder_if_not_existing(sources_folder)
        output_folder = os.path.join(local_model_folder, 'output')
        make_folder_if_not_existing(output_folder)
        # If we have a roxie_reference file copy across
        file_name = f"{simulation_name}_{sim_number}_ROXIE_REFERENCE.map2d"
        try:
            shutil.copy2(os.path.join(output_folder, file_name), sources_folder)  # Copy
        except:
            print(f"No roxie file {os.path.join(output_folder, file_name)}")

        # Copy simulation file
        file_name_temp = os.path.join(output_folder, f'{simulation_name}_{sim_number}')
        yaml_temp = os.path.join(file_name_temp + '_FiQuS.yaml')
        file_name_local = os.path.join(local_model_folder, f'{simulation_name}_{sim_number}')
        yaml_local = os.path.join(file_name_local + '.yaml')
        try:
            shutil.copyfile(yaml_temp, yaml_local)
        except:
            print(f"No file {yaml_temp}")

        geo_temp = os.path.join(file_name_temp + '_FiQuS.geom')
        set_temp = os.path.join(file_name_temp + '_FiQuS.set')
        geo_local = os.path.join(file_name_local + '.geom')
        set_local = os.path.join(file_name_local + '.set')
        try:
            shutil.copyfile(geo_temp, geo_local)
        except:
            print(f"No file {geo_temp}")
        try:
            shutil.copyfile(set_temp, set_local)
        except:
            print(f"No file {set_temp}")

        if verbose: print(f'Simulation files {file_name_temp} generated.')
        if verbose: print(f'Simulation files {file_name_local} copied.')

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        return BM

    def setup_sim_LEDET(self, BM: BuilderModel, simulation_name: str, sim_number: Union[int, str],
                        flag_json: bool = False, flag_plot_all: bool = False,
                        verbose: bool = None):
        """
        Set up a LEDET simulation by copying the last file generated by BuilderModel to the output folder and to the
        local LEDET working folder. The original file is then deleted.
        If flag_yaml=True, the model is set up to be run using a yaml input file.
        If flag_json=True, the model is set up to be run using a json input file.
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        local_LEDET_folder = self._get_local_folder('local_LEDET_folder')
        local_model_folder = str(Path(local_LEDET_folder / simulation_name / 'Input').resolve())
        field_maps_folder = Path(local_LEDET_folder / '..' / 'Field maps' / simulation_name).resolve()  # The map2d files are written in a subfolder {simulation_name} inside a folder "Field maps" at the same level as the LEDET folder [this structure is hard-coded in STEAM-LEDET]

        make_folder_if_not_existing(Path(local_LEDET_folder / simulation_name / 'Input').resolve(), verbose=verbose)
        make_folder_if_not_existing(Path(local_LEDET_folder / simulation_name / 'Input' / 'Control current input').resolve(), verbose=verbose)
        make_folder_if_not_existing(Path(local_LEDET_folder / simulation_name / 'Input' / 'Initialize variables').resolve(), verbose=verbose)
        make_folder_if_not_existing(Path(local_LEDET_folder / simulation_name / 'Input' / 'InitializationFiles').resolve(), verbose=verbose)

        BM.buildLEDET(sim_name=simulation_name, sim_number=sim_number,
                      output_path=local_model_folder, output_path_field_maps=field_maps_folder,
                      flag_json=flag_json, flag_plot_all=flag_plot_all, verbose=verbose)

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        return BM

    def setup_sim_PSPICE(self, BM: BuilderModel, simulation_name: str, sim_number, verbose: bool = None):
        """
        Set up a PSPICE simulation in the local PSPICE working folder
        Note: The sim_number is assigned to the subfolder name, not to the file name
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        # Write PSPICE netlist
        local_PSPICE_folder = self._get_local_folder('local_PSPICE_folder')

        local_model_folder = os.path.join(local_PSPICE_folder, simulation_name, str(sim_number))
        BM.buildPSPICE(sim_name=simulation_name, sim_number='', output_path=local_model_folder, verbose=verbose)

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        return BM

    def setup_sim_PyCoSim(self, BM: BuilderCosim, simulation_name, sim_number, verbose: bool = None):
        """
        Set up a PyCoSim model in the local PyCoSim working folder
        Note: The sim_number is assigned to the subfolder name, not to the file name
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        local_PyCoSim_folder = self._get_local_folder('local_PyCoSim_folder')
        local_model_folder = os.path.join(local_PyCoSim_folder, simulation_name, 'input')  # TODO TO DISCUSS: MW dislikes 'input', ER likes it
        BM.buildPyCoSim(sim_name=simulation_name, sim_number=sim_number, output_path=local_model_folder, verbose=verbose)

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        return BM

    def setup_sim_SIGMA(self, BM: BuilderModel, simulation_name, sim_number,
                        flag_plot_all: bool = False, verbose: bool = None):
        """
        Set up a SIGMA simulation by copying the last file generated by BuilderModel to the output folder and to the
        local SIGMA working folder.
        The original file is then deleted.
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        local_SIGMA_folder = self._get_local_folder('local_SIGMA_folder')
        local_model_folder = str(Path(local_SIGMA_folder / simulation_name / 'Input').resolve())
        BM.buildPySIGMA(sim_name=simulation_name, sim_number=sim_number,
                        output_path=local_model_folder,
                        flag_plot_all=flag_plot_all,
                        verbose=verbose)

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        return BM

    def setup_sim_XYCE(self, BM: BuilderModel, simulation_name, sim_number, verbose: bool = None):
        """
        Set up a PSPICE simulation by copying the last file generated by BuilderModel to the output folder and to the
        local PSPICE working folder.
        The simulation netlist and auxiliary files are copied in a new numbered subfoldered.
        The original file is then deleted.
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        # Unpack
        local_XYCE_folder = self._get_local_folder('local_XYCE_folder')
        local_model_folder = os.path.join(local_XYCE_folder, simulation_name, str(sim_number))
        BM.buildXYCE(sim_name=simulation_name, sim_number='', output_path=local_model_folder, verbose=verbose)

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        # Edit simulation file
        file_name_local = os.path.join(local_model_folder, simulation_name + '.cir')
        self.copy_XYCE_cir(file_name_local, file_name_local)
        if verbose: print(f'Simulation file {file_name_local} edited.')

        return BM

    def copy_XYCE_cir(self, file_name_temp, file_name_local):
        '''
            Function that copies the XYCE circuit file from 'file_name_temp' to 'file_name_local' and changes the
            respective output path for the csd
        :param file_name_temp: Original circuit file
        :param file_name_local: Final circuit file
        :return:
        '''

        with open(file_name_temp) as f:
            contents = f.readlines()
        for k in range(len(contents)):
            if contents[k].casefold().startswith('.print'):
                if 'csd' in contents[k]:
                    type_output = 'csd'
                elif 'csv' in contents[k]:
                    type_output = 'csv'
                elif 'txt' in contents[k]:
                    type_output = 'txt'
                else:
                    raise Exception("Don't understand output type.")
                print_line = contents[k].split('FILE=')
                print_line[-1] = f'FILE={file_name_local[:-4]}.{type_output} \n'
                contents[k] = ''.join(print_line)
                break

        contents = ''.join(contents)
        new_file = open(file_name_local, 'w')
        new_file.write(contents)
        new_file.close()

    def setup_sim_PyBBQ(self, BM: BuilderModel, simulation_name, sim_number, verbose: bool = None):
        """
        Set up a PyBBQ simulation in the local PyBBQ working folder
        Note: The sim_number is assigned to the subfolder name, not to the file name
        """
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        local_PyBBQ_folder = self._get_local_folder('local_PyBBQ_folder')
        local_model_folder = os.path.join(local_PyBBQ_folder, simulation_name, str(sim_number))
        BM.buildPyBBQ(sim_name=simulation_name, sim_number='', output_path=local_model_folder, verbose=verbose)

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        return BM

    def run_sim(self, software: str, simulation_name: str, sim_number: int, simFileType: str = None,
                verbose: bool = False):
        """
        Run selected simulation.
        The function applies a different logic for each simulation software.
        """
        if software == 'FiQuS':
            local_FiQuS_folder = self._get_local_folder('local_FiQuS_folder')
            #local_analysis_folder = simulation_name + '_' + str(sim_number)
            dFiQuS = DriverFiQuS(FiQuS_path=self.settings.FiQuS_path,
                                 path_folder_FiQuS_output=os.path.join(local_FiQuS_folder, simulation_name),
                                 path_folder_FiQuS_input=os.path.join(local_FiQuS_folder, simulation_name), verbose=verbose,
                                 GetDP_path=self.settings.GetDP_path)
            self.summary = dFiQuS.run_FiQuS(sim_file_name=simulation_name + '_' + str(sim_number) + '_FiQuS', return_summary=False)
        elif software == 'LEDET':
            local_LEDET_folder = self._get_local_folder('local_LEDET_folder')
            dLEDET = DriverLEDET(path_exe=self.settings.LEDET_path, path_folder_LEDET=local_LEDET_folder, verbose=verbose)
            self.summary = dLEDET.run_LEDET(simulation_name, str(sim_number), simFileType=simFileType)
        elif software == 'PSPICE':
            local_PSPICE_folder = self._get_local_folder('local_PSPICE_folder')
            local_model_folder = Path(local_PSPICE_folder / simulation_name / str(sim_number)).resolve()
            dPSPICE = DriverPSPICE(path_exe=self.settings.PSPICE_path, path_folder_PSPICE=local_model_folder, verbose=verbose)
            dPSPICE.run_PSPICE(simulation_name, suffix='')
        elif software == 'PyBBQ':
            local_PyBBQ_folder = self._get_local_folder('local_PyBBQ_folder')
            local_model_folder_input = os.path.join(local_PyBBQ_folder, simulation_name, str(sim_number))
            relative_folder_output = os.path.join(simulation_name, str(sim_number))
            dPyBBQ = DriverPyBBQ(path_exe=self.settings.PyBBQ_path, path_folder_PyBBQ=local_PyBBQ_folder,
                                 path_folder_PyBBQ_input=local_model_folder_input, verbose=verbose)
            dPyBBQ.run_PyBBQ(simulation_name, outputDirectory=relative_folder_output)
        elif software == 'PyCoSim':
            local_PyCoSim_folder = self._get_local_folder('local_PyCoSim_folder')
            local_model_folder = os.path.join(local_PyCoSim_folder, simulation_name, 'input')  # TODO TO DISCUSS: MW dislikes 'input', ER likes it
            pass
            # TODO find a sensible logic for running PyCoSim inside a STEAM analysis: This will be done by calling CosimPyCoSim here
            # path_cosim_data =
            # pyCOSIM = CosimPyCoSim(file_model_data=path_cosim_data, data_settings=self.settings, verbose=verbose)
            # pyCOSIM.run()
        elif software == 'SIGMA':
            local_SIGMA_folder = self._get_local_folder('local_SIGMA_folder')
            local_analysis_folder = os.path.join(local_SIGMA_folder, simulation_name, f'{sim_number}')  # TODO note simulation_name was added
            ds = DriverPySIGMA(path_input_folder=local_analysis_folder)
            ds.run_PySIGMA(simulation_name)
        elif software == 'XYCE':
            local_XYCE_folder = self._get_local_folder('local_XYCE_folder')
            local_model_folder = Path(local_XYCE_folder / simulation_name / str(sim_number)).resolve()
            dXYCE = DriverXYCE(path_exe=self.settings.XYCE_path, path_folder_XYCE=local_model_folder, verbose=verbose)
            dXYCE.run_XYCE(simulation_name, suffix='')
        else:
            raise Exception(f'Software {software} not supported for automated running.')

    def write_stimuli_from_interpolation(self, step, verbose: bool = None):
        '''
        Function to write a resistance stimuli for n apertures of a magnet for any current level. Resistance will be interpolated
        from pre-calculated values (see InterpolateResistance for closer explanation). Stimuli is then written in a .stl file for PSPICE

        :param current_level: list, all current level that shall be used for interpolation (each magnet has 1 current level)
        :param n_total_magnets: int, Number of total magnets in the circuit (A stimuli will be written for each, non-quenching = 0)
        :param n_apertures: int, Number of apertures per magnet. A stimuli will be written for each aperture for each magnet
        :param magnets: list, magnet numbers for which the stimuli shall be written
        :param tShift: list, time shift that needs to be applied to each stimuli
        (e.g. if magnet 1 quenches at 0.05s, magnet 2 at 1s etc.), so that the stimuli are applied at the correct time in the simulation
        :param Outputfile: str, name of the stimuli-file
        :param path_resources: str, path to the file with pre-calculated values
        :param InterpolationType: str, either Linear or Spline, type of interpolation
        :param type_stl: str, how to write the stimuli file (either 'a' (append) or 'w' (write))
        :param sparseTimeStepping: int, every x-th time value only a stimuli point is written (to reduce size of stimuli)
        :return:
        '''
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        # Unpack inputs
        current_level = step.current_level
        n_total_magnets = step.n_total_magnets
        n_apertures = step.n_apertures
        magnets = step.magnets
        tShift = step.t_offset
        Outputfile = step.output_file
        path_resources = step.path_interpolation_file
        InterpolationType = step.interpolation_type
        type_stl = step.type_file_writing
        sparseTimeStepping = step.n_sampling
        magnet_type = step.magnet_types
        # Set default values for selected missing inputs
        if not InterpolationType:
            InterpolationType = 'Linear'
        if not type_stl:
            type_stl = 'w'
        if not sparseTimeStepping:
            sparseTimeStepping = 1  # Note: This will ovrewrite the default value of 100 used in the writeStimuliFromInterpolation_general() function

        # Call coil-resistance interpolation function
        writeStimuliFromInterpolation(current_level, n_total_magnets, n_apertures, magnets, tShift, Outputfile,
                                              path_resources, InterpolationType, type_stl, sparseTimeStepping,
                                              magnet_type)

        if 'XYCE' in Outputfile:
            output_folder_path = os.path.join(self.output_path, 'Stimulus')
            if not os.path.exists(output_folder_path):
                os.makedirs(output_folder_path)
            #self.extract_stimulus_values(Outputfile, output_folder_path)
            translate_stimulus('all', Outputfile, output_folder_path)

        if verbose:
            print(f'Output stimulus file {Outputfile} written.')

    def run_parsim_event(self, step, verbose: bool = None):
        '''
        Function to generate steps based on list of events from external file

        :param step:
        :param verbose: if true displays more information
        :return:
        '''
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        input_file = step.input_file
        simulation_numbers = step.simulation_numbers
        model_name = step.model_name
        case_model = step.case_model
        simulation_name = step.simulation_name
        software = step.software
        t_PC_off = step.t_PC_off
        rel_quench_heater_trip_threshold = step.rel_quench_heater_trip_threshold #
        current_polarities_CLIQ = step.current_polarities_CLIQ
        dict_QH_circuits_to_QH_strips = step.dict_QH_circuits_to_QH_strips
        path_output_viewer_csv = step.path_output_viewer_csv
        path_output_event_csv = step.path_output_event_csv
        default_keys = step.default_keys
        path_postmortem_offline_data_folder = step.path_postmortem_offline_data_folder
        path_to_configurations_folder = step.path_to_configurations_folder
        filepath_to_temp_viewer_csv = step.filepath_to_temp_viewer_csv

        # Resolve path and substitute it
        path_output_from_analysis_file = default_keys.path_output  # TODO this is a workaround (see "default_keys.path_output = path_output_from_analysis_file")
        default_keys.path_output = str(self._get_local_folder(f'local_{software}_folder'))

        # Check inputs
        if not path_output_viewer_csv:
            path_output_viewer_csv = ''
            if verbose: print(f'Key "path_output_viewer_csv" was not defined in the STEAM analysis file: no output viewer files will be generated.')
        # if type(path_output_viewer_csv) == str:
        #     path_output_viewer_csv = [path_output_viewer_csv]  # Make sure this variable is always a list
        # if path_output_viewer_csv and len(path_output_viewer_csv) > 1:
        #     raise Exception(f'The length of path_output_viewer_csv must be 1, but it is {len(path_output_viewer_csv)}.')
        if path_output_viewer_csv and default_keys == {}:
            raise Exception(f'When key "path_output_viewer_csv" is defined in the STEAM analysis file, key "default_keys" must also be defined.')

        # Paths to output file
        if not path_output_event_csv:
            raise Exception('File path path_output_event_csv must be defined for an analysis step of type ParsimEvent.')

        # Read input file and run the ParsimEvent analysis
        if case_model == 'magnet':
            pem = ParsimEventMagnet(ref_model=self.list_models[model_name], verbose=verbose)
            pem.read_from_input(path_input_file=input_file, flag_append=False, rel_quench_heater_trip_threshold=rel_quench_heater_trip_threshold)
            pem.write_event_file(simulation_name=simulation_name, simulation_numbers=simulation_numbers,
                                 t_PC_off=t_PC_off, path_outputfile_event_csv=path_output_event_csv,
                                 current_polarities_CLIQ=current_polarities_CLIQ,
                                 dict_QH_circuits_to_QH_strips=dict_QH_circuits_to_QH_strips)

            # start parsim sweep step with newly created event file
            parsim_sweep_step = ParametricSweep(type='ParametricSweep', input_sweep_file=path_output_event_csv,
                                                model_name=model_name, case_model=case_model, software=software, verbose=verbose)
            self.run_parsim_sweep(parsim_sweep_step, verbose=verbose)

            # TODO: merge list and dict into self.data_analysis
            # TODO: add flag_show_parsim_output ?
            # TODO: add flag to write yaml analysis with all steps
            # TODO: parse Conductor Data - but what are the names in Quenchdict? (Parsim Sweep can handly conductor changes)

            # Write a .csv file that can be used to run a STEAM Viewer analysis
            if path_output_viewer_csv:
                default_keys.path_output = path_output_from_analysis_file  #TODO this is a workaround (See "path_output_from_analysis_file = default_keys.path_output")
                pem.set_up_viewer(path_output_viewer_csv, default_keys, simulation_numbers, simulation_name, software)
                if verbose: print(f'File {path_output_viewer_csv} written. It can be used to run a STEAM Viewer analysis.')
        elif case_model == 'circuit':
            # Read input file and run the ParsimEvent analysis
            pec = ParsimEventCircuit(ref_model=self.list_models[model_name], library_path=self.library_path, verbose=verbose)
            pec.read_from_input(path_input_file=input_file, flag_append=False)
            if simulation_name in ["RQ_47magnets", "RQ_51magnets", "RCBX"]:
                simulation_numbers = [0 + simulation_numbers[-1], 1 + simulation_numbers[-1]]
                self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_numbers = simulation_numbers
            pec.write_event_file(simulation_name=simulation_name, simulation_numbers=simulation_numbers,
                                 path_outputfile_event_csv=path_output_event_csv)

            quenching_magnet_list = []  # required for families where multiple magnets can quench like RB
            quenching_magnet_time = []
            quenching_current_list = []
            for event_number in range(len(pec.list_events)):  # reading through each row of the event file
                # get circuit specific information
                circuit_name = pec.list_events[event_number].GeneralParameters.name
                circuit_family_name = get_circuit_family_from_circuit_name(circuit_name, self.library_path)
                circuit_type = get_circuit_type_from_circuit_name(circuit_name, self.library_path, simulation_name)
                magnet_name = get_magnet_name(circuit_name,simulation_name,circuit_type)
                number_of_magnets = get_number_of_magnets(circuit_name,simulation_name,circuit_type,circuit_family_name)
                number_of_apertures = get_number_of_apertures_from_circuit_family_name(circuit_family_name)
                if circuit_family_name == "RB":
                    current_level = pec.list_events[event_number].QuenchEvents[circuit_name].current_at_quench
                    t_PC_off = pec.list_events[0].PoweredCircuits[circuit_name].delta_t_FGC_PIC
                else:
                    current_level = pec.list_events[event_number].PoweredCircuits[circuit_name].current_at_discharge
                    t_PC_off = pec.list_events[event_number].PoweredCircuits[circuit_name].delta_t_FGC_PIC
                magnets_list = self.__get_magnets_list(number_of_magnets)
                assert(simulation_name==self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_name)
                magnet_types = get_magnet_types_list(number_of_magnets, simulation_name)

                # load circuit parameters step
                if circuit_family_name == "RQ":
                    circuit_name_1 = circuit_name.replace(".", "D_")
                    circuit_name_2 = circuit_name.replace(".", "F_")
                    load_circuit_parameters_step_1 = LoadCircuitParameters(type='LoadCircuitParameters', model_name=model_name, path_file_circuit_parameters=os.path.join(self.library_path, f"circuits/circuit_parameters/{circuit_family_name}_circuit_parameters.csv"), selected_circuit_name=circuit_name_1)
                    load_circuit_parameters_step_2 = LoadCircuitParameters(type='LoadCircuitParameters', model_name=model_name, path_file_circuit_parameters=os.path.join(self.library_path, f"circuits/circuit_parameters/{circuit_family_name}_circuit_parameters.csv"), selected_circuit_name=circuit_name_2)
                    position = pec.list_events[event_number].QuenchEvents[circuit_name].magnet_electrical_position
                    quenching_magnet = [get_number_of_quenching_magnets_from_layoutdetails(position, circuit_family_name,library_path=self.library_path)]
                    # modify model diode step used to change diodes across the quenching magnets with heating
                    modify_model_diode_step = ModifyModel(type='ModifyModel', model_name=model_name, variable_to_change=f'Netlist[x_D{quenching_magnet[0]}].value', variable_value=[
                        "RQ_Protection_Diode"], simulation_numbers=[], simulation_name=simulation_name, software=software)
                elif circuit_type == "RCBX":
                    circuit_name_1 = circuit_name.replace("X", "XH")
                    circuit_name_2 = circuit_name.replace("X", "XV")
                    load_circuit_parameters_step_1 = LoadCircuitParameters(type='LoadCircuitParameters', model_name=model_name, path_file_circuit_parameters=os.path.join(self.library_path, f"circuits/circuit_parameters/{circuit_family_name}_circuit_parameters.csv"), selected_circuit_name=circuit_name_1)
                    load_circuit_parameters_step_2 = LoadCircuitParameters(type='LoadCircuitParameters', model_name=model_name, path_file_circuit_parameters=os.path.join(self.library_path, f"circuits/circuit_parameters/{circuit_family_name}_circuit_parameters.csv"), selected_circuit_name=circuit_name_2)
                elif circuit_type in ["RCD", "RCO"]:
                    if "-" in circuit_name:
                        parts = circuit_name.split("-")
                        last_part = parts[-1]
                        circuit_name_RCD = parts[0] + "." + last_part.split(".")[1]
                        circuit_name_RCO = last_part
                    elif "." in circuit_name:
                        circuit_name_RCD = circuit_name.replace(".", "D.", 1)
                        circuit_name_RCO = circuit_name.replace(".", "O.", 1)
                    temp_circuit_name = circuit_name_RCD if circuit_type == "RCD" else circuit_name_RCO
                    load_circuit_parameters_step = LoadCircuitParameters(type='LoadCircuitParameters', model_name=model_name, path_file_circuit_parameters=os.path.join(self.library_path, f"circuits/circuit_parameters/{circuit_family_name}_circuit_parameters.csv"), selected_circuit_name=temp_circuit_name)
                elif circuit_family_name == "RB":
                    if event_number == len(pec.list_events) - 1:
                        load_circuit_parameters_step = LoadCircuitParameters(type='LoadCircuitParameters', model_name=model_name, path_file_circuit_parameters=os.path.join(self.library_path, f"circuits/circuit_parameters/{circuit_family_name}_circuit_parameters.csv"), selected_circuit_name=circuit_name)
                else:
                    load_circuit_parameters_step = LoadCircuitParameters(type='LoadCircuitParameters', model_name=model_name, path_file_circuit_parameters=os.path.join(self.library_path, f"circuits/circuit_parameters/{circuit_family_name}_circuit_parameters.csv"), selected_circuit_name=circuit_name)

                # choosing stimulus output file location
                if circuit_family_name == "IPD":
                    stimulus_output_file = os.path.join(default_keys.path_output, f'{circuit_family_name}', f"{self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_numbers[0]}", 'coil_resistances.stl')
                elif circuit_family_name == "RQ":
                    stimulus_output_file_1 = os.path.join(default_keys.path_output, f'{circuit_type}', f"{self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_numbers[0]}", 'coil_resistances.stl')
                    stimulus_output_file_2 = os.path.join(default_keys.path_output, f'{circuit_type}', f"{self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_numbers[1]}", 'coil_resistances.stl')
                elif circuit_type == "RCBX":
                    stimulus_output_file_1 = os.path.join(default_keys.path_output, 'RCBX', f"{self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_numbers[0]}", 'coil_resistances.stl')
                    stimulus_output_file_2 = os.path.join(default_keys.path_output, 'RCBX', f"{self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_numbers[1]}", 'coil_resistances.stl')
                elif simulation_name.startswith("IPQ"):
                    stimulus_output_file = os.path.join(default_keys.path_output, f'{simulation_name}', f"{self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_numbers[0]}", 'coil_resistances.stl')
                elif circuit_name.startswith("RCBY"):
                    stimulus_output_file = os.path.join(default_keys.path_output, 'RCBY', f"{self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_numbers[0]}", 'coil_resistances.stl')
                elif circuit_name.startswith(("RCBH", "RCBV")):
                    stimulus_output_file = os.path.join(default_keys.path_output, 'RCB', f"{self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_numbers[0]}", 'coil_resistances.stl')
                elif circuit_type == "RB":
                    if event_number == len(pec.list_events) - 1:
                        stimulus_output_file = os.path.join(default_keys.path_output, f'{circuit_type}', f"{self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_numbers[0]}", 'coil_resistances.stl')
                elif circuit_name.startswith("RQS.A"):
                    stimulus_output_file = os.path.join(default_keys.path_output, 'RQS_AxxBx', f"{self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_numbers[0]}", 'coil_resistances.stl')
                elif circuit_name.startswith(("RQS.R", "RQS.L")):
                    stimulus_output_file = os.path.join(default_keys.path_output, 'RQS_R_LxBx', f"{self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_numbers[0]}", 'coil_resistances.stl')
                else:
                    stimulus_output_file = os.path.join(default_keys.path_output, f'{circuit_type}', f"{self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_numbers[0]}", 'coil_resistances.stl')

                # making appropriate directory if it doesn't exist for the stimulus output file
                if circuit_family_name == "RQ" or circuit_type == "RCBX":
                    for file_path in [stimulus_output_file_1, stimulus_output_file_2]:
                        directory = os.path.dirname(file_path)
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                else:
                    if circuit_family_name == "RB":
                        if event_number == len(pec.list_events) - 1:
                            directory = os.path.dirname(stimulus_output_file)
                            if not os.path.exists(directory):
                                os.makedirs(directory)
                    else:
                        directory = os.path.dirname(stimulus_output_file)
                        if not os.path.exists(directory):
                            os.makedirs(directory)

                # write stimulus file step
                if circuit_family_name == "RQ":
                    if pec.list_events[event_number].QuenchEvents[circuit_name].quench_cause == "No quench":
                        current_level = [0]*len(quenching_magnet)
                    write_stimuli_file_step_1 = WriteStimulusFile(type='WriteStimulusFile', output_file=stimulus_output_file_1, path_interpolation_file=[os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name}.csv')], n_total_magnets=number_of_magnets, n_apertures=number_of_apertures, current_level=[current_level[0]], magnets=quenching_magnet, t_offset=[t_PC_off], interpolation_type='Linear', type_file_writing='w', n_sampling=100, magnet_types=magnet_types)
                    write_stimuli_file_step_2 = WriteStimulusFile(type='WriteStimulusFile', output_file=stimulus_output_file_2, path_interpolation_file=[os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name}.csv')], n_total_magnets=number_of_magnets, n_apertures=number_of_apertures, current_level=[current_level[0]], magnets=quenching_magnet, t_offset=[t_PC_off], interpolation_type='Linear', type_file_writing='w', n_sampling=100, magnet_types=magnet_types)
                elif circuit_type == "RCBX":
                    if pec.list_events[event_number].QuenchEvents[circuit_name].quench_cause == "No quench":
                        current_level = [0, 0]
                    write_stimuli_file_step_1 = WriteStimulusFile(type='WriteStimulusFile', output_file=stimulus_output_file_1, path_interpolation_file=[os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[0]}.csv')], n_total_magnets=number_of_magnets, n_apertures=number_of_apertures, current_level=[abs(current_level[0])], magnets=magnets_list, t_offset=[t_PC_off[0]], interpolation_type='Linear', type_file_writing='w', n_sampling=1, magnet_types=magnet_types)
                    write_stimuli_file_step_2 = WriteStimulusFile(type='WriteStimulusFile', output_file=stimulus_output_file_2, path_interpolation_file=[os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[1]}.csv')], n_total_magnets=number_of_magnets, n_apertures=number_of_apertures, current_level=[abs(current_level[1])], magnets=magnets_list, t_offset=[t_PC_off[1]], interpolation_type='Linear', type_file_writing='w', n_sampling=1, magnet_types=magnet_types)
                elif circuit_family_name == "RQX":
                    if pec.list_events[event_number].QuenchEvents[circuit_name].quench_cause == "No quench":
                        current_level = [0] * len(magnets_list)
                    current_level = [current_level[0]+current_level[1], current_level[0]+current_level[2], current_level[0]+current_level[2], current_level[0]] #see schematic
                    write_stimuli_file_step = WriteStimulusFile(type='WriteStimulusFile', output_file=stimulus_output_file, path_interpolation_file=[os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[0]}.csv'), os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[1]}.csv')], n_total_magnets=number_of_magnets, n_apertures=number_of_apertures, current_level=current_level, magnets=magnets_list, t_offset=[t_PC_off]*number_of_magnets, interpolation_type='Linear', type_file_writing='w', n_sampling=1, magnet_types=magnet_types)
                elif circuit_family_name == "IPQ" and number_of_magnets == 2:
                    if pec.list_events[event_number].QuenchEvents[circuit_name].quench_cause == "No quench":
                        current_level = [0] * len(magnets_list)
                    write_stimuli_file_step = WriteStimulusFile(type='WriteStimulusFile', output_file=stimulus_output_file, path_interpolation_file=[os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[0]}.csv'), os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[1]}.csv')], n_total_magnets=number_of_magnets, n_apertures=number_of_apertures, current_level=current_level, magnets=magnets_list, t_offset=[t_PC_off]*number_of_magnets, interpolation_type='Linear', type_file_writing='w', n_sampling=1, magnet_types=magnet_types)
                elif circuit_family_name == "IPQ" and number_of_magnets == 1:
                    if pec.list_events[event_number].QuenchEvents[circuit_name].quench_cause == "No quench":
                        current_level = [0] * len(magnets_list)
                    write_stimuli_file_step = WriteStimulusFile(type='WriteStimulusFile', output_file= stimulus_output_file, path_interpolation_file=[os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name}.csv')], n_total_magnets=number_of_magnets, n_apertures=number_of_apertures, current_level=[current_level[0]], magnets=magnets_list, t_offset=[t_PC_off], interpolation_type='Linear', type_file_writing='w', n_sampling=1, magnet_types=magnet_types)
                elif circuit_type in ["RCS", "RO_13magnets", "RO_8magnets", "RSD_12magnets", "RSD_11magnets", "RSF_10magnets", "RSF_9magnets", "RQTL9", "RQT"] or (circuit_type == "RQ6" and circuit_family_name == "600A") or circuit_name.startswith("RQS.A"):
                    if pec.list_events[event_number].QuenchEvents[circuit_name].quench_cause == "No quench":
                        current_level = 0
                    write_stimuli_file_step = WriteStimulusFile(type='WriteStimulusFile', output_file=stimulus_output_file, path_interpolation_file=[os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[0]}.csv'), os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[1]}.csv')], n_total_magnets=number_of_magnets, n_apertures=number_of_apertures, current_level=[abs(current_level)]*number_of_magnets, magnets=magnets_list, t_offset=[t_PC_off[0]]*number_of_magnets, interpolation_type='Linear', type_file_writing='w', n_sampling=1, magnet_types=magnet_types)
                elif circuit_name.startswith(("RQS.R", "RQS.L", "RSS")):
                    if pec.list_events[event_number].QuenchEvents[circuit_name].quench_cause == "No quench":
                        current_level = 0
                    write_stimuli_file_step = WriteStimulusFile(type='WriteStimulusFile', output_file=stimulus_output_file, path_interpolation_file=[os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[0]}.csv'), os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[1]}.csv')], n_total_magnets=number_of_magnets, n_apertures=number_of_apertures, current_level=[abs(current_level)]*number_of_magnets, magnets=magnets_list, t_offset=[t_PC_off]*number_of_magnets, interpolation_type='Linear', type_file_writing='w', n_sampling=1, magnet_types=magnet_types)
                elif circuit_type == "RB":
                    position = pec.list_events[event_number].QuenchEvents[circuit_name].magnet_electrical_position
                    quenching_magnet = [get_number_of_quenching_magnets_from_layoutdetails(position, circuit_family_name,library_path=self.library_path)]
                    quenching_magnet_list.append(quenching_magnet[0])
                    quenching_magnet_time.append(pec.list_events[event_number].QuenchEvents[circuit_name].delta_t_iQPS_PIC)
                    quenching_current_list.append(current_level)
                    # modify model diode step used to change diodes across the quenching magnets with heating
                    modify_model_diode_step = ModifyModel(type='ModifyModel', model_name=model_name, variable_to_change=f'Netlist[x_D{quenching_magnet[0]}].value', variable_value=[
                        "RB_Protection_Diode"], simulation_numbers=[], simulation_name=simulation_name, software=software)
                    if event_number == len(pec.list_events) - 1:
                        zipped_lists = zip(quenching_magnet_list, quenching_magnet_time, quenching_current_list)
                        sorted_lists = sorted(zipped_lists, key=lambda x: x[0])
                        quenching_magnet_list, quenching_magnet_time, quenching_current_list = zip(*sorted_lists)
                        if pec.list_events[event_number].QuenchEvents[circuit_name].quench_cause == "No quench":
                            quenching_current_list = [0]*len(quenching_current_list)
                        write_stimuli_file_step = WriteStimulusFile(type='WriteStimulusFile', output_file=stimulus_output_file, path_interpolation_file=[os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name}.csv')], n_total_magnets=number_of_magnets, n_apertures=number_of_apertures, current_level=quenching_current_list, magnets=quenching_magnet_list, t_offset=quenching_magnet_time, interpolation_type='Linear', type_file_writing='w', n_sampling=100, magnet_types=magnet_types)
                elif circuit_type == "RCD":
                    if pec.list_events[event_number].QuenchEvents[circuit_name].quench_cause == "No quench":
                        current_level = [0, 0]
                    # write_stimuli_file_step = WriteStimulusFile(type='WriteStimulusFile', output_file= stimulus_output_file, path_interpolation_file=[os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[0]}.csv'), os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[1]}.csv')], n_total_magnets=number_of_magnets, n_apertures=number_of_apertures, current_level=[abs(current_level[1])]*number_of_magnets, magnets=magnets_list, t_offset=[t_PC_off[0]]*number_of_magnets, interpolation_type='Linear', type_file_writing='w', n_sampling=1, magnet_types=magnet_types)
                    n_required_coil_resistance_signals = 2
                    magnets_list = [1, 2]
                    magnet_types = [1, 2]
                    write_stimuli_file_step = WriteStimulusFile(type='WriteStimulusFile', output_file= stimulus_output_file, path_interpolation_file=[os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[0]}.csv'), os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[1]}.csv')], n_total_magnets=n_required_coil_resistance_signals, n_apertures=number_of_apertures, current_level=[abs(current_level[1])]*n_required_coil_resistance_signals, magnets=magnets_list, t_offset=[t_PC_off[0]]*n_required_coil_resistance_signals, interpolation_type='Linear', type_file_writing='w', n_sampling=1, magnet_types=magnet_types)
                elif circuit_type == "RCO":
                    if pec.list_events[event_number].QuenchEvents[circuit_name].quench_cause == "No quench":
                        current_level = [0, 0]
                    # write_stimuli_file_step = WriteStimulusFile(type='WriteStimulusFile', output_file= stimulus_output_file, path_interpolation_file=[os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[0]}.csv'), os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[1]}.csv')], n_total_magnets=number_of_magnets, n_apertures=number_of_apertures, current_level=[abs(current_level[0])]*number_of_magnets, magnets=magnets_list, t_offset=[t_PC_off[0]]*number_of_magnets, interpolation_type='Linear', type_file_writing='w', n_sampling=1, magnet_types=magnet_types)
                    n_required_coil_resistance_signals = 2
                    magnets_list = [1, 2]
                    magnet_types = [1, 2]
                    write_stimuli_file_step = WriteStimulusFile(type='WriteStimulusFile', output_file= stimulus_output_file, path_interpolation_file=[os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[0]}.csv'), os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name[1]}.csv')], n_total_magnets=n_required_coil_resistance_signals, n_apertures=number_of_apertures, current_level=[abs(current_level[0])]*n_required_coil_resistance_signals, magnets=magnets_list, t_offset=[t_PC_off[0]]*n_required_coil_resistance_signals, interpolation_type='Linear', type_file_writing='w', n_sampling=1, magnet_types=magnet_types)
                else:
                    if pec.list_events[event_number].QuenchEvents[circuit_name].quench_cause == "No quench":
                        current_level = 0
                    write_stimuli_file_step = WriteStimulusFile(type='WriteStimulusFile', output_file= stimulus_output_file, path_interpolation_file=[os.path.join(self.library_path,'circuits','coil_resistances_to_interpolate',f'interpolation_resistance_{magnet_name}.csv')], n_total_magnets=number_of_magnets, n_apertures=number_of_apertures, current_level=[abs(current_level)], magnets=magnets_list, t_offset=[t_PC_off], interpolation_type='Linear', type_file_writing='w', n_sampling=1, magnet_types=magnet_types)

                # parsim sweep step with newly created event file
                if circuit_family_name == "RQ" or circuit_type == "RCBX":
                    output_files = create_two_csvs_from_odd_and_even_rows(path_output_event_csv)
                    parsim_sweep_step_1 = ParametricSweep(type='ParametricSweep', input_sweep_file=output_files[0],
                                                        model_name=model_name, case_model=case_model, software=software, verbose=verbose)
                    parsim_sweep_step_2 = ParametricSweep(type='ParametricSweep', input_sweep_file=output_files[1],
                                                        model_name=model_name, case_model=case_model, software=software, verbose=verbose)
                else:
                    if circuit_family_name == "RB":
                        if event_number == len(pec.list_events) - 1:
                            parsim_sweep_step = ParametricSweep(type='ParametricSweep',
                                                                input_sweep_file=path_output_event_csv,
                                                                model_name=model_name, case_model=case_model,
                                                                software=software, verbose=verbose)
                    else:
                        parsim_sweep_step = ParametricSweep(type='ParametricSweep', input_sweep_file=path_output_event_csv,
                                                            model_name=model_name, case_model=case_model, software=software, verbose=verbose)


                # run all the steps together
                if circuit_family_name == "RQ":
                    # Note: RQ circuits do not have the generic crowbar, so there's no need to reverse it for numerical
                    # stability in this case. See reverse_crowbar() function for more details.

                    self.load_circuit_parameters(load_circuit_parameters_step_1, verbose=verbose)
                    self.write_stimuli_from_interpolation(write_stimuli_file_step_1, verbose=verbose)
                    self.step_modify_model(modify_model_diode_step, verbose=verbose)
                    self.run_parsim_sweep(parsim_sweep_step_1, verbose=verbose)
                    self.load_circuit_parameters(load_circuit_parameters_step_2, verbose=verbose)
                    self.write_stimuli_from_interpolation(write_stimuli_file_step_2, verbose=verbose)
                    self.step_modify_model(modify_model_diode_step, verbose=verbose)
                    self.run_parsim_sweep(parsim_sweep_step_2, verbose=verbose)
                elif circuit_type == "RCBX":
                    # Note: For RCBX, crowbar reversal is necessary for both RCBXH and RCBXV circuits if needed.
                    # See reverse_crowbar() function for more details.

                    self.load_circuit_parameters(load_circuit_parameters_step_1, verbose=verbose)
                    self.write_stimuli_from_interpolation(write_stimuli_file_step_1, verbose=verbose)
                    self.reverse_crowbar(temp_current_level = current_level[0],model_name = model_name,
                                         simulation_name = simulation_name, software = software, verbose = verbose)
                    self.run_parsim_sweep(parsim_sweep_step_1, verbose=verbose)
                    self.load_circuit_parameters(load_circuit_parameters_step_2, verbose=verbose)
                    self.write_stimuli_from_interpolation(write_stimuli_file_step_2, verbose=verbose)

                    # The crowbar remains reversed in the model for RCBXV if it was reversed for RCBXH.
                    # If the signs of the current levels of RCBXH and RCBXV are opposite, the crowbar needs to be
                    # reverted to its original position for the simulation of RCBXV.
                    if current_level[1] * current_level[0] < 0: # Signs of current levels are different. This could mean the first current level is <0 or the second,
                        # but not both. In either case, we have to reverse the direction of the crowbar, either to adapt to
                        # the negative current for RCBXV or to turn it back in the positive direction after it was reversed
                        # for the simulation of RCBXH.
                        self.reverse_crowbar(temp_current_level = -1 ,model_name = model_name, #hard coded negative current level to force the reversal in such case
                                             simulation_name = simulation_name, software = software, verbose = verbose)
                    self.run_parsim_sweep(parsim_sweep_step_2, verbose=verbose)
                elif circuit_type == "RB":
                    self.step_modify_model(modify_model_diode_step, verbose=verbose)  # diode is changed for each row of the event file
                    if event_number == len(pec.list_events)-1:  # the simulation runs correctly only at the end
                        self.load_circuit_parameters(load_circuit_parameters_step, verbose=verbose)
                        self.write_stimuli_from_interpolation(write_stimuli_file_step, verbose=verbose)
                        #Note: RB circuits do not have the generic crowbar, so we do not have to reverse it here as for RCBX
                        self.run_parsim_sweep(parsim_sweep_step, verbose=verbose)
                else:
                    self.load_circuit_parameters(load_circuit_parameters_step, verbose=verbose)
                    self.write_stimuli_from_interpolation(write_stimuli_file_step, verbose=verbose)

                    # Reverse the crowbar if needed. See reverse_crowbar() function for more details.
                    # RCD/RCO events are a special case here - it is a double circuit like RCBX or RQs, but it is the only case
                    # where analysis stream is called twice for them.
                    temp_current_level = current_level[1] if circuit_type == "RCD" else current_level[
                        0] if circuit_type == "RCO" else current_level # either RCD/RCO event or a circuit where the current level is an integer
                    self.reverse_crowbar(temp_current_level=temp_current_level, model_name=model_name,
                                         simulation_name=simulation_name, software=software, verbose=verbose)

                    self.run_parsim_sweep(parsim_sweep_step, verbose=verbose)

                # write an input file for the viewer here:
                # file will by default be saved in the simulation folder
                if path_postmortem_offline_data_folder:
                    if software == "XYCE":
                        temp_working_directory = self.data_analysis.PermanentSettings.local_XYCE_folder
                    elif software == "PSPICE":
                        temp_working_directory = self.data_analysis.PermanentSettings.local_PSPICE_folder
                    else:
                        temp_working_directory = "None"

                    unique_identifier = generate_unique_event_identifier_from_eventfile(os.path.basename(input_file),
                                                                                        verbose=True)
                    write_config_file_for_viewer(circuit_type = circuit_type, simulation_numbers = simulation_numbers,
                                                 circuit_name = circuit_name, circuit_family = circuit_family_name,
                                                 t_PC_off = t_PC_off, path_to_configurations_folder = path_to_configurations_folder,
                                                 temp_working_directory = temp_working_directory, path_postmortem_offline_data_folder = path_postmortem_offline_data_folder,
                                     unique_identifier = unique_identifier, filepath_to_temp_viewer_csv = filepath_to_temp_viewer_csv)
        else:
            raise Exception(f'case_model {case_model} not supported by ParsimEvent.')

        if verbose:
            print(f'ParsimEvent called using input file {input_file}.')

    def reverse_crowbar(self, temp_current_level, model_name, simulation_name, software, verbose: bool = None):
        """Inverts crowbar polarity if the 'generic_crowbar' component is used and the circuit current is negative.

        Args:
            temp_current_level (float): The current level of the circuit.
            model_name (str): Name of the model.
            simulation_name (str): Name of the simulation.
            software (str): Software used for simulation.
            verbose (bool): If True, prints detailed information about the process.

        Returns:
            None

        Notes:
            This function detects if the 'generic_crowbar' component is present in the circuit
            and inverts its nodes if the circuit current is negative. It then modifies the model
            to reflect this change. This step may need improvement in future versions, but its for now needed,
            because back to back crowbars (like we would want them in the circuit) right now lead to numerical
            instabilities.

        """
        #TODO improve the crowbar model to cope better with this case

        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        for component_name, component_info in self.list_models[model_name].circuit_data.Netlist.items():
            if component_info.type == 'parametrized component' and component_info.value == 'generic_crowbar':
                if temp_current_level < 0:
                    original_nodes = component_info.nodes
                    modify_model_crowbar_step = ModifyModel(type='ModifyModel', model_name=model_name,
                                                            variable_to_change=f'Netlist[{component_name}].nodes',
                                                            variable_value=[[original_nodes[1], original_nodes[0]]],
                                                            simulation_numbers=[], simulation_name=simulation_name,
                                                            software=software)
                    self.step_modify_model(modify_model_crowbar_step, verbose=verbose)
                    if verbose: print(
                        f'Component {component_name} was a subtrack "generic_crowbar" and its current was negative, so its nodes were inverted.')

    def run_parsim_conductor(self, step, verbose: bool = None):
        '''
        Function to generate steps to change the conductor data of a magnet using a csv database

        :param step: instance of ParsimConductor step
        :param verbose: if true displays more information
        '''
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        # Unpack inputs
        model_name = step.model_name
        case_model = step.case_model
        magnet_name = step.magnet_name
        software = step.software
        groups_to_coils = step.groups_to_coils
        length_to_coil = step.length_to_coil
        if not length_to_coil: length_to_coil = {}  # optimize coillen
        simulation_number = step.simulation_number
        input_file = step.input_file
        path_output_sweeper_csv = step.path_output_sweeper_csv
        strand_critical_current_measurements = step.strand_critical_current_measurements

        # check if crucial variables are not None
        if not path_output_sweeper_csv:
            raise Exception('File path path_output_event_csv must be defined for an analysis step of type ParsimEvent.')
        if not input_file:
            raise Exception('File path path_output_event_csv must be defined for an analysis step of type ParsimEvent.')

        # check if all groups are defined in the group dictionaries
        highest_group_index = max([max(values) for values in groups_to_coils.values()])
        expected_group_numbers = list(range(1, highest_group_index + 1))
        all_group_numbers_in_dict = [num for sublist in groups_to_coils.values() for num in sublist]
        if sorted(all_group_numbers_in_dict) != expected_group_numbers:
            raise Exception(f'Invalid groups_to_coils entry in step definition. \nSorted groups given by the user: {sorted(all_group_numbers_in_dict)}')

        # make a copy of the respective conductor for every coil and store it in the magnet model
        # NOTE: if a coil consists of 2 different conductors the user has to treat them as 2 different coils (so a coil is not always a coil but rather a subcoil with the same conductor)
        new_conductors = [None] * len(groups_to_coils)
        dict_coilname_to_conductorindex = {}
        new_conductor_to_group = [None] * len(self.list_models[model_name].model_data.CoilWindings.conductor_to_group)
        for idx, (coil_name, group_numbers) in enumerate(groups_to_coils.items()):
            # store the conductor indices of the groups that make up this coil
            conductor_indices = [self.list_models[model_name].model_data.CoilWindings.conductor_to_group[i-1] for i in group_numbers]

            # check if all the groups in the coil have the same conductor
            if len(set(conductor_indices)) != 1:
                raise Exception(f'Not every group in the coil {coil_name} has the same conductor. \n'
                                f'If a coil consists of more then one conductor it has to be treated like 2 separate coils.')
            else:
                # make a copy of the Conductor for this coil and overwrite the name
                # since all the entries in conductor_indices are the same, conductor_indices[0] can be used
                new_conductors[idx] = deepcopy(self.list_models[model_name].model_data.Conductors[conductor_indices[0]-1])
                new_conductors[idx].name = f'conductor_{coil_name}'

            # store what coilname belongs to what conductor index to later check in database
            dict_coilname_to_conductorindex[coil_name] = idx

            # change the entries in conductor_to_group with the new Conductor
            for group_number in group_numbers:
                new_conductor_to_group[group_number-1] = idx+1

        # check if all the values could be written
        if None in new_conductors or None in new_conductor_to_group:
            raise Exception(f'The given groups_to_coils did not contain all the group indices (1-{len(new_conductor_to_group)})!')

        # overwrite the information in the DataModelMagnet instance of the BuilderModel
        self.list_models[model_name].model_data.Conductors = new_conductors
        self.list_models[model_name].model_data.CoilWindings.conductor_to_group = new_conductor_to_group
        # NOTE: so far no parameters of the model_data were altered, just copies of the conductor have been made and connected to the specified groups
        del new_conductors, new_conductor_to_group


        if case_model == 'magnet':
            # create instance of ParsimConductor
            pc = ParsimConductor(verbose=verbose, model_data=self.list_models[model_name].model_data,
                                 dict_coilName_to_conductorIndex=dict_coilname_to_conductorindex,
                                 groups_to_coils=groups_to_coils, length_to_coil=length_to_coil,
                                 path_input_dir=Path(self.list_models[step.model_name].file_model_data).parent)
            # read the conductor database
            pc.read_from_input(path_input_file=input_file, magnet_name=magnet_name,
                               strand_critical_current_measurements=strand_critical_current_measurements)
            # write a sweeper csv file
            pc.write_conductor_parameter_file(path_output_file=path_output_sweeper_csv, simulation_name=model_name, # TODO simulation_name should be step variable in definition, model_name ist not step name?
                                              simulation_number=simulation_number)

            # create parsim sweep step with newly created sweeper csv file and run it
            parsim_sweep_step = ParametricSweep(type='ParametricSweep', input_sweep_file=path_output_sweeper_csv, # TODO rename teh class to ParametricSweepStep? ParsimConductor is no step class and ParametricSweep is
                                                model_name=model_name, case_model=case_model, software=software, verbose=verbose)
            self.run_parsim_sweep(parsim_sweep_step, verbose=verbose, revert=False)
        else:
            raise Exception(f'Case_model "{case_model}" not supported by ParsimConductor.')

    def run_parsim_sweep(self, step, verbose: bool = None, revert: bool = True):
        '''
        Function to generate steps based on list of models read from external file
        :param step:
        :param revert: if true the changes to the BM object are reverted after setting up the simulation files row by row
        '''
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        # Unpack inputs
        input_sweep_file = step.input_sweep_file
        default_model_name = step.model_name
        case_model = step.case_model
        software = step.software
        verbose = step.verbose

        # read input sweeper file
        self.input_parsim_sweep_df = pd.read_csv(input_sweep_file)

        # loop through every row and run ModifyMultipleVariables step for every row (=event)
        for i, row in self.input_parsim_sweep_df.iterrows():
            # check if model_name is provided in sweeper. csv file - if not use the default one
            if 'simulation_name' in row and row['simulation_name'] in self.list_models:
                # use sweeper model_name only if model_name is existing in list_models
                model_name = row['simulation_name']
                if verbose: print(f'row {i + 1}: Using model {model_name} as specified in the input file {input_sweep_file}.')
            else:
                model_name = default_model_name
                if verbose: print(f'row {i + 1}: Using default model {default_model_name} as initial model.')

            # check if simulation number is provided and extract it from file
            try:
                # number has to be present & has to be an int (or be parsable into one) for the rest of the code to work
                simulation_number = int(row['simulation_number'])
            except:
                raise Exception(f'ERROR: no simulation_number provided in csv file {input_sweep_file}.')
            if verbose: print(f'changing these fields row # {i + 1}: {row}')

            dict_variables_to_change = dict()

            # unpack model_data
            if case_model == 'magnet':
                model_data = self.list_models[model_name].model_data
                next_simulation_name = model_data.GeneralParameters.magnet_name
            elif case_model == 'circuit':
                model_data = self.list_models[model_name].circuit_data
                next_simulation_name = model_data.GeneralParameters.circuit_name
            elif case_model == 'conductor':
                model_data = self.list_models[model_name].conductor_data
                next_simulation_name = model_data.GeneralParameters.conductor_name
            else:
                raise Exception(f'case_model {case_model} not supported by ParsimSweep.')

            # Initialize this variable, which is only used in the special case where circuit parameters are set to be changed (key "GlobalParameters.global_parameters")
            dict_circuit_param_to_change = {}

            # Iterate through the keys and values in the data dictionary & store all variables to change
            for j, (var_name, var_value) in enumerate(row.items()):
                # if value is null, skip this row
                if not pd.notnull(var_value): continue

                # Handle the change of a variable in the conductor list
                if 'Conductors[' in var_name:
                    # to check if var_name is valid (meaning it is the name of a variable in model_data)
                    try:
                        # try if eval is able to find the variable in model_data - if not: an Exception will be raised
                        eval('model_data.' + var_name)
                        dict_variables_to_change[var_name] = var_value
                    except:
                        print(f'WARNING: Sweeper skipped Column name "{var_name}" with value "{var_value}" in csv file {input_sweep_file}')

                # Handle the change of the special-case key GlobalParameters.global_parameters (dictionary of circuit global parameters)
                elif case_model == 'circuit' and var_name.startswith('GlobalParameters.global_parameters'):
                    # dict_global_parameters = deepcopy(model_data.GlobalParameters.global_parameters)  # original dictionary of circuit global parameters
                    circuit_param_to_change = var_name.split('GlobalParameters.global_parameters.')[-1]
                    # dict_global_parameters[circuit_param_to_change] = var_value
                    # dict_variables_to_change['GlobalParameters.global_parameters'] = dict_global_parameters
                    dict_circuit_param_to_change[circuit_param_to_change] = var_value

                # Check if the current variable is present in the model data structure & value in csv is not empty
                elif rhasattr(model_data, var_name):
                    # save valid new variable names and values to change them later
                    if type(var_value) == int or type(var_value) == float or type(var_value) == bool:
                        dict_variables_to_change[var_name] = var_value
                    elif type(var_value) == str:
                        dict_variables_to_change[var_name] = parse_str_to_list(var_value)
                    else:
                        raise Exception(f'ERROR: Datatype of Element in Column "{var_value}" Row "{j + 2}" of csv file {input_sweep_file} is invalid.')

                # print when columns have been skipped
                elif not rhasattr(model_data, var_name) and var_name != 'simulation_number':
                    print(f'WARNING: Column name "{var_name}" with value "{var_value}" in csv file {input_sweep_file} is skipped.')

            # Special case: If circuit parameters were set to change, add the key "GlobalParameters.global_parameters" to the dictionary of variables to change
            if len(dict_circuit_param_to_change) > 0:
                dict_global_parameters = deepcopy(model_data.GlobalParameters.global_parameters)  # original dictionary of circuit global parameters
                for key, value in dict_circuit_param_to_change.items():
                    dict_global_parameters[key] = value
                dict_variables_to_change['GlobalParameters.global_parameters'] = dict_global_parameters

            # if no variable to change is found, the simulation should run none the less, so dict_variables_to_change has to have an entry
            if not dict_variables_to_change:
                if case_model == 'magnet':
                    dict_variables_to_change['GeneralParameters.magnet_name'] = rgetattr(model_data, 'GeneralParameters.magnet_name')
                elif case_model == 'circuit':
                    dict_variables_to_change['GeneralParameters.circuit_name'] = rgetattr(model_data, 'GeneralParameters.circuit_name')
                elif case_model == 'conductor':
                    dict_variables_to_change['GeneralParameters.conductor_name'] = rgetattr(model_data, 'GeneralParameters.conductor_name')
                else:
                    raise Exception(f'case_model {case_model} not supported by ParsimSweep.')


            # copy original model to reset changes that step_modify_model_multiple_variables does
            if revert: local_model_copy = deepcopy(self.list_models[model_name])

            # make step ModifyModelMultipleVariables and alter all values found before
            next_step = ModifyModelMultipleVariables(type='ModifyModelMultipleVariables')
            next_step.model_name = model_name
            next_step.simulation_name = next_simulation_name
            next_step.variables_value = [[val] for val in dict_variables_to_change.values()]
            next_step.variables_to_change = list(dict_variables_to_change.keys())
            next_step.simulation_numbers = [simulation_number]
            next_step.software = software
            self.step_modify_model_multiple_variables(next_step, verbose=verbose)

            # reset changes to the model in self if revert flag is set
            if revert:
                self.list_models[model_name] = deepcopy(local_model_copy)
                del local_model_copy

        if verbose:
            print(f'Parsim Event called using input file {input_sweep_file}.')

    def steam_analyze_lhc_event(self, input_csv_file: str, flag_run_software: bool, software: str, dict_settings_paths: dict, file_counter: int):
        aSTEAM = AnalysisSTEAM()

        # Assign the keys read either from permanent-settings or local-settings TODO: later in inititalization of subclass
        for name, _ in dict_settings_paths.items():
            if name in  aSTEAM.settings.__dict__:
                print(f"Found {name} in settings")
                value = dict_settings_paths[name]
                aSTEAM.setAttribute(aSTEAM.settings, name, value)
                if value:
                    print('{} : {}. Added.'.format(name, value))
            elif name == 'library_path':
                aSTEAM.library_path = dict_settings_paths['library_path']
            else:
                print('{}: not found in the settings. Skipped.'.format(name))

        aSTEAM.data_analysis.WorkingFolders.library_path = dict_settings_paths['library_path']
        aSTEAM.data_analysis.PermanentSettings.PSPICE_path = dict_settings_paths['PSPICE_path']
        aSTEAM.data_analysis.PermanentSettings.XYCE_path = dict_settings_paths['XYCE_path']
        aSTEAM.data_analysis.PermanentSettings.PSPICE_library_path = dict_settings_paths['PSPICE_library_path']
        aSTEAM.data_analysis.PermanentSettings.local_PSPICE_folder = dict_settings_paths['local_PSPICE_folder']
        aSTEAM.data_analysis.PermanentSettings.local_XYCE_folder = dict_settings_paths['local_XYCE_folder']


        if software == 'PSPICE':
            local_folder = aSTEAM.settings.local_PSPICE_folder
            print(f"Changed local folder to {local_folder}")
        elif software == 'XYCE':
            local_folder = aSTEAM.settings.local_XYCE_folder
            print(f"Changed local folder to {local_folder}")

        circuit_name = get_circuit_name_from_eventfile(event_file=os.path.join(os.getcwd(), input_csv_file))
        if circuit_name.startswith("RCD"):
            aSTEAM.analyze_RCD_RCO_event(os.path.join(os.getcwd(), input_csv_file), local_folder, flag_run_software, software, file_counter,dict_settings_paths)
        elif circuit_name.startswith(("RD1", "RD2", "RD3", "RD4")):
            circuit_type = "IPD"
            aSTEAM.analyze_circuit_event(os.path.join(os.getcwd(), input_csv_file), local_folder, circuit_type, flag_run_software, software, file_counter,dict_settings_paths)
        elif circuit_name.startswith(("RQ4", "RQ5", "RQ7", "RQ8", "RQ9", "RQ10")) or (circuit_name.startswith("RQ6.") and len(circuit_name) == 6):
            circuit_type = find_IPQ_circuit_type_from_IPQ_parameters_table(os.path.join( aSTEAM.library_path, f"circuits/circuit_parameters/IPQ_circuit_parameters.csv"), input_csv_file.split("\\")[-1].split("_")[0])
            print(circuit_type)
            aSTEAM.analyze_circuit_event(os.path.join(os.getcwd(), input_csv_file), local_folder, circuit_type, flag_run_software, software, file_counter,dict_settings_paths)
        else:
            # circuit_type = get_circuit_type(circuit_name,  aSTEAM.library_path) OLD
            circuit_type = get_circuit_type_from_circuit_name(circuit_name,  aSTEAM.library_path)
            aSTEAM.analyze_circuit_event(os.path.join(os.getcwd(), input_csv_file), local_folder, circuit_type, flag_run_software, software, file_counter,dict_settings_paths)

    def analyze_circuit_event(self, input_csv_file: str, local_folder: str,circuit_type: str, flag_run_software: bool, software: str, file_counter: int,dict_settings_paths: dict):
        #file_counter = 1
        #file_name_analysis = os.path.join(os.getcwd(), "analysisSTEAM_settings.yaml") #file containing settings paths
        unique_identifier_event = os.path.splitext(os.path.basename(input_csv_file))[0]

        output_directory_yaml_files = dict_settings_paths['output_directory_yaml_files']
        output_directory_event_files = dict_settings_paths['output_directory_event_files']

        yaml_file_name = f'Infile_{software}_{unique_identifier_event}_{file_counter}.yaml'
        event_file_name = f'Eventfile_{software}_{unique_identifier_event}_{file_counter}.csv'

        path_output_yaml_file = os.path.join(output_directory_yaml_files,yaml_file_name)
        path_output_event_csv = os.path.join(output_directory_event_files,event_file_name)

        self.data_analysis.AnalysisStepDefinition = {
            'setup_folder_PSPICE': SetUpFolder(type='SetUpFolder', simulation_name=circuit_type, software=software),
            'makeModel_ref': MakeModel(type='MakeModel', model_name='BM', file_model_data=circuit_type,
                                       case_model='circuit', software=software, simulation_name=None,
                                       simulation_number=None, flag_build=True, verbose=False,
                                       flag_plot_all=False, flag_json=False),
            'modifyModel_probe': ModifyModelMultipleVariables(type='ModifyModelMultipleVariables', model_name='BM',
                                           variables_to_change=['PostProcess.probe.probe_type'],
                                                              variables_value=[['CSDF']], software=software,
                                                              simulation_name=None,
                                           simulation_numbers=[]),
            'runParsimEvent': ParsimEvent(type='ParsimEvent', input_file=input_csv_file,
                                          path_output_event_csv=path_output_event_csv, path_output_viewer_csv=None,
                                          simulation_numbers=[file_counter], model_name='BM', case_model='circuit',
                                          simulation_name=circuit_type, software=software, t_PC_off=None,
                                          rel_quench_heater_trip_threshold=None, current_polarities_CLIQ=[],
                                          dict_QH_circuits_to_QH_strips={},
                                          default_keys=DefaultParsimEventKeys(local_LEDET_folder=None,
                                                                              path_config_file=None, default_configs=[],
                                                                              path_tdms_files=None,
                                                                              path_output_measurement_files=None,
                                                                              path_output=local_folder)),
            'run_simulation': RunSimulation(type='RunSimulation', software=software, simulation_name=circuit_type, simulation_numbers=[file_counter])}

        self.output_path = local_folder
        if software == 'PSPICE':
            self.data_analysis.PermanentSettings.local_PSPICE_folder = local_folder
        elif software == 'XYCE':
            self.data_analysis.PermanentSettings.local_XYCE_folder = local_folder
        if flag_run_software== False:
            self.data_analysis.AnalysisStepSequence = ['setup_folder_PSPICE', 'makeModel_ref', 'modifyModel_probe', 'runParsimEvent']
        else:
            self.data_analysis.AnalysisStepSequence = ['setup_folder_PSPICE', 'makeModel_ref', 'modifyModel_probe', 'runParsimEvent', 'run_simulation']

        if software == 'PSPICE':
            local_PSPICE_folder = self._get_local_folder('local_PSPICE_folder')
            list_output_file = [
                os.path.join(local_PSPICE_folder, f'{circuit_type}', f'{file_counter}', f'{circuit_type}.cir')]
        elif software == 'XYCE':
            local_XYCE_folder = self._get_local_folder('local_XYCE_folder')
            list_output_file = [
                os.path.join(local_XYCE_folder, f'{circuit_type}', f'{file_counter}', f'{circuit_type}.cir')]

        if os.path.exists(path_output_yaml_file): os.remove(path_output_yaml_file)
        for file in list_output_file:
            if os.path.exists(file): os.remove(file)

        # act
        #print(self.data_analysis.PermanentSettings.PSPICE_path)
        self.write_analysis_file(path_output_file=path_output_yaml_file)
        self.run_analysis(verbose= True)



    def analyze_RCD_RCO_event(self, input_csv_file: str, local_folder: str, flag_run_software: bool, software: str, file_counter: int, dict_settings_paths: dict):

        unique_identifier_event = os.path.splitext(os.path.basename(input_csv_file))[0]

        output_directory_yaml_files = dict_settings_paths['output_directory_yaml_files']
        output_directory_event_files = dict_settings_paths['output_directory_event_files']

        yaml_file_name = f'Infile_{software}_{unique_identifier_event}_{file_counter}.yaml'
        event_file_name_RCO = f'Eventfile_RCO_{software}_{unique_identifier_event}_{file_counter}.csv'
        event_file_name_RCD = f'Eventfile_RCD_{software}_{unique_identifier_event}_{file_counter}.csv'

        path_output_yaml_file = os.path.join(output_directory_yaml_files,yaml_file_name)
        path_output_event_RCO_csv = os.path.join(output_directory_event_files, event_file_name_RCO)
        path_output_event_RCD_csv = os.path.join(output_directory_event_files, event_file_name_RCD)

        # arrange
        file_name_analysis = os.path.join(os.getcwd(), "analysisSTEAM_settings.yaml") #file containing settings paths
        aSTEAM_1 = AnalysisSTEAM(file_name_analysis=file_name_analysis)
        if software == 'PSPICE':
            aSTEAM_1.settings.local_PSPICE_folder = local_folder
        elif software == 'XYCE':
            aSTEAM_1.settings.local_XYCE_folder = local_folder
        aSTEAM_1.data_analysis.AnalysisStepDefinition = {
            'setup_folder_PSPICE': SetUpFolder(type='SetUpFolder', simulation_name='RCO', software=software),
            'makeModel_ref': MakeModel(type='MakeModel', model_name='BM', file_model_data='RCO', case_model='circuit',
                                       software=software, simulation_name=None, simulation_number=None, flag_build=True,
                                       verbose=False, flag_plot_all=False, flag_json=False),
            'runParsimEvent': ParsimEvent(type='ParsimEvent', input_file=input_csv_file,
                                          path_output_event_csv=path_output_event_RCO_csv, path_output_viewer_csv=None,
                                          simulation_numbers=[file_counter], model_name='BM', case_model='circuit',
                                          simulation_name='RCO', software=software, t_PC_off=None,
                                          rel_quench_heater_trip_threshold=None, current_polarities_CLIQ=[],
                                          dict_QH_circuits_to_QH_strips={},
                                          default_keys=DefaultParsimEventKeys(local_LEDET_folder=None,
                                                                              path_config_file=None, default_configs=[],
                                                                              path_tdms_files=None,
                                                                              path_output_measurement_files=None,
                                                                              path_output=local_folder)),
            'run_simulation': RunSimulation(type='RunSimulation', software=software, simulation_name='RCO',
                                            simulation_numbers=[file_counter])}
        aSTEAM_1.output_path = local_folder
        if software == 'PSPICE':
            aSTEAM_1.data_analysis.PermanentSettings.local_PSPICE_folder = local_folder
        elif software == 'XYCE':
            aSTEAM_1.data_analysis.PermanentSettings.local_XYCE_folder = local_folder
        if flag_run_software == False:
            aSTEAM_1.data_analysis.AnalysisStepSequence = ['setup_folder_PSPICE', 'makeModel_ref', 'runParsimEvent']
        else:
            aSTEAM_1.data_analysis.AnalysisStepSequence = ['setup_folder_PSPICE', 'makeModel_ref', 'runParsimEvent', 'run_simulation']

        aSTEAM_2 = AnalysisSTEAM(file_name_analysis=file_name_analysis)
        if software == 'PSPICE':
            aSTEAM_2.settings.local_PSPICE_folder = local_folder
        elif software == 'XYCE':
            aSTEAM_2.settings.local_XYCE_folder = local_folder
        aSTEAM_2.data_analysis.AnalysisStepDefinition = {
            'setup_folder_PSPICE': SetUpFolder(type='SetUpFolder', simulation_name='RCD', software=software),
            'makeModel_ref': MakeModel(type='MakeModel', model_name='BM', file_model_data='RCD', case_model='circuit',
                                       software=software, simulation_name=None, simulation_number=None, flag_build=True,
                                       verbose=False, flag_plot_all=False, flag_json=False),
            'runParsimEvent': ParsimEvent(type='ParsimEvent', input_file=input_csv_file,
                                          path_output_event_csv=path_output_event_RCD_csv, path_output_viewer_csv=None,
                                          simulation_numbers=[file_counter], model_name='BM', case_model='circuit',
                                          simulation_name='RCD', software=software, t_PC_off=None,
                                          rel_quench_heater_trip_threshold=None, current_polarities_CLIQ=[],
                                          dict_QH_circuits_to_QH_strips={},
                                          default_keys=DefaultParsimEventKeys(local_LEDET_folder=None,
                                                                              path_config_file=None, default_configs=[],
                                                                              path_tdms_files=None,
                                                                              path_output_measurement_files=None,
                                                                              path_output=local_folder)),
            'run_simulation': RunSimulation(type='RunSimulation', software=software, simulation_name='RCD',
                                            simulation_numbers=[file_counter])}
        aSTEAM_2.output_path = local_folder
        if software == 'PSPICE':
            aSTEAM_2.data_analysis.PermanentSettings.local_PSPICE_folder = local_folder
        elif software == 'XYCE':
            aSTEAM_2.data_analysis.PermanentSettings.local_XYCE_folder = local_folder
        if flag_run_software == False:
            aSTEAM_2.data_analysis.AnalysisStepSequence = ['setup_folder_PSPICE', 'makeModel_ref', 'runParsimEvent']
        else:
            aSTEAM_2.data_analysis.AnalysisStepSequence = ['setup_folder_PSPICE', 'makeModel_ref', 'runParsimEvent', 'run_simulation']

        if input_csv_file.endswith('.csv'):
            outputfile_1 = os.path.join(os.getcwd(), 'output', 'run_parsim_event_circuit',
                                        f'TestFile_AnalysisSTEAM_run_parsim_event_circuit_RCO_{file_counter}.yaml')
            outputfile_2 = os.path.join(os.getcwd(), 'output', 'run_parsim_event_circuit',
                                        f'TestFile_AnalysisSTEAM_run_parsim_event_circuit_RCD_{file_counter}.yaml')
            if software == 'PSPICE':
                list_output_file = [
                    os.path.join(aSTEAM_1.settings.local_PSPICE_folder, 'RCO', f'{file_counter}', 'RCO.cir'),
                    os.path.join(aSTEAM_2.settings.local_PSPICE_folder, 'RCD', f'{file_counter}', 'RCD.cir')]
            elif software == 'XYCE':
                list_output_file = [
                    os.path.join(aSTEAM_1.settings.local_XYCE_folder, 'RCO', f'{file_counter}', 'RCO.cir'),
                    os.path.join(aSTEAM_2.settings.local_XYCE_folder, 'RCD', f'{file_counter}', 'RCD.cir')]
            if os.path.exists(outputfile_1): os.remove(outputfile_1)
            if os.path.exists(outputfile_2): os.remove(outputfile_2)
            for file in list_output_file:
                if os.path.exists(file): os.remove(file)

            # act
            aSTEAM_1.write_analysis_file(path_output_file=outputfile_1)
            aSTEAM_1.run_analysis()

            aSTEAM_2.write_analysis_file(path_output_file=outputfile_2)
            aSTEAM_2.run_analysis()


    # def __get_circuit_family_name(self, circuit_name: str):
    #     if circuit_name.startswith("RCBH") or circuit_name.startswith("RCBV"):
    #         return "60A"
    #     elif circuit_name.startswith("RD"):
    #         return "IPD"
    #     elif circuit_name.startswith("RQX"):
    #         return "RQX"
    #     elif circuit_name.startswith(("RQ4", "RQ5", "RQ7", "RQ8", "RQ9", "RQ10")) or (circuit_name.startswith("RQ6.") and len(circuit_name) == 6):
    #         return "IPQ"
    #     elif circuit_name.startswith(("RQT12", "RQT13", "RQS", "RSS", "RQTL7", "RQTL8", "RQTL10", "RQTL11", "RCBX", "RQSX3", "RCS", "ROD", "ROF", "RSD", "RSF", "RQTL9", "RQTD", "RQTF", "RCD", "RCO", "RC.")) or (circuit_name.startswith("RQ6.") and len(circuit_name) == 8):
    #         return "600A"
    #     elif circuit_name.startswith("RQ"):
    #         return "RQ"
    #     elif circuit_name.startswith(("RCBY", "RCBC", "RCTX")):
    #         return "80-120A"
    #     elif circuit_name.startswith("RB"):
    #         return "RB"

    # def __get_magnet_name(self, circuit_name: str, simulation_name: str, circuit_type: str):
    #     #assert (simulation_name == self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_name)
    #     #assert (circuit_type == self.__get_circuit_type(circuit_name, self.library_path))
    #     #assert (True == False)
    #
    #     if circuit_name.startswith("RCBH") or circuit_name.startswith("RCBV"):
    #         return "MCBH"
    #     elif circuit_name.startswith("RD"):
    #         #circuit_type = self.__get_circuit_type(circuit_name, self.library_path)
    #         magnet_dict = {"RD1": "MBX", "RD2": "MBRC", "RD3": "MBRS", "RD4": "MBRB"}
    #         return magnet_dict.get(circuit_type, "")
    #     elif circuit_name.startswith("RQX"):
    #         return ["MQXA", "MQXB"]
    #     elif circuit_name.startswith(("RQ4", "RQ5", "RQ7", "RQ8", "RQ9", "RQ10")) or (circuit_name.startswith("RQ6.") and len(circuit_name) == 6):
    #         magnet_dict = {"IPQ_RQ4_2_2xRPHH_2xMQY": "MQY", "IPQ_RQ4_4_2xRPHH_4xMQY": ["MQY", "MQY"], "IPQ_RQ5_2_2xRPHGB_2xMQML": "MQML", "IPQ_RQ5_2_2xRPHH_2xMQY": "MQY", "IPQ_RQ5_4_2xRPHGB_4xMQM": ["MQM", "MQM"], "IPQ_RQ5_4_2xRPHH_4xMQY": ["MQY", "MQY"], "IPQ_RQ6_2_2xRPHGB_2xMQML": "MQML", "IPQ_RQ6_2_2xRPHGB_2xMQY": "MQY", "IPQ_RQ6_4_2xRPHGB_2xMQM_2xMQML": ["MQM", "MQML"], "IPQ_RQ7_2_2xRPHGA_2xMQM": "MQM", "IPQ_RQ7_4_2xRPHGA_4xMQM": ["MQM", "MQM"], "IPQ_RQ8_2_2xRPHGA_2xMQML": "MQML", "IPQ_RQ9_4_2xRPHGA_2xMQM_2xMQMC": ["MQM", "MQMC"], "IPQ_RQ10_2_2xRPHGA_2xMQML": "MQML"}
    #         return magnet_dict.get(simulation_name, "")
    #     elif circuit_name.startswith("RQ6.") and len(circuit_name) == 8:
    #         return ["MQTLH", "MQTLH_quenchback"]
    #     elif circuit_name.startswith(("RQTL7", "RQTL8", "RQTL10", "RQTL11")):
    #         return "MQTLI"
    #     elif circuit_name.startswith("RQTL9"):
    #         return ["MQTLI", "MQTLI_quenchback"]
    #     elif circuit_name.startswith("RQSX3"):
    #         return "MQSX"
    #     elif circuit_name.startswith("RQS"):
    #         return ["MQS", "MQS_quenchback"]
    #     elif circuit_name.startswith(("RQT12", "RQT13")):
    #         return "MQT"
    #     elif circuit_name.startswith(("RQTD", "RQTF")):
    #         return ["MQT", "MQT_quenchback"]
    #     elif circuit_name.startswith("RQ"):
    #         return "MQ"
    #     elif circuit_name.startswith("RCBY"):
    #         return "MCBYH"
    #     elif circuit_name.startswith("RCBC"):
    #         return "MCBCH"
    #     elif circuit_name.startswith("RCS"):
    #         return ["MCS", "MCS_quenchback"]
    #     elif circuit_name.startswith("RB"):
    #         return "MB"
    #     elif circuit_name.startswith("RCBX"):
    #         return ["MCBXH", "MCBXV"]
    #     elif circuit_name.startswith("RSS"):
    #         return ["MSS", "MSS_quenchback"]
    #     elif circuit_name.startswith(("ROD", "ROF")):
    #         return ["MO", "MO_quenchback"]
    #     elif circuit_name.startswith(("RSD", "RSF")):
    #         return ["MS", "MS_quenchback"]
    #     elif simulation_name == "RCD":
    #         return ["MCD", "MCD_quenchback"]
    #     elif simulation_name == "RCO":
    #         return ["MCO", "MCO_quenchback"]

    # def __get_number_of_magnets(self,circuit_name: str, simulation_name: str, circuit_type: str):
    #     circuit_family_name = get_circuit_family_from_circuit_name(circuit_name)
    #     #circuit_type = self.__get_circuit_type(circuit_name, self.library_path)
    #     if circuit_type in ["RCS", "RB"]:
    #         return 154
    #     elif circuit_type in ["RCD", "RCO"]:
    #         return 77
    #     elif circuit_name.startswith("RQ6.") and len(circuit_name) == 8:
    #         return 6
    #     elif circuit_name.startswith(("RQS.R", "RQS.L", "RQTL9")):
    #         return 2
    #     elif circuit_name.startswith(("RQS.A", "RSS", "RQX")):
    #         return 4
    #     elif circuit_name.startswith(("RQTD", "RQTF")):
    #         return 8
    #     elif circuit_family_name in ["60A", "IPD", "80-120A", "600A"]:
    #         return 1
    #     elif circuit_type == "RQ_47magnets":
    #         return 47
    #     elif circuit_type == "RQ_51magnets":
    #         return 51
    #     elif circuit_family_name == "IPQ":
    #         return int(int(re.search(r'_(\d+)_', simulation_name).group(1))/2)

    # def __get_number_of_apertures(self, circuit_name: str):
    #     circuit_family_name = get_circuit_family_from_circuit_name(circuit_name)
    #     if circuit_family_name in ["IPQ", "RB"]:
    #         return 2
    #     else:
    #         return 1

    def __get_magnets_list(self, number_of_magnets: int):
        list = []
        for i in range(1, number_of_magnets+1):
            list.append(i)
        return list

    # def __get_magnet_types_list(self, number_of_magnets: int, simulation_name: str):
    #     list = []
    #     if number_of_magnets == 4 and simulation_name.startswith("RQX"): #to be improved
    #         list = [1, 2, 2, 1]
    #     elif simulation_name.startswith("IPQ") and number_of_magnets == 2:
    #         list = [1, 2]
    #     elif simulation_name.startswith("RB"):
    #         for i in range(1, number_of_magnets+1):
    #             list.append(1)
    #     elif number_of_magnets in [154, 13, 8, 77, 6, 12, 11, 10, 9, 4, 2]:
    #         list = [1] + [2] * (number_of_magnets - 1)
    #     else:
    #         for i in range(1, number_of_magnets+1):
    #             list.append(1)
    #     return list

    # def __get_circuit_type(self, circuit_name: str, library_path, simulation_name: str = None):
    #     # if simulation_name:
    #     #     assert(self.data_analysis.AnalysisStepDefinition['runParsimEvent'].simulation_name == simulation_name)
    #     #     #assert(True == False)
    #     if circuit_name.startswith("RCBH") or circuit_name.startswith("RCBV"):
    #         return "RCB"
    #     elif circuit_name.startswith(("RD1", "RD2", "RD3", "RD4")):
    #         return {"RD1": "RD1", "RD2": "RD2", "RD3": "RD3", "RD4": "RD4"}.get(circuit_name[:3], "No match found")
    #     elif circuit_name.startswith("RQX"):
    #         return "RQX"
    #     elif circuit_name.startswith(("RQ4", "RQ5", "RQ6", "RQ7", "RQ8", "RQ9", "RQ10")):
    #         return circuit_name.split(".")[0]
    #     elif circuit_name.startswith(("RQT12", "RQT13")):
    #         return "RQT_12_13"
    #     elif circuit_name.startswith(("RQTL7", "RQTL8", "RQTL10", "RQTL11")):
    #         return "RQTL_7_8_10_11"
    #     elif circuit_name.startswith("RQTL9"):
    #         return "RQTL9"
    #     elif circuit_name.startswith(("RQTD", "RQTF")):
    #         return "RQT"
    #     elif circuit_name.startswith("RQSX3"):
    #         return "RQSX3"
    #     elif circuit_name.startswith("RQS"):
    #         return "RQS"
    #     elif circuit_name.startswith("RQ."):
    #         circuit_name_temp = circuit_name.replace(".", "D_")
    #         magnet_number = find_n_magnets_in_circuit(os.path.join(library_path, f"circuits/circuit_parameters/RQ_circuit_parameters.csv"), circuit_name_temp)
    #         return f"RQ_{magnet_number}magnets"
    #     elif circuit_name.startswith("RCS"):
    #         return "RCS"
    #     elif circuit_name.startswith("RB"):
    #         return "RB"
    #     elif circuit_name.startswith("RCBX"):
    #         return "RCBX"
    #     elif circuit_name.startswith("RCBC"):
    #         return "RCBC"
    #     elif circuit_name.startswith("RCBY"):
    #         return "RCBY"
    #     elif circuit_name.startswith("RSS"):
    #         return "RSS"
    #     elif circuit_name.startswith(("RSD")):
    #         magnet_number = find_n_magnets_in_circuit(os.path.join(library_path, f"circuits/circuit_parameters/600A_circuit_parameters.csv"), circuit_name)
    #         return f"RSD_{magnet_number}magnets"
    #     elif circuit_name.startswith(("RSF")):
    #         magnet_number = find_n_magnets_in_circuit(os.path.join(library_path, f"circuits/circuit_parameters/600A_circuit_parameters.csv"), circuit_name)
    #         return f"RSF_{magnet_number}magnets"
    #     elif circuit_name.startswith(("RO")):
    #         magnet_number = find_n_magnets_in_circuit(os.path.join(library_path, f"circuits/circuit_parameters/600A_circuit_parameters.csv"), circuit_name)
    #         return f"RO_{magnet_number}magnets"
    #     elif simulation_name == "RCD": #improvement pending
    #         return "RCD"
    #     elif simulation_name == "RCO": #improvement pending
    #         return "RCO"

    # def __get_quenching_magnet_number(self, position: str, circuit_family_name: str,library_path):
    #     df = pd.read_csv(os.path.join(library_path, 'circuits', 'circuit_parameters', f"{circuit_family_name}_LayoutDetails.csv"))
    #     mask = df['Magnet'].str.split('.').str[1] == position
    #     result = df.loc[mask, '#Electric_circuit'].iloc[0]
    #     return result

    # def __split_csv(self, input_file_name):
    #     # Create empty lists to hold the odd and even rows
    #     odd_rows = []
    #     even_rows = []
    #
    #     # Open the input CSV file and read in the rows
    #     with open(input_file_name, 'r') as input_file:
    #         reader = csv.reader(input_file)
    #
    #         # Save the header row
    #         header = next(reader)
    #
    #         # Loop over the remaining rows and append them to the odd or even list
    #         for i, row in enumerate(reader):
    #             if i % 2 == 0:
    #                 even_rows.append(row)
    #             else:
    #                 odd_rows.append(row)
    #
    #     # Write the odd and even rows to separate output files
    #     output_odd_file_name = 'output_odd.csv'
    #     with open(output_odd_file_name, 'w', newline='') as output_odd_file:
    #         writer_odd = csv.writer(output_odd_file)
    #         writer_odd.writerow(header)
    #         writer_odd.writerows(odd_rows)
    #
    #     output_even_file_name = 'output_even.csv'
    #     with open(output_even_file_name, 'w', newline='') as output_even_file:
    #         writer_even = csv.writer(output_even_file)
    #         writer_even.writerow(header)
    #         writer_even.writerows(even_rows)
    #
    #     # Return a list of the output file names
    #     return [output_even_file_name, output_odd_file_name]

    # def __find_magnets(self, filename, key):
    #     with open(filename, 'r') as file:
    #         reader = csv.DictReader(file)
    #         for row in reader:
    #             if row['circuit'] == key:
    #                 return row['NumberOfMagnets']
    #         return None

    # def __find_circuit_model(self, filename, key):
    #     with open(filename, 'r') as file:
    #         reader = csv.DictReader(file)
    #         for row in reader:
    #             if row['circuit'] == key:
    #                 return row['circuit_type']
    #         return None

    # def __get_first_circuit_name(self, csv_file):
    #     with open(csv_file, 'r') as file:
    #         reader = csv.DictReader(file)
    #         for row in reader:
    #             first_entry = row.get("Circuit Name")
    #             if first_entry:
    #                 return first_entry

    def extract_stimulus_values(self, stl_file, output_folder):
        stimulus_pattern = re.compile(r'\.STIMULUS\s+(\S+)\s+PWL\s+([\s\S]*?)(?=\.STIMULUS|\Z)', re.IGNORECASE)
        value_pattern = re.compile(r'\(\s*([\d.]+)\s*[s]?,\s*([\d.]+)\s*\)')

        with open(stl_file, 'r') as file:
            contents = file.read()

        stimuli = stimulus_pattern.findall(contents)
        for stimulus in stimuli:
            stimulus_name = stimulus[0]
            stimulus_values = stimulus[1]

            values = value_pattern.findall(stimulus_values)
            values = [(value[0], value[1]) for value in values]  # Remove 's' from the first entry

            csv_file_name = stimulus_name + '.csv'
            csv_file_path = os.path.join(output_folder, csv_file_name)

            with open(csv_file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(values)

            print(f"Created CSV file: {csv_file_path}")

    def _get_local_folder(self, selected_local_folder: str):
        '''
        ** Return the local tool folder after resolving the logic **
        - The path to the selected local tool folder is read from the settings
        - If the path is absolute, the path is simply returned
        - If the path is relative, the path is resolved with respect to location of the original STEAM analysis yaml file (self.path_analysis_file)
        :param selected_local_folder: Selected local folder to load from the settings
        :return:
        '''
        path_from_settings = getattr(self.settings, selected_local_folder)
        local_model_folder = Path(path_from_settings) if os.path.isabs(path_from_settings) else Path(os.getcwd() / Path(path_from_settings)).resolve()
        return local_model_folder
