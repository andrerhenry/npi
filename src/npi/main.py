import os 
from argparse import ArgumentParser

from .module_index import list_modules
from .get_request import add_install_parser, InstallNamespace
from .version import add_version_parser

# Temp path to local dir for testing 
global REPO_PATH



def main():
    parser = ArgumentParser(prog='npi', description='niagara package installer')
    subparsers = parser.add_subparsers(required=False, help='subcommand help')

    install_parser = add_install_parser(subparsers)
    version_parser = add_version_parser(subparsers)

    
    parser_list = subparsers.add_parser('list')
    parser_list.set_defaults(func=list_modules)
    
    args = parser.parse_args()
    args.func(args)




if __name__ == "__main__":
    main()
    