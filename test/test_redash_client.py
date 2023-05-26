import httpx
import pytest
from local_redash.lib.redash_client import RedashClient
from local_redash.models.redash_client import (DataSourceList, Query,
                                               QueryUpdate)
from pytest_httpserver import HTTPServer


def test_search_query(httpserver: HTTPServer, response_query_models):
    httpserver.expect_request('/api/queries',
                              query_string='page=1').respond_with_json(
                                  response_query_models[0])
    httpserver.expect_request('/api/queries',
                              query_string='page=2').respond_with_json(
                                  response_query_models[1])
    httpserver.expect_request('/api/queries',
                              query_string='page=3').respond_with_json(
                                  response_query_models[2])
    query_name = response_query_models[2]['results'][0]['name']

    client = RedashClient(httpserver.url_for("/"), 'aaaaaaaa')
    result = client.search_query(query_name)

    assert result is not None
    assert result.name == query_name
    assert type(result) is Query


def test_search_query_none(httpserver: HTTPServer, response_query_models):
    httpserver.expect_request('/api/queries',
                              query_string='page=1').respond_with_json(
                                  response_query_models[0])
    httpserver.expect_request('/api/queries',
                              query_string='page=2').respond_with_json(
                                  response_query_models[1])
    httpserver.expect_request('/api/queries',
                              query_string='page=3').respond_with_json(
                                  response_query_models[2])

    client = RedashClient(httpserver.url_for("/"), 'aaaaaaaa')
    result = client.search_query('test_query')
    assert result is None


def test_get_data_source_list(httpserver: HTTPServer,
                              response_dataSource_models):
    httpserver.expect_request('/api/data_sources').respond_with_json(
        response_dataSource_models)

    client = RedashClient(httpserver.url_for("/"), 'aaaaaaaa')
    result = client.get_data_source_list()

    assert len(list(result)) == len(response_dataSource_models)
    assert type(result) is DataSourceList


def test_get_data_source_list_empty(httpserver: HTTPServer):
    httpserver.expect_request('/api/data_sources').respond_with_json([])

    client = RedashClient(httpserver.url_for("/"), 'aaaaaaaa')
    result = client.get_data_source_list()

    assert len(list(result)) == 0


def test_update_query(httpserver: HTTPServer, response_query_update_model):
    query_str = 'select * from aaaaa'
    payload = {'query': query_str, 'options': {}}
    httpserver.expect_request(
        '/api/queries/1',
        json=payload).respond_with_json(response_query_update_model)

    client = RedashClient(httpserver.url_for("/"), 'aaaaaaaa')
    result = client.update_query(1, query_str)

    assert type(result) is QueryUpdate


def test_create_query(httpserver: HTTPServer, response_query_update_model):
    query_str = 'select * from aaaaa'
    payload = {
        "data_source_id": 1,
        "name": 'test',
        "query": query_str,
        "description": 'test query',
        "options": {}
    }
    httpserver.expect_request(
        '/api/queries',
        json=payload).respond_with_json(response_query_update_model)

    client = RedashClient(httpserver.url_for("/"), 'aaaaaaaa')
    result = client.create_query(1, 'test', query_str, 'test query')

    assert type(result) is QueryUpdate


# private method


def test_polling_job(httpserver: HTTPServer):
    pass


def test_get(httpserver: HTTPServer):
    httpserver.expect_request('/foo',
                              headers={
                                  'Authorization': 'Key aaaaaaaa'
                              }).respond_with_json({'foo': 'bar'})

    client = RedashClient(httpserver.url_for("/"), 'aaaaaaaa')
    result = client._get('foo')

    assert result == {'foo': 'bar'}


def test_get_with_param(httpserver: HTTPServer):
    httpserver.expect_request(
        '/foo',
        query_string='page=1&page_size=25').respond_with_json({'foo': 'bar'})

    client = RedashClient(httpserver.url_for("/"), 'aaaaaaaa')
    result = client._get('foo', params={'page': 1, 'page_size': 25})

    assert result == {'foo': 'bar'}


def test_get_error(httpserver: HTTPServer):
    httpserver.expect_request('/foo').respond_with_json({'error': '400'},
                                                        status=400)
    client = RedashClient(httpserver.url_for('/'), 'aaaaaaaa')
    with pytest.raises(httpx.HTTPStatusError, match='400 BAD REQUEST') as e:
        client._get('foo')


def test_post_with_body(httpserver: HTTPServer):
    httpserver.expect_request('/foo', json={
        'page': 1,
        'page_size': 25
    }).respond_with_json({'foo': 'bar'})

    client = RedashClient(httpserver.url_for("/"), 'aaaaaaaa')
    result = client._post('foo', payload={'page': 1, 'page_size': 25})

    assert result == {'foo': 'bar'}


def test_get_paginate(httpserver: HTTPServer, response_query_models):
    httpserver.expect_request('/foo', query_string='page=1').respond_with_json(
        response_query_models[0])
    httpserver.expect_request('/foo', query_string='page=2').respond_with_json(
        response_query_models[1])
    httpserver.expect_request('/foo', query_string='page=3').respond_with_json(
        response_query_models[2])

    client = RedashClient(httpserver.url_for("/"), 'aaaaaaaa')
    result = client._get_paginate('foo')
    assert len(result) == 27
