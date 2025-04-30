import os
import requests
import json
import logging
from argparse import _SubParsersAction, ArgumentParser
from dataclasses import dataclass
from collections.abc import Iterable

from rapidfuzz import fuzz, process
from yarl import URL

from .version import get_niagara_path, check_verison_override
from .errors import GetPackageManifestError

logger = logging.getLogger(__name__)

global REPO_URL
REPO_URL = URL('http://18.119.133.195/niagara/')

@dataclass
class SearchArgs:
    """Class holding the passed arguments from the search parser.
    
    Attributes:
        package_name (str): Name of package to be installed
        niagara_version (str): Optional argument for version override
        local (bool): flag to chagne to local search

    """    
    package_name:str
    niagara_version:str
    local:bool



def get_manifest(version: str) -> dict:
    """Gets the reposistory manifest of all packages for the specified version.

    Args:
        version (str): version of niagaara in MAJOR.MINOR format

    Returns:
        dict: package manifest with meta data
    """
    # TODO change str to version type
    logging.debug('Getting manifest at URL: %s', (REPO_URL/version))
    
    response_manifest = requests.get(str(REPO_URL/version/'manifest.json'))

    if response_manifest.status_code == 200:
        manifest = json.loads(response_manifest.content.decode('UTF-8'))
    else:
        logging.debug(f'Failed to download manifest from vresion: %s', (version))
        raise GetPackageManifestError("Error with Package Manifest. " \
        "Error is likey at the server, not with local npi.")

    manifest = json.loads(response_manifest.content.decode('UTF-8'))
    return manifest


def search_package_local(package_name: str) -> None:
    """Searches the installed files for the specified package.

    Args:
        package_name (str): Package name to search.
    """    
    # TODO change to search at server. serach with API request?
    install_dir = get_niagara_path()/'modules'
    package_list = os.listdir(install_dir)

    if package_name in package_list:
        print(f'Package {package_name} is installed.')
    else:
        fuzzy_search(package_name, package_list)
    return 


def search_package_repo(package_name: str, version: str) -> str | None:
    """Finds the closet named package in the repository repo when excapt package is not found.

    Args:
        package_name (str): Package name to search.

    Returns:
        str | None: closest named package, or None if a similar named package is not avaible.
    """
    package_list = get_manifest(version).keys()
    if package_name in package_list:
        print(f'Package {package_name} is available for install.')
        return package_name
    else:
        return fuzzy_search(package_name, package_list)


def fuzzy_search(package_name: str, package_list: Iterable[str]) -> str | None:
    """Finds the closet named package in iterable list, and None when package is not found.

    Args:
        package_name (str): Package name to search.

    Returns:
        str: closest named package, or None if a similar named package is not avaible.
    """
    search_results = process.extractOne(package_name, package_list, scorer=fuzz.ratio)

    if search_results[1] >= 90:
        closest_package = search_results[0]
        print("Package not found.")
        print(f"Did you mean: {closest_package}?")
    elif search_results[1] >= 60:
        closest_package = search_results[0]
        print("Package not found.")
        print(f"Closest package is {closest_package}")
    else:
        print('Package not found.')
        return None
    return closest_package


def search_command(args: SearchArgs):
    if args.local:
        search_package_local(args.package_name)
    else:
        version = check_verison_override(args.niagara_version)
        search_package_repo(args.package_name, version)
    return


def add_search_parsers(subparsers: _SubParsersAction) -> ArgumentParser:
    """Search for the package specified. 

    Args:
        subparsers (_SubParsersAction): Base subparser

    Returns:
        ArgumentParser: subparser with search subparser
    """
    parser_search = subparsers.add_parser(
        'search', 
        help='Searches the repository for the specified package.', 
        description='Search for the specified pakcage.')
    parser_search.add_argument('package_name', type=str)
    parser_search.set_defaults(func=search_command)

    group = parser_search.add_mutually_exclusive_group()
    group.add_argument('-nv', '--niagara-version', type=str, metavar='<MAJOR.MINOR>', help='Override the version of niagara in search.')
    group.add_argument('-l', '--local', action='store_true', help='Changes search to search local packages.')
    return parser_search

