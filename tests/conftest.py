import pytest

from npi.search import get_manifest

@pytest.fixture
def mock_get_manifest():
    mock_manifest_data = """
    {
    "vykonPro": {
        "files": [
        "vykonPro-ux.jar",
        "vykonPro-rt.jar",
        "vykonPro-doc.jar",
        "vykonPro-wb.jar"
        ],
        "runtimeProfiles": [
        "ux",
        "rt",
        "doc",
        "wb"
        ]
    },
    "vykonProUtil": {
        "files": [
        "vykonProUtil-doc.jar",
        "vykonProUtil-rt.jar",
        "vykonProUtil-wb.jar"
        ],
        "runtimeProfiles": [
        "doc",
        "rt",
        "wb"
        ]
    }
    }"""

    pytest.MonkeyPatch.setattr(get_manifest, mock_manifest_data)



