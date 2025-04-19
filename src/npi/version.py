import logging
from argparse import ArgumentParser, _SubParsersAction
from pathlib import Path
from importlib.metadata import version
from dataclasses import dataclass

from jproperties import Properties

from .errors import NiagaraSystemDetectionError

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
    build_version: int | None = None

    def __post_init__(self) -> None :
        self.version_number: str = str(self.major_version) + '.' + str(self.minor_version)


def get_niagara_path(niagara_path:str | Path | None = None) -> Path:
    """Gets the Path to root directory of the niagara installation.

    Args:
        niagara_path (str | Path | None, optional): Nigara path override. Defaults to None.

    Raises:
        NiagaraSystemDetectionError: _description_

    Returns:
        Path: Path to niagara root directory.
    """
    #TODO: add override flag to parser
    niagara_path = Path(niagara_path or Path.cwd())
    parent_dir = Path(niagara_path).name
    
    if parent_dir == 'bin' or parent_dir == 'modules':
        return (niagara_path.parent)
    if '-' in parent_dir and '.' in parent_dir:
        return niagara_path
    
    raise NiagaraSystemDetectionError('Niagara System could not be detected. " \
    "Please use npi from the Niagara console or the root of Niagara file system.')


def get_install_dir() -> Path:
    """Gets the Path to modules folder of the niagara installaiton.

    Returns:
        Path: Installation directory.
    """    
    return get_niagara_path() / 'modules'


def read_version_properties_file(properties_dir: Path) -> Properties:
    """_sReads the niagara version properties files and stores data in Properties class.

    Args:
        properties_dir (Path): Path to directory of version.poperties.

    Returns:
        Properties: Data from version.poperties.
    """
    version_data= Properties()
    with open(properties_dir/"version.properties", "rb") as file:
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
        version_data.get('version').data,
        version_data.get('version.major').data,
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
    bin_path = get_niagara_path()/'bin'
    if (bin_path/'version.properties').exists():
        version = set_version_from_properties_file(read_version_properties_file(bin_path))
    else:
        niagara_distro = get_niagara_path().name
        version = set_version_from_path(niagara_distro)
    logger.debug('Version: %s.%s', version.major_version, version.minor_version)
    return version

def show_niagara_version(args) -> None:
    """Prints the Version information from the detected niagara version. 

    Args:
        args (argparse.Namespace)): Parsed command-line arguments (unused).
    """
    version_info = get_niagara_version()
    print(f'Version: {version_info.major_version}.{version_info.minor_version}')


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