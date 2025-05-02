import pytest
import shutil
import os

from argparse import ArgumentParser
from pathlib import Path

from npi.main import build_parser
from npi.search import get_manifest


@pytest.fixture
def main_parser_fixture():
        return build_parser()


@pytest.fixture()
def mock_distech_file_struc(tmp_path, hmock_file_request, monkeypatch):
    """ Creates a mock Niagara files structure for tests.
    The defulat is set to a Distech 4.13.

    """    
    base_path = Path(__file__).parent
    mock_niagara = 'EC-Net4-4.13.0.186'
    source_enviro_path = base_path/'resources'/'mock_install'/ mock_niagara

    shutil.copytree(source_enviro_path, tmp_path/mock_niagara)
    monkeypatch.chdir(tmp_path/mock_niagara)
     
    
@pytest.fixture
def set_enviro_distech_4_13(monkeypatch: pytest.MonkeyPatch):
    base_path = Path(__file__).parent
    monkeypatch.chdir(base_path/'resources'/'mock_install'/'EC-Net4-4.13.0.186')

@pytest.fixture
def set_enviro_vykon_4_14(monkeypatch: pytest.MonkeyPatch):
    base_path = Path(__file__).parent
    monkeypatch.chdir(base_path/'resources'/'mock_install'/'Niagara-4.14.0.162')


@pytest.fixture
def mock_get_manifest(monkeypatch):
    mock_manifest_data = '''
    {
    'vykonPro': {
        'files': [
        'vykonPro-ux.jar',
        'vykonPro-rt.jar',
        'vykonPro-doc.jar',
        'vykonPro-wb.jar'
        ],
        'runtimeProfiles': [
        'ux',
        'rt',
        'doc',
        'wb'
        ]
    },
    'vykonProUtil': {
        'files': [
        'vykonProUtil-doc.jar',
        'vykonProUtil-rt.jar',
        'vykonProUtil-wb.jar'
        ],
        'runtimeProfiles': [
        'doc',
        'rt',
        'wb'
        ]
    }
    }'''

    mock_manifest_data = 'Some Content for tests.'
    content_in_bytes = mock_manifest_data.encode('utf-8')
    mock_response = {'status_code': 200, 'content': content_in_bytes}
    return mock_response


@pytest.fixture
def mock_file_request():
    class MockPackageResponse:
        def __init__(self, url):
            self.status_code = 200
            self.content = ('Some Content for tests.').encode('utf-8')

    return MockPackageResponse
