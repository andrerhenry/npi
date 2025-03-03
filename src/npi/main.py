import os 
import argparse

from .list_modules import list_packages

# Temp path to local dir for testing 
global REPO_PATH

def install(args):
    print(f"looking for {args.package}")

        

def main():
    parser = argparse.ArgumentParser(prog='npi', description='niagara package installer')
    subparsers = parser.add_subparsers(required=False, help='subcommand help')

    parser_install = subparsers.add_parser(name='install', help='list packages to be installed')
    parser_install.add_argument('package')
    parser_install.set_defaults(func=install)

    
    parser_list = subparsers.add_parser('list')
    #parser.add_argument('list', help='list current installed pakcages')
    parser_list.set_defaults(func=list_packages)
    
    args = parser.parse_args()
    args.func(args)


    







if __name__ == "__main__":
    main()
    