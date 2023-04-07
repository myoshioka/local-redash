import os
import pytest
import json
from local_redash.containers import Container


@pytest.fixture
def test_container():
    return Container(
        config={'redash': {
            'url': 'http://dummy',
            'api_key': 'dummy_key'
        }})


@pytest.fixture
def mock_value_data_source_list():
    return get_test_data('data_source_list.json')


@pytest.fixture
def mock_value_query_list():
    return get_test_data('query_list.json')


def get_test_data(filename):
    folder_path = os.path.abspath(os.path.dirname(__file__))
    folder = os.path.join(folder_path, 'testdata')
    jsonfile = os.path.join(folder, filename)
    with open(jsonfile) as file:
        data = json.load(file)
    return data
