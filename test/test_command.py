from unittest import mock
from unittest.mock import MagicMock


def test_data_source_list(test_container, mock_value_data_source_list, capsys):
    test_container.config.command.type.from_value('data_source_list')

    expected_format = "\n".join([
        '+------+--------+----------------+----------+----------+-------------+--------+',
        '|   id |  name  |  pause_reason  |  syntax  |   paused |  view_only  |  type  |',
        '|------+--------+----------------+----------+----------+-------------+--------|',
        '|    1 |  aaaa  |      bbbb      |   cccc   |        1 |    False    |  fuga  |',
        '|    2 |  1111  |      2222      |   3333   |        1 |    True     |  hoge  |',
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
        '+------------+------------+-------------+------------+--------------+--------------+',
        '|  username  |   staff_id |  last_name  |   store_id |   address_id |  first_name  |',
        '|------------+------------+-------------+------------+--------------+--------------|',
        '|    Mike    |          1 |   Hillyer   |          1 |            3 |     Mike     |',
        '|    Jon     |          2 |  Stephens   |          2 |            4 |     Jon      |',
        '+------------+------------+-------------+------------+--------------+--------------+',
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
