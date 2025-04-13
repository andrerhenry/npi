import os
from argparse import _SubParsersAction, ArgumentParser
from collections.abc import Mapping

from .version import get_install_dir

def list_modules_local(args) -> list[str]:
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
    return parser_list