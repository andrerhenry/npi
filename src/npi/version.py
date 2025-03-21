import os 
from pathlib import Path
from dataclasses import dataclass

@dataclass
class NiagaraVersion:
    """A Class holding current niagara version information
    
    Attributes:
        distributor (str): Distributor name
        major_version (int): Major version number
        minor_version (int): minor version number
        patch_version (int): Patch version number
    """
    distributor: str
    major_version: int
    minor_version: int
    patch_version: int



def check_niagara_version():
    parent_dir = Path(os.getcwd()).name
    print(f'parent dir: {parent_dir}')

    if parent_dir == 'bin' or parent_dir == 'modules':
        niagra_distro = (Path(os.getcwd()).parent).name
        print(f'niagara distribution: {niagra_distro}')
        check_version(niagra_distro)



def check_version(niagara_distro:str) -> NiagaraVersion:
    """Returns the distributor and version of the niagara distribution

    Args:
        niagara_distro (str): File string of the folder containing the niagara distrobution

    Returns:
        NiagaraVersion: Data class contianing the distributor and version numbers
    """    
    distributor = niagara_distro.split('-')[0]
    version = niagara_distro.split('-')[1]
    # add error catching to make sure sure versino information is parsed correctly?
    major_version = version.split('.')[0]
    minor_version = version.split('.')[1]
    patch_version = version.split('.')[2]
    return NiagaraVersion(distributor, major_version, minor_version, patch_version)

