from pathlib import Path

from npi.install import install_file

def test_install_file(tmp_path):
    file_name = 'vykonPro-rt.jar'
    version = '4.13'
    test_install_path = Path(__file__).parent/'resources'/'mock_install'/'EC-Net4-4.13.0.186'/'modules'
    # Test full download at resource path 

    install_file(file_name, version, test_install_path)
    assert((test_install_path/file_name).is_file)
    (test_install_path/file_name).unlink()


def test_install_file_with_mock(tmp_path, mocker, mock_file_request):
    file_name = 'vykonPro-rt.jar'
    version = '4.13'
    test_install_path = tmp_path/'some_dir'

    test_install_path.mkdir(parents=True, exist_ok=True)
    mocker.patch('requests.get', mock_file_request)

    install_file(file_name, version, test_install_path)
    assert (test_install_path/file_name).exists()

    