from pydantic import BaseModel, Field

from typing import Dict, List, Union, Literal, Optional

class Bound(BaseModel):
    """
        Class for FiQuS multipole
    """
    min: Optional[float] = None
    max: Optional[float] = None


class SamplingVar(BaseModel):
    """
        Class for FiQuS multipole
    """
    bounds: Bound = Bound()


class MultiDimParStudyVar(BaseModel):
    """
        Class for FiQuS multipole
    """
    data_points: Optional[int] = None
    bounds: Bound = Bound()

class OptppQNewtonParStudyVar(BaseModel):
    """
        Class for FiQuS multipole
    """
    initial_point: float = Field(default=None, description="Smart sentence from dakota manual")
    bounds: Bound = Bound()
    #descriptors: str = Field(default=None, description="Smart sentence from dakota manual")

class Sampling(BaseModel):
    """
        Class for FiQuS multipole
    """
    type: Literal['sampling']
    samples: Optional[int] = None
    seed: Optional[int] = None
    response_levels: Optional[float] = None
    variables: Dict[str, SamplingVar] = {}


class MultiDimParStudy(BaseModel):
    """
        Class for FiQuS multipole
    """
    type: Literal['multidim_parameter_study']
    variables: Dict[str, MultiDimParStudyVar] = {}

class OptppQNewton(BaseModel):
    """
        Class for FiQuS multipole
    """
    type: Literal['optpp_q_newton']
    convergence_tolerance: float = Field(default=None, description="Smart sentence from dakota manual")
    variables: Dict[str, OptppQNewtonParStudyVar] = {}
    #samples: Optional[int] = None
    #seed: Optional[int] = None

    #response_levels: Optional[float] = None


class Response(BaseModel):
    """
        Class for FiQuS multipole
    """
    response: Optional[str] = None  # Union[ResponseFunction, ObjectiveFunction] = {'type': 'response_functions'}
    descriptors: Optional[List[str]] = None


# First Level
class DataModelParsimDakota(BaseModel):
    parsim_name: str = Field(default=None, description="Name of the study. This is folder name in which the files will be saved in the local_Dakota_folder")
    sim_number_offset: int = Field(default=None, description="This number is added to the simulation numbers used by the tool and Dakota. THis is to enable not overwriting simulations in the tool folder")
    evaluation_concurrency: int = Field(default=None, description="Number of concurrent executions. ")
    study: Union[MultiDimParStudy, Sampling, OptppQNewton] = {'type': 'multidim_parameter_study'}
    responses: Response = Response()
    analysis_yaml_file_name: str = Field(default=None, description="name of analysis file to use in Dakota simulation, for the moment, the file needs to be in the same folder as Dakota input yaml")
    initial_steps_list: List[str] = Field(default=None, description="List of initial steps to be performed before Dakota is running (looping)")
    iterable_steps_list: List[str] = Field(default=None, description="List of steps to repeat in the analysis when Dakota is running (looping)")
    python_path_dakota: str = Field(default="python.exe", description="Path to the python.exe, that Dakota should use for running driver_link.py")

# from steam_sdk.data.DataAnalysis import WorkingFolders
# from steam_sdk.data.DataSettings import DataSettings

### SUB-SUB-LEVEL
# class interface(BaseModel):
#     analysis_drivers: str = ''
#     fork: Optional[str] = None
#     interface_arguments: Dict = {}
#
#
# class responses(BaseModel):
#     response_functions: int = 0
#     descriptors: Optional[List[str]] = None
#     objective_functions: int = 0
#     nonlinear_inequality_constraints: int = 0
#     calibration_terms: int = 0
#     type_gradients: str = ''
#     numerical_gradients: Dict = {}
#     analytical_gradients: Dict = {}
#     no_gradients: bool = False
#     no_hessians: bool = False
#
#
# class variables(BaseModel):
#     type_variable: str = ''
#     variable_arguments: Dict = {}
#
#
# class model(BaseModel):
#     type_model: str = ''
#
#
# class method(BaseModel):
#     type_method: str = ''
#     method_argument: Dict = {}
#
#
# class environment(BaseModel):
#     graphics: bool = False
#     type_tabular_data: str = ''
#     tabular_data_argument: Dict = {}
#
#
# # SUB-LEVEL
# class DAKOTA_analysis(BaseModel):
#     interface: interface = interface()
#     responses: responses = responses()
#     variables: variables = variables()
#     method: method = method()
#     model: model = model()
#     environment: environment = environment()





# Second Level: Responses
# class ObjectiveFunction(BaseModel):
#     """
#         Class for FiQuS multipole
#     """
#     #type: Literal['objective_functions']
#
#
# class ResponseFunction(BaseModel):
#     """
#         Class for FiQuS multipole
#     """
#     #type: Literal['response_functions']




