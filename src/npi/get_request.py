import requests
from argparse import _SubParsersAction, ArgumentParser


# def get_request(url: str, file_path: str):
#     url = 'http://18.119.133.195/public_html/testfile.txt'
#     response = requests.get(url)

#     if response.status_code == 200:
#         with open(file_Path, 'wb') as file:
#             file.write(response.content)
#         print('File downloaded successfully')
#     else:
#         print('Failed to download file')

#testing 
def get_request(*args):
    url = 'http://18.119.133.195/public_html/testfile.txt'
    response = requests.get(url)

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
    parser_install.add_argument('package_name')
    parser_install.set_defaults(func=get_request)






if __name__ == '__main__':
    url = 'http://18.119.133.195/public_html/testfile.txt'
    file_Path = '/tmp/testing_download.txt'
    
    get_request(url, file_Path)