import os
from argparse import _SubParsersAction, ArgumentParser
from pathlib import Path
from collections.abc import Mapping
from typing import NamedTuple
from rapidfuzz import fuzz, process

from .version import get_niagara_path, get_install_dir, get_niagara_version

class PackageName(NamedTuple):
    package_name:str



def list_modules_local(args) -> Mapping:
    """Returns and prints the modules installed in the Niagara modules direcotry.

    Args:
        args (argparse.Namespace)): Parsed command-line arguments (unused).

    Returns:
        Mapping: List of modules installed.
    """    
    install_dir = get_install_dir()
    module_list = os.listdir(install_dir)
    print(f"Listing installed packages at location:")
    print(install_dir, '\n')

    for package in module_list:
        print(package)

    return module_list


def find_module(args: PackageName) -> bool:
    """Finds the closet named module.

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


def add_list_parsers(subparsers: _SubParsersAction) -> ArgumentParser:
    """Lists the installed modules

    Args:
        subparsers (_SubParsersAction): Base subparser

    Returns:
        ArgumentParser: subparser with list subparser
    """
    parser_list = subparsers.add_parser(
        'list', 
        help='Lists the current installed modules', 
        description='Lists the current installed modules')
    parser_list.set_defaults(func=list_modules_local)
    
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
    parser_list.set_defaults(func=find_module)

