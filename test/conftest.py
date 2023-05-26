import json
import os

import pytest
from local_redash.containers import Container
from local_redash.models.redash_client import (DataSource, DataSourceList,
                                               Query, QueryList, QueryUpdate,
                                               ResponseQuery, Visualization)
from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory
from redash_toolbelt import Redash


class QueryFactory(ModelFactory[Query]):
    __model__ = Query
    options = {}


class VisualizationFactory(ModelFactory[Visualization]):
    __model__ = Visualization
    options = {}


class QueryUpdateFactory(ModelFactory[QueryUpdate]):
    __model__ = QueryUpdate
    options = {}
    visualizations = Use(VisualizationFactory.batch, size=1)


class ResponseQueryFactory(ModelFactory[ResponseQuery]):
    __model__ = ResponseQuery
    results = Use(QueryFactory.batch, size=10)


class DataSourceFactory(ModelFactory[DataSource]):
    __model__ = DataSource


@pytest.fixture
def test_container():
    return Container(
        config={'redash': {
            'url': 'http://dummy',
            'api_key': 'dummy_key'
        }})


@pytest.fixture
def mock_value_data_source_list():
    return DataSourceList.parse_obj(get_test_data('data_source_list.json'))


@pytest.fixture
def mock_value_query_list():
    return QueryList.parse_obj(get_test_data('query_list.json'))


@pytest.fixture
def query_model():
    return QueryFactory.build()


@pytest.fixture
def response_query_models():

    response_query_1 = ResponseQuery(
        count=27,
        page=1,
        page_size=10,
        results=[QueryFactory.build() for i in range(10)]).dict()
    response_query_2 = ResponseQuery(
        count=27,
        page=2,
        page_size=10,
        results=[QueryFactory.build() for i in range(10)]).dict()
    response_query_3 = ResponseQuery(
        count=27,
        page=3,
        page_size=10,
        results=[QueryFactory.build() for i in range(7)]).dict()

    return [response_query_1, response_query_2, response_query_3]


@pytest.fixture
def response_dataSource_models():
    return [DataSourceFactory.build().dict() for i in range(5)]


@pytest.fixture
def response_query_update_model():
    return QueryUpdateFactory.build().dict()


def get_test_data(filename):
    folder_path = os.path.abspath(os.path.dirname(__file__))
    folder = os.path.join(folder_path, 'testdata')
    jsonfile = os.path.join(folder, filename)
    with open(jsonfile) as file:
        data = json.load(file)
    return data
