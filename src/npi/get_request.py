import requests
from pathlib import Path
from dataclasses import dataclass
from argparse import _SubParsersAction, ArgumentParser, Namespace
from yarl import URL

from .version import get_niagara_version

@dataclass
class InstallArgs:
    """A class holding the passed arguments passed from the install parser
    
    Attributes:
        package_name (str): Name of package to be installed
        niagara_version (str): Optional argument 
    """
    package_name: str
    niagara_version: str


def get_request(args: InstallArgs):
    """Installed the deisgnated package from the repoistory

    Args:
        args (InstallArgs): Contians the argument namespace for the install parser.
    """    
    repo_url = URL('http://18.119.133.195/niagara/')
    file_name = args.package_name

    if args.niagara_version:
        version = args.niagara_version
        # Debug
        print(f'Debug: from --niagara-version version: {version}')
    else:
        version_info = get_niagara_version()
        version = version_info.major_version + '.' +version_info.minor_version
        # Debug
        print(f'Debug: from get_niagara_version version: {version}')
    folder_name = version
    
    # Debug line
    print(repo_url/folder_name/file_name)

    response = requests.get(repo_url/folder_name/file_name)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f'Successfully installed {args.package_name}')
    else:
        print(f'Failed to download file: {response.status_code}')



def add_install_parser(subparsers: _SubParsersAction) -> ArgumentParser:
    """ Adds package install parser action to subparsers object

    Args:
        subparsers (_SubParsersAction): Base subparser

    Returns:
        ArgumentParser: adds subarpse with added install actions
    """    
    parser_install = subparsers.add_parser(name='install', help='list packages to be installed')
    parser_install.add_argument('--niagara-version', type=str)
    parser_install.add_argument('package_name', type=str)
    parser_install.set_defaults(func=get_request)



if __name__ == '__main__':
    # testing veriables 
    repo_url = URL('http://18.119.133.195/')
    folder_name = 'public_html'
    file_name = 'testfile.txt'
    #url = repo_url.joinpath(folder_name,file_name)
    print(repo_url/folder_name/file_name)
    print(type(repo_url/folder_name/file_name))
    
    print(repo_url.__str__)

    response = requests.get(repo_url/folder_name/file_name)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print('File downloaded successfully')
    #get_request((repo_url + folder_name),)