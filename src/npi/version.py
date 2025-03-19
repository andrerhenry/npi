import os 
from pathlib import Path


def check_niagara_version():
    parent_dir = Path(os.getcwd()).name
    print(f'parent dir: {parent_dir}')

    if parent_dir == 'bin' or parent_dir == 'modules':
        niagra_distro = (Path(os.getcwd()).parent).name
    print(f'niagara distribution: {niagra_distro}')



check_niagara_version()