import os
from pathlib import Path


base_path = Path(os.getcwd()) / "mock_install"
niagara_folder = "Niagara-4.14.0.162"
install_dir = base_path / niagara_folder / "modules"

print(install_dir)
print(os.listdir(install_dir))