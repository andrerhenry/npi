import requests
import logging
from dataclasses import dataclass
from argparse import _SubParsersAction, ArgumentParser
from yarl import URL

from .version import get_niagara_version, check_verison_override

logger = logging.getLogger(__name__)

@dataclass
class InstallArgs:
    """A class holding the passed arguments passed from the install parser
    
    Attributes:
        package_name (str): Name of package to be installed
        niagara_version (str): Optional argument 
    """
    package_name: str
    niagara_version: str


def install_package(args: InstallArgs):
    """Installed the specified package from the repoistory

    Args:
        args (InstallArgs): Contians the argument namespace for the install parser.
    """    
    repo_url = URL('http://18.119.133.195/niagara/')
    version = check_verison_override(args.niagara_version)
    package_name = args.package_name
    
    logging.debug('URL with args: %s', (repo_url/version/package_name))

    
    response = requests.get(repo_url/version/'manifest.json')
    if response.status_code == 200:
        with open('manifest.json', 'wb') as file:
            print("got the file")
            file.write(response.content)

    response = requests.get(repo_url/version/package_name)
    if response.status_code == 200:
        with open(package_name, 'wb') as file:
            file.write(response.content)
        print(f'Successfully installed {args.package_name}')
    else:
        print(f'Failed to download file: {response.status_code}')



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
    parser_install.add_argument('--niagara-version', type=str, metavar='', help='Override the version of niagara')
    parser_install.add_argument('package_name', type=str, help='Name of package to be installed')
    parser_install.set_defaults(func=install_package)
