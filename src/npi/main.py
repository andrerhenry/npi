import os 
from argparse import ArgumentParser
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
logger.info('LoggingStarted')

from .module_index import add_list_parsers, add_search_parsers
from .get_request import add_install_parser, InstallArgs
from .version import add_version_parser

# Temp path to local dir for testing 
global REPO_PATH



def main():
    parser = ArgumentParser(prog='npi', description='niagara package installer')
    subparsers = parser.add_subparsers(required=False, help='subcommand help')

    install_parser = add_install_parser(subparsers)
    version_parser = add_version_parser(subparsers)
    list_parser = add_list_parsers(subparsers)
    search_parser = add_search_parsers(subparsers)

    args = parser.parse_args()
    args.func(args)




if __name__ == "__main__":
    main()
    