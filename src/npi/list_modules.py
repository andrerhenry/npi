import os
from pathlib import Path

def list() -> None:
    base_path = Path(os.getcwd()) / "mock_install"
    niagara_folder = "Niagara-4.14.0.162"
    install_dir = base_path / niagara_folder / "modules"

    print("listing installed packages")
    print(install_dir)
    print(os.listdir(install_dir))

if __name__ == "__main__":
    list()