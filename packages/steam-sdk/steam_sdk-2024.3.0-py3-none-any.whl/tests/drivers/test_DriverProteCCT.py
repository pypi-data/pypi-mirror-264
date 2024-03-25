import unittest
import os
from pathlib import Path
import shutil

from steam_sdk.data.DataSettings import DataSettings
from steam_sdk.drivers.DriverProteCCT import DriverProteCCT
from steam_sdk.utils.read_settings_file import read_settings_file


class TestDriverProteCCT(unittest.TestCase):

    def setUp(self) -> None:
        """
            This function is executed before each test in this class
        """
        self.current_path = os.getcwd()
        self.test_folder = os.path.dirname(__file__)
        print('\nCurrent folder:          {}'.format(self.current_path))
        print('\nTest is run from folder: {}'.format(os.getcwd()))
        self.settings: DataSettings = read_settings_file()[1]

    def tearDown(self) -> None:
        """
            This function is executed after each test in this class
        """
        os.chdir(self.current_path)  # go back to initial folder


    def test_runProteCCT_fromCircuitLibrary_multiple(self):
        '''
            This test runs iteratively the ProteCCT netlists in the provided list.
            Each input file is copied from the local STEAM_SDK test model library.
        '''
        magnet_names = ['MCBRD']
        for magnet_name in magnet_names:
            print('Circuit: {}'.format(magnet_name))
            self.runProteCCT_fromCircuitLibrary(magnet_name = magnet_name)


    def runProteCCT_fromCircuitLibrary(self, magnet_name = 'MCBRD'):
        '''
            This test checks that ProteCCT can be run programmatically using DriverProteCCT.
            The input file is copied from the local STEAM_SDK test model library.
            The path of ProteCCT executable is set to be the one of the Gitlab runner.
            In order to run this test locally, path_exe should be changed.
        '''

        # arrange
        # Define working folder and make sure dedicated output folder exists
        software = 'ProteCCT'
        sim_number = 0
        path_folder_ProteCCT_output = Path(os.path.join(self.test_folder, self.settings.local_ProteCCT_folder)).resolve()
        path_folder_ProteCCT_input = os.path.join(path_folder_ProteCCT_output, 'input')
        print('path_folder_ProteCCT: {}'.format(path_folder_ProteCCT_input))
        if not os.path.isdir(path_folder_ProteCCT_input):
            print("Output folder {} does not exist. Making it now".format(path_folder_ProteCCT_input))
            Path(path_folder_ProteCCT_input).mkdir(parents=True)

        # Copy input file from the STEAM_SDK test model library
        file_name_input = Path(Path(self.test_folder).parent / os.path.join('builders', 'model_library', 'magnets', magnet_name, 'output', software, f'{magnet_name}_{sim_number}.xlsx')).resolve()
        name_copied = f'{magnet_name}_{software}_COPIED'
        file_name_local = os.path.join(path_folder_ProteCCT_input, f'{name_copied}.xlsx')
        shutil.copyfile(file_name_input, file_name_local)
        print(f'Simulation file {file_name_local} copied.')

        # Dictionary with manually-written expected names of ProteCCT output files (one per magnet)
        expected_file_names = {
            'MCBRD': 'MCBRD, I0=393A, TOp=1.9K, tQB=35ms, QI=0.01651, VGnd=528.3V, VEE=531.0V, addedHeCpFrac=0.006, fLoopFactor=0.8',
        }

        # Define expected output files, and delete them if they already exist
        expected_file_xls = os.path.join(path_folder_ProteCCT_output, 'output', expected_file_names[magnet_name] + '.xls')
        if os.path.isfile(expected_file_xls):
            os.remove(expected_file_xls)
            print('File {} already existed. It was deleted now.'.format(expected_file_xls))

        # Initialize Driver
        dProteCCT = DriverProteCCT(
            path_exe=self.settings.ProteCCT_path,
            path_folder_ProteCCT=path_folder_ProteCCT_output,
            verbose=True)

        # assert
        print('Expected file: {}'.format(expected_file_xls))



