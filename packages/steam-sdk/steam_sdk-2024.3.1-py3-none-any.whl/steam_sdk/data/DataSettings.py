from pydantic import BaseModel
from typing import Optional

class DataSettings(BaseModel):
    """
        Dataclass of settings for STEAM analyses
        This will be populated either form a local settings file (if flag_permanent_settings=False)
        or from the keys in the input analysis file (if flag_permanent_settings=True)
    """
    comsolexe_path:        Optional[str] = None  # full path to comsol.exe, only COMSOL53a is supported
    JAVA_jdk_path:         Optional[str] = None  # full path to folder with java jdk
    CFunLibPath:           Optional[str] = None  # full path to dll files with material properties
    ANSYS_path:            Optional[str] = None  # full path to ANSYS executable
    COSIM_path:            Optional[str] = None  # full path to STEAM-COSIM executable
    Dakota_path:           Optional[str] = None  # full path to Dakota executable
    FiQuS_path:            Optional[str] = None  # Full path to FiQuS repository (FiQuS or FiQuS-dev should work)
    GetDP_path:            Optional[str] = None  # Full path to getdp.exe (OneLab or CERN builds should work)
    LEDET_path:            Optional[str] = None  # full path to STEAM-LEDET executable
    ProteCCT_path:         Optional[str] = None  # full path to STEAM-ProteCCT executable
    PSPICE_path:           Optional[str] = None  # full path to PSPICE executable
    PyBBQ_path:            Optional[str] = None  #
    XYCE_path:             Optional[str] = None  #
    PSPICE_library_path:   Optional[str] = None  #
    MTF_credentials_path:  Optional[str] = None  # full path to the txt file containing the credentials for MTF login
    local_library_path:    Optional[str] = None  # relative or absolute path to local STEAM library folder
    local_ANSYS_folder:    Optional[str] = None  # full path to local ANSYS folder
    local_COSIM_folder:    Optional[str] = None  # full path to local COSIM folder
    local_Dakota_folder:   Optional[str] = None  # full path to local Dakota folder
    local_FiQuS_folder:    Optional[str] = None  # full path to local FiQuS folder
    local_LEDET_folder:    Optional[str] = None  # full path to local LEDET folder
    local_ProteCCT_folder: Optional[str] = None  # full path to local ProteCCT folder
    local_PSPICE_folder:   Optional[str] = None  # full path to local PSPICE folder
    local_PyBBQ_folder:    Optional[str] = None  # full path to local PyBBQ folder
    local_PyCoSim_folder:  Optional[str] = None  # full path to local PyCoSim folder
    local_SIGMA_folder:    Optional[str] = None  # full path to local SIGMA folder
    local_XYCE_folder:     Optional[str] = None  # full path to local PSPICE folder

