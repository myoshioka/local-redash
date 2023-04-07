from unittest import mock


def test_data_source_list(test_container, mock_value_data_source_list,
                          monkeypatch, capsys):
    test_container.config.command.type.from_value('data_source_list')

    expected_format = "\n".join([
        '+--------+----------------+----------+----------+-------------+--------+------+',
        '|  name  |  pause_reason  |  syntax  |   paused |  view_only  |  type  |   id |',
        '|--------+----------------+----------+----------+-------------+--------+------|',
        '|  aaaa  |      bbbb      |   cccc   |        1 |    False    |  fuga  |    1 |',
        '|  1111  |      2222      |   3333   |        1 |    True     |  hoge  |    2 |',
        '+--------+----------------+----------+----------+-------------+--------+------+',
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


def test_query_list(test_container, mock_value_query_list, monkeypatch,
                    capsys):
    test_container.config.command.type.from_value('query_list')
    test_container.config.columns.query_list.from_value([
        'id', 'name', 'created_at', 'retrieved_at', 'data_source_id', 'runtime'
    ])

    expected_format = "\n".join([
        '+--------------------------+------+------------------+------------+--------------------------+-----------+',
        '|       retrieved_at       |   id |   data_source_id |    name    |        created_at        |   runtime |',
        '|--------------------------+------+------------------+------------+--------------------------+-----------|',
        '| 2023-04-07T06:31:06.983Z |    2 |                1 | query_test | 2022-09-29T08:48:25.160Z | 0.0163462 |',
        '| 2022-09-16T10:12:21.974Z |    1 |                1 |  test-01   | 2022-09-16T10:12:37.666Z | 0.0268879 |',
        '+--------------------------+------+------------------+------------+--------------------------+-----------+',
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
