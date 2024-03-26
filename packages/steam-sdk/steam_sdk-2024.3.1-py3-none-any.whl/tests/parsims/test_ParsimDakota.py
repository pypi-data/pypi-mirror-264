import unittest
import os

from steam_sdk.parsims.ParsimDakota import ParsimDakota

class TestParsimDakota(unittest.TestCase):
    """
    Test for testing parametric Dakota simulations with given analysis file that runs a single tool. No multiple tools or co-simulation tests are implemented for now.
    """
    def setUp(self) -> None:
        """
            This function is executed before each test in this class
        """
        self.current_path = os.getcwd()
        self.test_folder = os.path.dirname(__file__)
        # os.chdir(self.test_folder)  # move to the directory where this file is located
        print('\nCurrent folder:          {}'.format(self.current_path))
        print('\nTest is run from folder: {}'.format(os.getcwd()))


    def tearDown(self) -> None:
        """
            This function is executed after each test in this class
        """
        os.chdir(self.current_path)  # go back to initial folder

    def test_ParsimDakota_FiQuS_MQXA_multidim_parameter_study(self):
        dakota_yaml_path = os.path.join(self.test_folder, 'input', 'parsim_dakota', "TestFile_ParsimDakota_FiQuS_MQXA_multidim_parameter_study.yaml")
        ParsimDakota(input_DAKOTA_yaml=dakota_yaml_path)

    def test_ParsimDakota_LEDET_SMC_multidim_parameter_study(self):
        dakota_yaml_path = os.path.join(self.test_folder, 'input', 'parsim_dakota', "TestFile_ParsimDakota_LEDET_SMC_multidim_parameter_study.yaml")
        ParsimDakota(input_DAKOTA_yaml=dakota_yaml_path)

    def test_ParsimDakota_XYCE_RSS_parameter_study(self): # RSS is rather well performing in XYCE
        dakota_yaml_path = os.path.join(self.test_folder, 'input', 'parsim_dakota', "TestFile_ParsimDakota_XYCE_RSS_multidim_parameter_study.yaml")

        # The working directory is changed to tempDakota during the test so we can not specify the input file for
        #  run parsim event circuit with a relative path. Thats why an absolute path is specified in the analysis yaml file
        # which is adapted using the user_name so it works on differnt machines.
        # TODO: Find a better solution for this
        path_analysis_yamlfile = os.path.abspath(os.path.join(self.test_folder, 'input', 'parsim_dakota', "TestFile_AnalysisSTEAM_XYCE.yaml"))
        user_name = os.getlogin()
        with open(path_analysis_yamlfile, 'r') as file:
            yaml_content = file.read()
        updated_content = yaml_content.replace("user_name", user_name)
        file_path_updated_yaml = os.path.join(os.path.dirname(path_analysis_yamlfile), os.path.basename(path_analysis_yamlfile).split(".")[0] + "_updated.yaml")
        # Write the updated content to a new file
        with open(file_path_updated_yaml, 'w') as file:
            file.write(updated_content)

        ParsimDakota(input_DAKOTA_yaml=dakota_yaml_path)

