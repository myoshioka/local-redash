from unittest import mock
from unittest.mock import MagicMock, mock_open, patch

from local_redash.commands.query import QueryCommand
from local_redash.lib.redash_client import RedashClient


def test_data_source_list(test_container, mock_value_data_source_list, capsys):
    test_container.config.command.type.from_value('data_source_list')

    expected_format = "\n".join([
        '+------+--------+----------------+----------+----------+-------------+--------+',
        '|   id |  name  |  pause_reason  |  syntax  |   paused |  view_only  |  type  |',
        '|------+--------+----------------+----------+----------+-------------+--------|',
        '|    1 |  aaaa  |      bbbb      |   cccc   |        1 |    False    | mysql  |',
        '|    2 |  1111  |      2222      |   3333   |        1 |    True     |   pg   |',
        '+------+--------+----------------+----------+----------+-------------+--------+',
    ])
    redash_client_mock = mock.Mock()
    redash_client_mock.get_data_source_list.return_value = mock_value_data_source_list

    with test_container.redash_client.override(redash_client_mock):
        executer = test_container.executer()
        executer.execute()

    captured = capsys.readouterr()
    print('\n')
    print(captured.out)
    print(expected_format)
    assert captured.out.splitlines() == expected_format.splitlines()


def test_query_list(test_container, mock_value_query_list, capsys):
    test_container.config.command.type.from_value('query_list')
    test_container.config.columns.query_list.from_value([
        'id', 'name', 'created_at', 'retrieved_at', 'data_source_id', 'runtime'
    ])

    expected_format = "\n".join([
        '+------+------------+------------------+-----------+--------------------------+--------------------------+',
        '|   id |    name    |   data_source_id |   runtime |       retrieved_at       |        created_at        |',
        '|------+------------+------------------+-----------+--------------------------+--------------------------|',
        '|    2 | query_test |                1 | 0.0163462 | 2023-04-07T06:31:06.983Z | 2022-09-29T08:48:25.160Z |',
        '|    1 |  test-01   |                1 | 0.0268879 | 2022-09-16T10:12:21.974Z | 2022-09-16T10:12:37.666Z |',
        '+------+------------+------------------+-----------+--------------------------+--------------------------+',
    ])
    redash_client_mock = mock.Mock()
    redash_client_mock.get_query_list.return_value = mock_value_query_list

    with test_container.redash_client.override(redash_client_mock):
        executer = test_container.executer()
        executer.execute()

    captured = capsys.readouterr()
    print('\n')
    print(captured.out)
    print(expected_format)
    assert captured.out.splitlines() == expected_format.splitlines()


def test_query(test_container, mock_value_query_result_data,
               mock_value_query_update, capsys):
    test_container.config.command.type.from_value('query')

    expected_format = "\n".join([
        '+------------+------------+--------------+-------------+------------+--------------+',
        '|   staff_id |  username  |  first_name  |  last_name  |   store_id |   address_id |',
        '|------------+------------+--------------+-------------+------------+--------------|',
        '|          1 |    Mike    |     Mike     |   Hillyer   |          1 |            3 |',
        '|          2 |    Jon     |     Jon      |  Stephens   |          2 |            4 |',
        '+------------+------------+--------------+-------------+------------+--------------+',
    ])

    redash_client_mock = mock.Mock()
    redash_client_mock.search_query.return_value = None
    redash_client_mock.create_query.return_value = mock_value_query_update
    redash_client_mock.query_result.return_value = mock_value_query_result_data

    with test_container.redash_client.override(redash_client_mock):
        command = test_container.command()
        get_query_mock = MagicMock(return_value='test query')
        get_file_name_mock = MagicMock(return_value='test')
        command._get_query = get_query_mock
        command._get_file_name = get_file_name_mock

        executer = test_container.executer()
        executer.execute('test.sql', '1')

    captured = capsys.readouterr()
    print('\n')
    print(captured.out)
    print(expected_format)

    assert captured.out.splitlines() == expected_format.splitlines()


def test_query_sort_columns(mock_value_query_result_data):
    client = RedashClient('http://dummy', 'aaaaaaaa')
    query_command = QueryCommand(client)
    result_data = query_command._sort_columns(mock_value_query_result_data)

    sorted_columns = [column.friendly_name for column in result_data.columns]
    keys_list = [list(row.keys()) for row in result_data.rows.dict()]

    for keys in keys_list:
        assert keys == sorted_columns


# @patch("builtins.open", new_callable=mock_open)
def test_query_export(test_container, mock_value_query,
                      mock_value_data_source_detail, capsys):
    test_container.config.command.type.from_value('query_export')

    expected_format = "\n".join([
        '+------------------------------+',
        '| exported-query               |',
        '|------------------------------|',
        '| select                       |',
        '|     id,                      |',
        '|     email,                   |',
        '|     admin,                   |',
        '|     first_name,              |',
        '|     last_name                |',
        '| from users                   |',
        '| where id = 7327 or id = 7328 |',
        '+------------------------------+',
    ])
    redash_client_mock = mock.Mock()
    redash_client_mock.search_query.return_value = mock_value_query
    redash_client_mock.get_data_source.return_value = mock_value_data_source_detail
    save_query_mock = MagicMock(return_value=True)

    with test_container.redash_client.override(redash_client_mock):
        command = test_container.command()
        command._save_query = save_query_mock

        executer = test_container.executer()
        executer.execute('query_test', './', stralign='left')

    save_query_mock.assert_called_once_with(
        'select\n    id,\n    email,\n    admin,\n    first_name,\n    last_name\nfrom users\nwhere id = 7327 or id = 7328\n',
        './query_test.sql')

    captured = capsys.readouterr()
    print('\n')
    print(captured.out)
    print(expected_format)
    assert captured.out.splitlines() == expected_format.splitlines()
