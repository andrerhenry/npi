import requests
from pathlib import Path
from argparse import _SubParsersAction, Namespace

from .main import MainNamespace

class InstallNamespace(Namespace):
    niaagara_version: str
    package_name: str

#testing 
def get_request(args: MainNamespace):
    repo_url = Path('http://18.119.133.195/')
    url = 'http://18.119.133.195/public_html/testfile.txt'
    response = requests.get(url)
    args.package_name

    if response.status_code == 200:
        with open('file.txt', 'wb') as file:
            file.write(response.content)
        print('File downloaded successfully')
    else:
        print('Failed to download file')



def add_install_parser(subparsers: _SubParsersAction) -> _SubParsersAction:
    """ Adds install parser action to subparsers object

    Args:
        subparsers (_SubParsersAction): Base subparser

    Returns:
        _SubParsersAction: a subarpse with added install action
    """    
    parser_install = subparsers.add_parser(name='install', help='list packages to be installed')
    parser_install.add_argument('niagara_version')
    parser_install.add_argument('package_name')
    parser_install.set_defaults(func=get_request)



if __name__ == '__main__':
    # testing veriables 
    repo_url = Path('http://18.119.133.195/')
    folder_name = 'public_html'
    file_name = 'testfile.txt'
    url = repo_url.joinpath(folder_name,file_name)
    
    print(url)
    
    #get_request((repo_url + folder_name),)