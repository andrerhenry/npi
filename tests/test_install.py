import os
import pytest
import requests
from pathlib import Path
from pytest_mock import mocker

from npi.install import install_file
from tests.conftest import MockPackageResponse

@pytest.fixture
def mock_file_request():
    content = 'Some Content for tests.'
    content_in_bytes = content.encode('utf-8')
    #mock_response = {'status_code': 200, 'content': content_in_bytes}
    mock_response = MockPackageResponse(200, content)
    return mock_response

def test_install_file(tmp_path):
    file_name = 'vykonPro-rt.jar'
    version = '4.13'
    test_install_path = Path(__file__).parent/'resources'/'mock_install'/'EC-Net4-4.13.0.186'/'modules'
    # Test actually install files, mock?
    install_file(file_name, version, tmp_path)
    assert((tmp_path/file_name).is_file)

    install_file(file_name, version, test_install_path)
    assert((test_install_path/file_name).is_file)

    (test_install_path/file_name).unlink()


def test_install_file_with_mock(tmp_path, monkeypatch, mock_file_request, mocker):
    file_name = 'vykonPro-rt.jar'
    version = '4.13'
    test_install_path = tmp_path

    # def mock_get(*args, **kwargs):
    #     return mock_file_request()
    
    mocker.patch('requests.get',return_value = mock_file_request())
    # monkeypatch.setattr(requests, 'get', mock_get())

    # test_install_path = Path(__file__)/'resources'/'EC-Net4-4.13.0.186'/'modules'
    install_file(file_name, version, test_install_path)
    install_file(file_name, version, Path(__file__).parent)
    assert (Path(tmp_path)/file_name).exists()