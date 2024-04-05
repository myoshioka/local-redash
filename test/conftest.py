import json
import os

import pytest
from local_redash.containers import Container
from local_redash.models.redash_client import (DataSource, DataSourceDetail,
                                               DataSourceList, JobResult,
                                               JobResultStatus, Query,
                                               QueryDetail, QueryList,
                                               QueryResulColumn,
                                               QueryResulRows, QueryResult,
                                               QueryResultData, ResponseQuery,
                                               Visualization)
from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory
from pytest_httpserver import HTTPServer


def get_test_data(filename):
    folder_path = os.path.abspath(os.path.dirname(__file__))
    folder = os.path.join(folder_path, 'testdata')
    jsonfile = os.path.join(folder, filename)
    with open(jsonfile) as file:
        data = json.load(file)
    return data


class QueryFactory(ModelFactory[Query]):
    __model__ = Query
    options = {}


class VisualizationFactory(ModelFactory[Visualization]):
    __model__ = Visualization
    options = {}


class QueryDetailFactory(ModelFactory[QueryDetail]):
    __model__ = QueryDetail
    options = {}
    visualizations = Use(VisualizationFactory.batch, size=1)


class ResponseQueryFactory(ModelFactory[ResponseQuery]):
    __model__ = ResponseQuery
    results = Use(QueryFactory.batch, size=10)


class DataSourceFactory(ModelFactory[DataSource]):
    __model__ = DataSource


class JobResultFactory(ModelFactory[JobResult]):
    __model__ = JobResult


class QueryResulColumnFactory(ModelFactory[QueryResulColumn]):
    __model__ = QueryResulColumn


class QueryResulRowsFactory(ModelFactory[QueryResulRows]):
    __model__ = QueryResulRows


class QueryResultDataFactory(ModelFactory[QueryResultData]):
    __model__ = QueryResultData
    rows = QueryResulRows.parse_obj(get_test_data('query_result_rows.json'))
    columns = Use(QueryResulColumnFactory.batch, size=5)


class QueryResultFactory(ModelFactory[QueryResult]):
    __model__ = QueryResult
    # data = Use(QueryResultDataFactory.batch, size=1)
    data = QueryResultDataFactory.build()


# fixture
@pytest.fixture()
def httpserver(make_httpserver):
    server = make_httpserver
    server.expect_request('/api/users').respond_with_json({"message": "OK"})
    yield server
    server.clear()


@pytest.fixture
def test_container():
    return Container(
        config={
            'redash': {
                'url': 'http://dummy',
                'api_key': 'dummy_key'
            },
            'table_format': {
                'tablefmt': 'psql',
                'stralign': 'left'
            }
        })


@pytest.fixture
def mock_value_data_source_list():
    return DataSourceList.parse_obj(get_test_data('data_source_list.json'))


@pytest.fixture
def mock_value_data_source_detail():
    return DataSourceDetail.parse_obj(get_test_data('data_source_detail.json'))


@pytest.fixture
def mock_value_query_list():
    return QueryList.parse_obj(get_test_data('query_list.json'))


@pytest.fixture
def mock_value_query():
    return Query.parse_obj(get_test_data('query_list.json')[0])


@pytest.fixture
def mock_value_query_result_data():
    return QueryResultData.parse_obj(
        get_test_data('query_result.json')['query_result']['data'])


@pytest.fixture
def mock_value_query_detail():
    return QueryDetailFactory.build(
        query=get_test_data('query_list.json')[0]['query'],
        name=get_test_data('query_list.json')[0]['name'])


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
def response_query_detail_model():
    return QueryDetailFactory.build().dict()


@pytest.fixture
def response_job_result_finished_model():
    return JobResultFactory.build(status=JobResultStatus.FINISHED,
                                  query_result_id=1).dict()


@pytest.fixture
def response_query_result_model():
    return QueryResultFactory.build().dict()
