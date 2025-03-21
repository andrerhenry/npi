import os 
from argparse import ArgumentParser, _SubParsersAction
from pathlib import Path
from typing import NamedTuple
from dataclasses import dataclass


class Version(NamedTuple):
    """A Class holding current niagara major and minor version

    Attributes:
        major_version (int): Major version number
        minor_version (int): minor version number
    """    
    major_version: int
    minor_version: int


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


def check_niagara_version() -> Version | None:
    """Checks the niagara version information and returns major and minor version. 


    Returns:
        Version | None: Returns major minor version numbers, and None if there is an error 
    """    
    parent_dir = Path(os.getcwd()).name

    if parent_dir == 'bin' or parent_dir == 'modules':
        niagara_distro = (Path(os.getcwd()).parent).name
        print(f'niagara distribution: {niagara_distro}')
        check_version(niagara_distro)
    elif '-' in parent_dir and '.' in parent_dir:
        niagara_distro = parent_dir
        check_version(parent_dir)
    else:
        print("Niagara version not recongized.")
        print('Use commeands {} {} to force install')
        return
    version_info = check_version(niagara_distro)
    print(f'distributor: {version_info.distributor}, version:{version_info.major_version}.{version_info.minor_version}')
    return Version(version_info.major_version, version_info.minor_version)


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


def add_version_parser(subparsers: _SubParsersAction) -> ArgumentParser:
    """Addes command to show the current version of niagara detected

    Args:
        subparsers (_SubParsersAction): Base subparser

    Returns:
        ArgumentParser: subparser with version subparser
    """
    version_parser = subparsers.add_parser(name='version', help='Shows the current version of niagara detectd')
    version_parser.set_defaults(func=check_niagara_version)
