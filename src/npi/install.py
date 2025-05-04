import requests
import logging

from pathlib import Path
from dataclasses import dataclass
from argparse import _SubParsersAction, ArgumentParser
from yarl import URL

from npi.version import get_install_dir, check_verison_override
from npi.search import get_manifest, fuzzy_search

logger = logging.getLogger(__name__)

global REPO_URL
REPO_URL = URL('http://18.119.133.195/niagara/')


@dataclass
class InstallArgs:
    """A class holding the passed arguments from the install parser.
    
    Attributes:
        package_name (str): Name of package to be installed
        niagara_version (str): Optional argument for version override
        path_override(str): Optional argument for install target direcotry
    """
    package_name: str
    niagara_version: str
    path_override: str


def install_file(file_name: str, version: str, install_dir: str) -> None:
    response_package = requests.get(REPO_URL/version/file_name)
    
    if response_package.status_code == 200:
        with open(install_dir/file_name, 'wb') as file:
            file.write(response_package.content)
        logging.debug(f'Successfully installed: %s', (file_name))
        print(f'Successfully installed {file_name}')
    else:
        logging.debug(f'Failed to download file: %s', (file_name))
        print(f'Failed to download file: {response_package.status_code}')


def check_path_override(path_override:str | Path | None)-> str:
    """Checks the override for target install path, if none was provided it will return the defualt path.

    Args:
        path_override (str | None): Optional path override from argument parser.

    Returns:
        str: Target install path.
    """
    if path_override:
        target_path = path_override
    else:
        target_path = get_install_dir()
    return Path(target_path)


def install_package_command(args: InstallArgs):
    """Installed the specified package from the repoistory.

    Args:
        args (InstallArgs): Contians the argument namespace for the install parser.
    """    

    package_name = args.package_name
    version = check_verison_override(args.niagara_version)
    install_dir = check_path_override(args.path_override)
    manifest = get_manifest(version)

    logging.debug('URL with args: %s', (REPO_URL/version/package_name))

    if package_name in manifest:
        files = manifest[package_name]['files']
        logging.debug('Files queued for download: %s', ' '.join(files))
        for file_name in files:
            install_file(file_name, version, install_dir)

        print(f'\n{package_name} has successfully been installed. \
              \nRestart Niagara to load package.')
        
    else:
        logging.debug('Package not found, running fuzy search.')
        # Run fuzzy search for package suggestions
        fuzzy_search(package_name, manifest.keys())


def add_install_parser(subparsers: _SubParsersAction) -> ArgumentParser:
    """ Adds package install parser action to subparsers object

    Args:
        subparsers (_SubParsersAction): Base subparser

    Returns:
        ArgumentParser: adds subarpse with added install actions
    """    
    parser_install = subparsers.add_parser(
        name='install', 
        help='Install specified package', 
        description='Install specified package')
    parser_install.add_argument('--niagara-version', type=str, metavar='<MAJOR.MINOR>', help='Override the version of niagara')
    parser_install.add_argument('package_name', type=str, help='Name of package to be installed')
    parser_install.add_argument('--path', dest='path_override', type=str, help='Override the installation install directory')
    parser_install.set_defaults(func=install_package_command)
    return parser_install
