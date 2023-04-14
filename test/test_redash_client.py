from unittest import mock
from local_redash.lib.redash_client import RedashClient


def test_search_query(query_model):
    redash_mock = mock.Mock()
    redash_mock.paginate.return_value = [query_model.dict()]

    client = RedashClient(redash_mock)
    result = client.search_query(query_model.name)

    assert result == query_model


def test_search_query_none(query_model):
    redash_mock = mock.Mock()
    redash_mock.paginate.return_value = [query_model.dict()]

    client = RedashClient(redash_mock)
    result = client.search_query('test_query')

    assert result is None
