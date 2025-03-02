import os 
import argparse

# Temp path to local dir for testing 
global REPO_PATH

def main():
    parser = argparse.ArgumentParser(prog='npi', description='niagara package installer')
    subparsers = parser.add_subparsers(help='subcommand help')

    parser_install = subparsers.add_parser('install', help='list packages to be installed')
    parser_install.add_argument('package')
    args = parser.parse_args()
    package = args.package
    print(f"looking for {package}")
    




if __name__ == "__main__":
    main()
    