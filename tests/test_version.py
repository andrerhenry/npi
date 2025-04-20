import pytest
from pathlib import Path

from npi.main import main
import npi.version as version
from npi.errors import NiagaraSystemDetectionError


@pytest.fixture
def sample_file(tmp_path) -> Path:
    file = tmp_path / "my_file.txt"
    file.write_text("some content")
    return file

@pytest.fixture
def version_properties_file(tmp_path):
    CONTENT = """releaseText1=Powered by Niagara 4 Framework
    releaseText2=Build 4.13.0.186
    releaseText3=Tue Jul 18 19:15:39 Coordinated Universal Time 2023
    version=4.13.0.186
    version.major=4
    version.minor=13
    version.iteration=0
    version.build=186
    startMenuFolder=Niagara 4.13.0.186
    appName=wb.exe
    displayName=Niagara"""

    version_properties = tmp_path/'version.properties'
    version_properties.write_text(CONTENT, encoding='utf-8')



@pytest.mark.parametrize("folder_name", ["EC-Net4-4.13.0.186", "Niagara-4.14.0.162"])
def test_get_niagara_path(tmp_path, folder_name):
    test_path = tmp_path / folder_name / "bin"
    test_path.mkdir(parents=True)
    assert version.get_niagara_path(test_path) == tmp_path/folder_name

    with pytest.raises(NiagaraSystemDetectionError):
        version.get_niagara_version(tmp_path)


def test_set_version_from_properties_file(tmp_path, version_properties_file):
    poperties_object = version.read_version_properties_file(tmp_path)
    version_object = version.set_version_from_properties_file(poperties_object)
    
    assert version_object.version == "4.13.0.186"
    assert version_object.major_version == 4
    assert version_object.minor_version == 13
    assert version_object.iteration_version == 0
    assert version_object.build_version == 186

