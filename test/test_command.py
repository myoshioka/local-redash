from unittest import mock


def test_data_source_list(test_container, mock_value_data_source_list,
                          monkeypatch, capsys):
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


def test_query_list(test_container, mock_value_query_list, monkeypatch,
                    capsys):
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
