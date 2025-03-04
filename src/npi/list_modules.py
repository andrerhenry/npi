import os
from pathlib import Path

def list_packages(*args ) -> None:

    base_path = Path(os.getcwd()) / "mock_install"
    niagara_folder = "Niagara-4.14.0.162"
    install_dir = base_path / niagara_folder / "modules"

    print("Listing installed packages for  {install} at location:")
    print(install_dir)
    package_list = os.listdir(install_dir)
    
    for package in package_list:
        print(package)

if __name__ == "__main__":
    list_packages()