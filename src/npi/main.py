import os 
from argparse import ArgumentParser

from .module_index import list_modules
from .get_request import add_install_parser, InstallNamespace

# Temp path to local dir for testing 
global REPO_PATH

def install(args):
    print(f"looking for {args.package}")

class MainNamespace(InstallNamespace):
    pass
        

def main():
    parser = ArgumentParser(prog='npi', description='niagara package installer')
    subparsers = parser.add_subparsers(required=False, help='subcommand help')

    # parser_install = subparsers.add_parser(name='install', help='list packages to be installed')
    # parser_install.add_argument('package')
    # parser_install.set_defaults(func=install)
    install_parser = add_install_parser(subparsers)

    
    parser_list = subparsers.add_parser('list')
    #parser.add_argument('list', help='list current installed pakcages')
    parser_list.set_defaults(func=list_modules)
    
    args = parser.parse_args()
    args.func(args)


    







if __name__ == "__main__":
    main()
    