import os
import pytest
import json
from polyfactory.factories.pydantic_factory import ModelFactory
from local_redash.containers import Container
from redash_toolbelt import Redash
from local_redash.models.redash_client import Query


class QueryFactory(ModelFactory[Query]):
    __model__ = Query


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


@pytest.fixture
def query_model():
    return QueryFactory.build()


def get_test_data(filename):
    folder_path = os.path.abspath(os.path.dirname(__file__))
    folder = os.path.join(folder_path, 'testdata')
    jsonfile = os.path.join(folder, filename)
    with open(jsonfile) as file:
        data = json.load(file)
    return data
