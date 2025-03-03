import os 
import argparse

# Temp path to local dir for testing 
global REPO_PATH

def install(package):
    print(f"looking for {package}")

def list() -> None:
        print("listing installed packages")

def main():
    parser = argparse.ArgumentParser(prog='npi', description='niagara package installer')
    subparsers = parser.add_subparsers(help='subcommand help')

    parser_install = subparsers.add_parser(name='install', help='list packages to be installed')
    parser_install.add_argument('package')
    args_install = parser.parse_args()
    package = args_install.package
    install(package)

    
    parser.add_argument('-l', '--list', help='list current installed pakcages')
    args = parser.parse_args()

    







if __name__ == "__main__":
    main()
    