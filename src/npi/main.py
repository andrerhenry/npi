import os 
from argparse import ArgumentParser
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)
logger.info('LoggingStarted')

from .list import add_list_parsers
from .search import add_search_parsers
from .install import add_install_parser
from .version import add_version_parser, npi_version
from .errors import NiagaraSystemDetectionError, GetPackageManifestError

# Temp path to local dir for testing 
global REPO_PATH


def main():
    try:
        parser = ArgumentParser(prog='npi', 
                                description='Niagara package installer helps you install and manage '
                                'Niagara packages.')
        parser.add_argument('--version', action='version', version=npi_version())

        subparsers = parser.add_subparsers(title='subcommands', dest='subcommands', metavar='', required=False)
        install_parser = add_install_parser(subparsers)
        version_parser = add_version_parser(subparsers)
        list_parser = add_list_parsers(subparsers)
        search_parser = add_search_parsers(subparsers)

        args = parser.parse_args()
        args.func(args)
    except NiagaraSystemDetectionError as error:
        print(error)
    except GetPackageManifestError as error:
        print(error)


if __name__ == "__main__":
    main()
    