import requests
import json
import logging
from dataclasses import dataclass
from argparse import _SubParsersAction, ArgumentParser
from yarl import URL

from .version import get_install_dir, check_verison_override
from .search import get_manifest, fuzzy_search

logger = logging.getLogger(__name__)

global REPO_URL
REPO_URL = URL('http://18.119.133.195/niagara/')


@dataclass
class InstallArgs:
    """A class holding the passed arguments from the install parser.
    
    Attributes:
        package_name (str): Name of package to be installed
        niagara_version (str): Optional argument for version override
    """
    package_name: str
    niagara_version: str



def install_package(args: InstallArgs):
    """Installed the specified package from the repoistory.

    Args:
        args (InstallArgs): Contians the argument namespace for the install parser.
    """    

    package_name = args.package_name
    version = check_verison_override(args.niagara_version)
    install_dir = get_install_dir()
    manifest = get_manifest(version)

    logging.debug('URL with args: %s', (REPO_URL/version/package_name))

    if package_name in manifest:
        files = manifest[package_name]['files']

        logging.debug('Files queued for download: %s', ' '.join(files))
        for file_name in files:
            response_package = requests.get(REPO_URL/version/file_name)
            if response_package.status_code == 200:
                with open(install_dir/file_name, 'wb') as file:
                    file.write(response_package.content)
                logging.debug(f'Successfully installed: %s', (file_name))
                print(f'Successfully installed {file_name}')
            else:
                logging.debug(f'Failed to download file: %s', (file_name))
                print(f'Failed to download file: {response_package.status_code}')
    else:
        logging.debug('Package not found, running fuzy search.')
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
    parser_install.set_defaults(func=install_package)
