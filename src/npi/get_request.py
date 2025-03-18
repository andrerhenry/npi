import requests
from pathlib import Path
from argparse import _SubParsersAction, ArgumentParser, Namespace
from yarl import URL

class InstallNamespace(Namespace):
    niagara_version: str
    package_name: str


def get_request(args: InstallNamespace):
    repo_url = URL('http://18.119.133.195/niagara/')
    folder_name = args.niagara_version
    file_name = args.package_name


    response = requests.get(repo_url/folder_name/file_name)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print('File downloaded successfully')
    else:
        print('Failed to download file')



def add_install_parser(subparsers: _SubParsersAction) -> ArgumentParser:
    """ Adds install parser action to subparsers object

    Args:
        subparsers (_SubParsersAction): Base subparser

    Returns:
        _SubParsersAction: a subarpse with added install action
    """    
    parser_install = subparsers.add_parser(name='install', help='list packages to be installed')
    parser_install.add_argument('--niagara_version', type=str)
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