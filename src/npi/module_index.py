import os
from argparse import _SubParsersAction, ArgumentParser
from pathlib import Path
from collections.abc import Mapping

from rapidfuzz import fuzz, process

from .version import get_niagara_path


def get_install_dir() -> Path:
    """Return the return installation directory releitivly from the currenty path

    Returns:
        Path: instaallation directory
    """    
    # temp func? move to version module?
    base_path = Path(os.getcwd()) / "mock_install"
    niagara_folder = "Niagara-4.14.0.162"
    install_dir = base_path / niagara_folder / "modules"
    return install_dir


def list_modules(args) -> Mapping:
    """Returns and prints the modules installed.

    Args:
        args (argparse.Namespace)): Parsed command-line arguments (unused).

    Returns:
        Mapping: List of modules installed.
    """    
    if not (niagara_path := get_niagara_path()):
        #TODO error
        print('Modules folder not recognised.')
        return
    
    install_dir = niagara_path/'modules'
    module_list = os.listdir(install_dir)
    print("Listing installed packages for {install} at location:")
    print(install_dir)

    for package in module_list:
        print(package)

    return module_list


def find_module(module_name: str) -> bool:
    """Finds the closed named module 

    Args:
        module_name (str): moudle to be installed

    Returns:
        bool: if the module is found
    """    
    install_dir = get_install_dir()
    module_list = os.listdir(install_dir)

    # Look in to droping file extention in index/search
    search_results = process.extractOne(module_name, module_list, scorer=fuzz.ratio)
    # check should be index [0]?
    print(search_results[1])
    if module_name in module_list:
        print(f"Module: {module_name} found")
    elif search_results[1] >= 80:
        print(f"Closet module is {search_results[0]}")
    return True


def add_list_parsers(subparsers: _SubParsersAction) -> ArgumentParser:
    """Lists the installed modules

    Args:
        subparsers (_SubParsersAction): Base subparser

    Returns:
        ArgumentParser: subparser with list subparser
    """
    parser_list = subparsers.add_parser('list', help='lists the current installed modules')
    parser_list.set_defaults(func=list_modules)
    

if __name__ == "__main__":
    # Lines to test module 
    list_modules()
    find_module("somemodule2")

