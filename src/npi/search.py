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


def search_package_local(args: PackageName) -> bool:
    """Finds the closet installed package.

    Args:
        module_name (str): Package name to search.

    Returns:
        bool: if the module is found
    """    
    # TODO change to search at server. serach with API request?
    install_dir = get_niagara_path()/'modules'
    module_list = os.listdir(install_dir)

    # Look in to droping file extention in index/search
    search_results = process.extractOne(args.package_name, module_list, scorer=fuzz.ratio)
    if args.package_name in module_list:
        print(f"Module: {args.package_name} found")
    #about 10 points for not include the file extention. rework to factor extention
    elif search_results[1] >= 75:
        print(f"Closet module is {search_results[0]}")
    else:
        print('Module not found.')
        return
    return True


def fuzzy_search(package_name: str, version: str) -> str | None:
    """Finds the closet named module in repo when excapt package is not found.

    Args:
        module_name (str): Package name to search.

    Returns:
        str: closest named module, or None if a similar named package is not avaible.
    """
    package_list = get_manifest(version).keys()
    search_results = process.extractOne(package_name, package_list, scorer=fuzz.ratio)

    if search_results[1] >= 90:
        closest_package = search_results[0]
        print("Package not found.")
        print(f"Did you mean: {closest_package}?")
    elif search_results[1] >= 60:
        closest_package = search_results[0]
        print("Package not found.")
        print(f"Closet package is {closest_package}")
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

