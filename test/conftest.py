import pytest
from local_redash.containers import Container


@pytest.fixture
def test_container():
    return Container(
        config={'redash': {
            'url': 'http://dummy',
            'api_key': 'dummy_key'
        }})
