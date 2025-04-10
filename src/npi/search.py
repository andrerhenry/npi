import os
import requests
import json
import logging
from argparse import _SubParsersAction, ArgumentParser
from typing import NamedTuple

from rapidfuzz import fuzz, process
from yarl import URL

from .version import get_niagara_path
from .npi_errors import GetPackageManifestError

logger = logging.getLogger(__name__)

global REPO_URL
REPO_URL = URL('http://18.119.133.195/niagara/')

class PackageName(NamedTuple):
    package_name:str


def get_manifest(version: str) -> dict:
    """Gets the reposistory manifest of all packages for the specified version.

    Args:
        version (str): version of niagaara in MAJOR.MINOR format

    Returns:
        dict: package manifest with meta data
    """
    # TODO change str to version type
    logging.debug('Getting manifest at URL: %s', (REPO_URL/version))
    
    response_manifest = requests.get(REPO_URL/version/'manifest.json')

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
        module_name (str): Package name to search.

    Returns:
        str: closest named module, or None if a similar named package is not avaible.
    """
    package_list = get_manifest(version).keys()
    if package_name in package_list:
        print(f'Package {package_name} is availbe for install.')
    else:
        closest_package = fuzzy_search(package_name, package_list)
    return closest_package



def fuzzy_search(package_name: str, package_list: list [str]) -> str | None:
    """Finds the closet named module in repo when excapt package is not found.

    Args:
        module_name (str): Package name to search.

    Returns:
        str: closest named module, or None if a similar named package is not avaible.
    """
    search_results = process.extractOne(package_name, package_list, scorer=fuzz.ratio)



def fuzzy_search(package_name: str, package_list: list [str]) -> str | None:
    """Finds the closet named module in repo when excapt package is not found.

    Args:
        module_name (str): Package name to search.

    Returns:
        str: closest named module, or None if a similar named package is not avaible.
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
        print('Module not found.')
        return None
    return closest_package



def add_search_parsers(subparsers: _SubParsersAction) -> ArgumentParser:
    """Search for the module specified. 

    Args:
        subparsers (_SubParsersAction): Base subparser

    Returns:
        ArgumentParser: subparser with search subparser
    """
    parser_list = subparsers.add_parser(
        'search', 
        help='Search for the module specified', 
        description='Search for the module specified')
    parser_list.add_argument('package_name', type=str)
    parser_list.set_defaults(func=search_package_local)

