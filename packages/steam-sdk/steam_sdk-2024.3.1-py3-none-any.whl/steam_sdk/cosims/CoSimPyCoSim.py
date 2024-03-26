import os
import shutil
from pathlib import Path
from typing import Union, List

from steam_sdk.data.DataCoSim import NSTI
from steam_sdk.data.DataFiQuS import DataFiQuS
from steam_sdk.data.DataModelCosim import sim_FiQuS, sim_LEDET, sim_PSPICE, sim_XYCE, sim_Generic, FileToCopy
from steam_sdk.data.DataPyCoSim import DataPyCoSim
from steam_sdk.data.DataSettings import DataSettings
from steam_sdk.drivers.DriverFiQuS import DriverFiQuS
from steam_sdk.drivers.DriverLEDET import DriverLEDET
from steam_sdk.drivers.DriverPSPICE import DriverPSPICE
from steam_sdk.drivers.DriverXYCE import DriverXYCE
from steam_sdk.parsers.ParserYAML import yaml_to_data
from steam_sdk.parsers.utils_ParserCosims import write_model_input_files
from steam_sdk.utils.make_folder_if_not_existing import make_folder_if_not_existing


class CosimPyCoSim:
    """
        Class to run a co-operative simulation
    """

    def __init__(self,
                 file_model_data: str,
                 sim_number: int,
                 data_settings: DataSettings = None,
                 verbose: bool = False
                 ):
        """
            Builder object to generate models from STEAM simulation tools specified by user

            file_model_data: path to folder with input data (DataPyCoSim yaml input file)
            sim_number: number of the simulation
            :param data_settings: DataSettings object containing all settings, previously read from user specific settings.SYSTEM.yaml file or from a STEAM analysis permanent settings
            verbose: to display internal processes (output of status & error messages) for troubleshooting

            Notes:
            The PyCoSim folder structure will be as follows:
            - local_PyCoSim is the main folder
              - COSIM_NAME
                - SOFTWARE_FOLDER
                  - SIMULATION_NAME
                    - {COSIM_NUMBER}_{SIMULATION_NUMBER}_{TIME_WINDOW_NUMBER}_{ITERATION_NUMBER}

            Example 1:
            - C:\local_PyCoSim
              - RQX
                - LEDET
                  - MQXA
                    - Field Maps
                    - 55_1_1_1\LEDET\Input
                  - MQXA
                    - 55_2_1_1
                  - MQXB
                    - 55_1_1_1
                  - MQXB
                    - 55_2_1_1

            Example 1:
            - C:\local_PyCoSim
              - RQX
                - FiQuS
                  - MQXA
                    - G1
                      - M1
                        - 55_1_1_1
                - LEDET
                  - MQXB
                    - Field Maps
                    - 55
                     - 1_1_1\LEDET\Input
                - PSPICE
                  - RQX_cosim
                    - 55_1_1_1

            D:\library_mesh

        """
        # Load data from input file
        self.cosim_data: DataPyCoSim = yaml_to_data(file_model_data, DataPyCoSim)
        self.local_PyCoSim_folder = Path(data_settings.local_PyCoSim_folder).resolve()
        self.sim_number = sim_number
        self.data_settings = data_settings
        self.verbose = verbose
        self.summary = {}  # This will be populated with a summary of simulation results (mainly used ofr DAKOTA)

        if verbose:
            print(f'PyCoSim initialized with input file {file_model_data}.')
            print(f'Local PyCoSim folder is {self.local_PyCoSim_folder}')

    def run(self):
        """
        This runs co-sim
        """
        # Read initial
        # A1 Make the folder structure
        # A2 Make the input files for the pre-run simulation
        # A3 Run the pre-run input files
        # B Start a while loop with some convergence criteria
        #   B0 If present, check output to see if convergence is met
        #   B1 Make new folders
        #   B2 Make new input files using output of previous simulation
        #   B3 Run the new input files
        # C1 Make the folder structure for the final run
        # C2 Make the input files for the final-run simulation
        # C3 Run the final-run input files

        if self.verbose: print(f'Co-simulation {self.cosim_data.GeneralParameters.cosim_name} {self.sim_number} started.')
        self.nsti = NSTI(self.sim_number, 0, 0, 0)

        # Pre-cosim
        for model_set, model in enumerate(self.cosim_data.Simulations.values()):
            self.nsti.update(self.sim_number, model_set, 0, 0)  # Initial time window and iteration  # cosim_nsti --> N=Simulation number. S=Simulation set. T=Time window. I=Iteration.
            write_model_input_files(cosim_data=self.cosim_data, model_name=model.name, model=model,
                                    cosim_software='PyCoSim', local_cosim_folder=self.local_PyCoSim_folder,
                                    data_settings=self.data_settings,
                                    nsti=self.nsti, verbose=self.verbose)
            # TODO Pass input/output
            # if flag_run_precosim...
            if model.flag_run_pre_cosim:
                if self.verbose: print(f'Model {model.name}. Simulation set {self.nsti.s}. Pre-cosim simulation.')

                self._run_sim(model=model)
                # TODO add some basic check that the simulation run wihout errors
                self._copy_files(model=model)
                # self._copy_variables(model_name=model_name, model=model, verbose=verbose) #TODO implentation needed

        # Co-simulation
        # Loop through time windows
        for model_set, model in enumerate(self.cosim_data.Simulations.values()):
            # Reset convergence variables
            flag_converge, current_iteration = False, 0
            # Loop until convergence is found
            while flag_converge == False:
                for tw, time_wind in enumerate(self.cosim_data.Settings.Time_Windows):
                    self.nsti.update(self.sim_number, model_set, tw + 1, current_iteration)
                    if self.verbose: print(f'Model {model.name}. Simulation set {self.nsti.s}. Time window {self.nsti.t}. Iteration {self.nsti.i}.')
                    # TODO Get input/output
                    # Make model

                    # TODO Pass input/output
                    if model.flag_run_cosim:
                        write_model_input_files(cosim_data=self.cosim_data, model_name=model.name, model=model,
                                                cosim_software='PyCoSim', data_settings=self.data_settings,
                                                nsti=self.nsti, verbose=self.verbose)
                        # TODO Run model
                        # TODO add some basic check that the simulation run wihout errors
                # TODO check convergence
                if 2 == 2:
                    flag_converge = True
                    if self.verbose: print(f'Model {model.name}. Simulation set {self.nsti.s}. Time window {self.nsti.t}. Convergence reached at iteration {self.nsti.i}.')  # Add info about convergence crirteria
                else:
                    current_iteration = current_iteration + 1

        # Post-cosim
        for model_set, model in enumerate(self.cosim_data.Simulations.values()):
            if self.cosim_data.Settings.Options_run.executeCleanRun[model_set]:
                self.nsti.update(self.sim_number, model_set, len(self.cosim_data.Settings.Time_Windows.t_0) + 1, 0)
                if self.verbose: print(f'Model {model.name}. Simulation set {self.nsti.s}. Post-cosim simulation.')
                # TODO Get input/output
                # Make model
                write_model_input_files(cosim_data=self.cosim_data, model_name=model.name, model=model,
                                        cosim_software='PyCoSim', data_settings=self.data_settings,
                                        nsti=self.nsti, verbose=self.verbose)
                if model.flag_run_post_cosim:

                    pass
                    # TODO Run model
                    # TODO add some basic check that the simulation run wihout errors

        if self.verbose: print(f'Co-simulation {self.cosim_data.GeneralParameters.cosim_name} {self.sim_number} finished.')


    def _run_sim(self, model: Union[sim_FiQuS, sim_LEDET, sim_PSPICE, sim_XYCE]):
        """
        Run selected simulation.
        The function applies a different logic for each simulation software.
        """

        # Define local folder
        local_folder = self.__find_local_target_folder(model=model)

        # run simulation
        if model.type == 'FiQuS':
            dFiQuS = DriverFiQuS(path_folder_FiQuS_input=local_folder, path_folder_FiQuS_output=local_folder,
                                 FiQuS_path=self.data_settings.FiQuS_path, GetDP_path=self.data_settings.GetDP_path, verbose=self.verbose)
            self.summary[model.name] = dFiQuS.run_FiQuS(sim_file_name=f'{model.modelName}_{self.nsti.n_s_t_i}_FiQuS')
        elif model.type == 'LEDET':
            dLEDET = DriverLEDET(path_exe=self.data_settings.LEDET_path, path_folder_LEDET=local_folder, verbose=self.verbose)
            dLEDET.run_LEDET(nameMagnet=model.modelName, simsToRun=str(model.simulationNumber), simFileType='.xlsx')  # simFileType is hard-coded
        elif model.type == 'PSPICE':
            dPSPICE = DriverPSPICE(path_exe=self.data_settings.PSPICE_path, path_folder_PSPICE=local_folder, verbose=self.verbose)
            dPSPICE.run_PSPICE(nameCircuit=model.modelName, suffix='')
        elif model.type == 'XYCE':
            dXYCE = DriverXYCE(path_exe=self.data_settings.XYCE_path, path_folder_XYCE=local_folder, verbose=self.verbose)
            dXYCE.run_XYCE(nameCircuit=model.modelName, suffix='')
        else:
            raise Exception(f'Software {model.type} not supported for automated running.')


    def _copy_files(self, model: Union[sim_Generic, sim_FiQuS, sim_LEDET, sim_PSPICE, sim_XYCE]):
        '''
        This function copies files across from the output of one model to another.
        :param model_name:
        :param model:
        :param verbose:
        :return:
        '''

        # Get list of files to copy, which depends on the current co-simulation state
        if self.nsti.t == 0:
            files_to_copy: List[FileToCopy] = model.files_to_copy_after.pre_cosim
        elif self.nsti.t > len(self.cosim_data.Settings.Time_Windows.t_0):
            files_to_copy: List[FileToCopy] = model.files_to_copy_after.post_cosim
        else:
            files_to_copy: List[FileToCopy] = model.files_to_copy_after.cosim

        if len(files_to_copy) > 0:
            # Define local folder
            local_folder = self.__find_local_source_folder(model=model)

            # Copy files
            for file_to_copy in files_to_copy:
                if file_to_copy.old_file_name_relative_path:
                    original_file = Path(Path(local_folder), file_to_copy.old_file_name_relative_path).resolve()
                    target_local_folder = self.__find_local_target_folder(model=self.cosim_data.Simulations[
                        file_to_copy.target_model])
                    if not file_to_copy.new_file_name_relative_path:
                        file_to_copy.new_file_name_relative_path = file_to_copy.old_file_name_relative_path
                    target_file = Path(Path(target_local_folder), file_to_copy.new_file_name_relative_path).resolve()
                    make_folder_if_not_existing(os.path.dirname(target_file), verbose=self.verbose)
                    if self.verbose: print(f'Copy file {original_file} to file {target_file}.')
                    shutil.copyfile(original_file, target_file)

    def __find_local_source_folder(self, model: Union[sim_FiQuS, sim_LEDET, sim_PSPICE, sim_XYCE]):
        '''
        Function to find the path to the local folder, which has a different logic for each simulation tool
        :param model: Current simulation model
        :return: Path to the local folder of the current simulation model
        '''
        local_folder_prefix = os.path.join(self.local_PyCoSim_folder,
                                           self.cosim_data.GeneralParameters.cosim_name,
                                           model.type,
                                           model.modelName)
        if model.type == 'FiQuS':
            fiqus_input_file_path = os.path.join(local_folder_prefix, f'{model.modelName}_{self.nsti.n_s_t_i}_FiQuS.yaml')
            fiqus_data: DataFiQuS = yaml_to_data(fiqus_input_file_path, DataFiQuS)
            if fiqus_data.run.type in ['geometry_only']:
                return os.path.join(local_folder_prefix, f'Geometry_{fiqus_data.run.geometry}')
            elif fiqus_data.run.type in ['start_from_yaml', 'solve_with_post_process_python']:
                return os.path.join(local_folder_prefix, f'Geometry_{fiqus_data.run.geometry}', f'Mesh_{fiqus_data.run.mesh}', f'Solution_{fiqus_data.run.solution}')
        elif model.type == 'LEDET':
            pass
        elif model.type == 'PSPICE':
            pass
        elif model.type == 'XYCE':
            pass
        else:
            raise Exception(f'Software {model.type} not supported for automated running.')


    def __find_local_target_folder(self, model: Union[sim_FiQuS, sim_LEDET, sim_PSPICE, sim_XYCE]):
        '''
        Function to find the path to the local folder, which has a different logic for each simulation tool
        :param model: Current simulation model
        :return: Path to the local folder of the current simulation model
        '''

        # Define local folder
        local_folder_prefix = os.path.join(self.local_PyCoSim_folder,
                                           self.cosim_data.GeneralParameters.cosim_name,
                                           model.type)
        if model.type == 'FiQuS':
            local_folder = os.path.join(local_folder_prefix, f'{model.modelName}')
        elif model.type == 'LEDET':
            local_folder = os.path.join(local_folder_prefix, str(self.nsti.n), f'{model.modelName}')
        elif model.type in ['PSPICE', 'XYCE']:
            local_folder = os.path.join(local_folder_prefix, self.nsti.n_s_t_i, model.modelName, str(model.simulationNumber))
        local_folder = str(Path.resolve(Path(local_folder)))
        return local_folder


    def _check_convergence(self):
        """
        This functionality is not coded yet
        :return:
        :rtype:
        """
        # check whether converge criteria are met
        flag_converged = False
        return flag_converged