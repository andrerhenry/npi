import os
from pathlib import Path
from collections.abc import Mapping

def list_modules(*args ) -> tuple[Mapping, Path]:

    base_path = Path(os.getcwd()) / "mock_install"
    niagara_folder = "Niagara-4.14.0.162"
    install_dir = base_path / niagara_folder / "modules"

    print("Listing installed packages for  {install} at location:")
    print(install_dir)
    module_list = os.listdir(install_dir)

    for package in module_list:
        print(package)
    return module_list, install_dir

if __name__ == "__main__":
    list_modules()

