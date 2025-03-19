import os 
from pathlib import Path
from collections import namedtuple


def check_niagara_version():
    parent_dir = Path(os.getcwd()).name
    print(f'parent dir: {parent_dir}')

    if parent_dir == 'bin' or parent_dir == 'modules':
        niagra_distro = (Path(os.getcwd()).parent).name
        print(f'niagara distribution: {niagra_distro}')
        check_version(niagra_distro)



def check_version(niagara_distro:str):
    distributor = niagara_distro.split('-')[0]
    niagara_version = niagara_distro.split('-')[1]
    major_version = niagara_version.split('.')[0]
    minor_version = niagara_version.split('.')[1]
    print(distributor, niagara_version, major_version,minor_version)


check_niagara_version()