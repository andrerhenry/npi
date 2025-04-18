import os 
import logging
from argparse import ArgumentParser, _SubParsersAction
from pathlib import Path
from importlib.metadata import version
from dataclasses import dataclass

from jproperties import Properties

from .errors import NiagaraSystemDectectionError

logger = logging.getLogger(__name__)

@dataclass
class NiagaraVersion:
    """A Class holding current niagara version information
    
    Attributes:
        version (str): Whole version stringe
        major_version (int): Major version number
        minor_version (int): Minor version number
        iteration_version (int): Iteration version number
        build_version (int): Build version number
        version_number(str): Version number in strings for directory paths
    """
    version: str
    major_version: int
    minor_version: int
    iteration_version: int
    build_version: int

    def __post_init__(self) -> None :
        self.version_number: str = str(self.major_version) + '.' + str(self.minor_version)


def get_niagara_path() -> Path:
    """Gets the Path to root directory of the niagara installation.

    Returns:
        Path: Path to niagara root directory.
    """
    #TODO: add override variable to overrride the path
    parent_dir = Path(os.getcwd()).name
    
    if parent_dir == 'bin' or parent_dir == 'modules':
        niagara_path = (Path(os.getcwd()).parent)
    elif '-' in parent_dir and '.' in parent_dir:
        niagara_path = Path(os.getcwd())
    else:
        raise NiagaraSystemDectectionError('Niagara System could not be detected. " \
        "Please use npi at the Niagara directory or specify the path a Niagara file system.')
    return niagara_path


def get_install_dir() -> Path:
    """Gets the Path to modules folder of the niagara installaiton.

    Returns:
        Path: Installation directory.
    """    
    return get_niagara_path() / 'modules'


def read_version_properties_file() -> Properties:
    """Reads the niagara version properties files and stores data in Properties class.

    Returns:
        Properties: Data from version.poperties
    """    
    version_data= Properties()
    properties_path = get_niagara_path()/"bin"
    with open(properties_path/"version.properties", "rb") as file:
        version_data.load(file, "utf-8")
    return version_data


def set_version_from_properties_file(version_data: Properties) -> NiagaraVersion:
    """Stores version information from version_data

    Args:
        version_data (Properties): veresion information from version.properties file.

    Returns:
        NiagaraVersion: Data class contianing the version information.
    """    
    version = NiagaraVersion(
        version_data.get('verison').data,
        version_data.get('versoin.major').data,
        version_data.get('version.minor').data,
        version_data.get('version.iteration').data,
        version_data.get('version.build').data
    )
    return version


def set_version_from_path(version_information:str) -> NiagaraVersion:
    """Stores version information of current niagara. 

    Args:
        version_information Properties: Class of raw data holding version information.

    Returns:
        NiagaraVersion: Data class contianing the version information.
    """    
    version = version_information.split('-')[-1]
    distributor = version_information.replace('-' + version, '')
    major_version = int(version.split('.')[0])
    minor_version = int(version.split('.')[1])
    patch_version = int(version.split('.')[2])
    return NiagaraVersion(distributor, major_version, minor_version, patch_version)


def get_niagara_version(args = None) -> NiagaraVersion:
    """Checks the niagara version information and returns major and minor version. 

    Args:
        args (argparse.Namespace)): Parsed command-line arguments (unused).

    Returns:
        NiagaraVersion: Returns NiagaraVersion class containing version infromation.
    """ 
    niagara_distro = get_niagara_path().name
    version_info = set_version_from_path(niagara_distro)
    logger.debug('Distributor: %s, Version: %s.%s', version_info.distributor, version_info.major_version, version_info.minor_version)
    return version_info

def show_niagara_version(args) -> None:
    """Prints the Version information from the detected niagara version. 

    Args:
        args (argparse.Namespace)): Parsed command-line arguments (unused).
    """
    version_info = get_niagara_version()
    print(f'Distributor: {version_info.distributor}, Version: {version_info.major_version}.{version_info.minor_version}')


def check_verison_override(optional_version_input:str | None)-> str:
    """checks the override version input, if none was provided it will return the detected version

    Args:
        optional_version_input (str | None): Optional version override from argument parser.

    Returns:
        str: Niagara version string.
    """
    if optional_version_input:
        version = optional_version_input
        logger.debug('From --nagara-version %s', version)
    else:
        version_info = get_niagara_version()
        version = str(version_info.major_version) + '.' + str(version_info.minor_version)
        logger.debug('From get_niagara_version %s', version)
    return version


def add_version_parser(subparsers: _SubParsersAction) -> ArgumentParser:
    """Addes command to show the current version of niagara detected.

    Args:
        subparsers (_SubParsersAction): Base subparser to be modified.

    Returns:
        ArgumentParser: Subparser with version subparser added.
    """
    version_parser = subparsers.add_parser(
        name='version', 
        help='Shows the current version of niagara detected', 
        description='Shows the current version of niagara detected')
    version_parser.set_defaults(func=show_niagara_version)
    return version_parser


def npi_version() -> str:
    """Gets and displays the programs version information.

    Returns:
        str: Program version information message.
    """    
    return f'npi version installed {version('npi')}'