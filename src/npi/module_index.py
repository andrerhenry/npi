import os
from pathlib import Path
from collections.abc import Mapping

from rapidfuzz import fuzz, process


def get_install_dir() -> Path:
    base_path = Path(os.getcwd()) / "mock_install"
    niagara_folder = "Niagara-4.14.0.162"
    install_dir = base_path / niagara_folder / "modules"
    return install_dir


def list_modules(*args ) -> Mapping:
    install_dir = get_install_dir()
    module_list = os.listdir(install_dir)

    print("Listing installed packages for {install} at location:")
    print(install_dir)

    for package in module_list:
        print(package)

    return module_list


def find_module(module_name: str) -> bool:
    install_dir = get_install_dir()
    module_list = os.listdir(install_dir)

    # Look in to droping file extention in index/search
    search_results = process.extractOne(module_name, module_list, scorer=fuzz.ratio)
    print(search_results[1])
    if module_name in module_list:
        print(f"Module: {module_name} found")
    elif search_results[1] >= 80:
        print(f"Closet module is {search_results[0]}")
    return  True


if __name__ == "__main__":
    # Lines to test module 
    list_modules()
    find_module("somemodule2")

