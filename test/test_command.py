from unittest import mock


def test_data_source_list(test_container, monkeypatch, capsys):
    test_container.config.command.type.from_value('data_source_list')

    expected_format = "\n".join([
        '+--------+----------------+----------+----------+-------------+--------+------+',
        '|  name  |  pause_reason  |  syntax  |   paused |  view_only  |  type  |   id |',
        '|--------+----------------+----------+----------+-------------+--------+------|',
        '|  aaaa  |      bbbb      |   cccc   |        1 |    False    |  fuga  |    1 |',
        '|  1111  |      2222      |   3333   |        1 |    True     |  hoge  |    2 |',
        '+--------+----------------+----------+----------+-------------+--------+------+',
    ])
    mock_value = [{
        'name': 'aaaa',
        'pause_reason': 'bbbb',
        'syntax': 'cccc',
        'paused': '1',
        'view_only': 'False',
        'type': 'fuga',
        'id': '1',
    }, {
        'name': '1111',
        'pause_reason': '2222',
        'syntax': '3333',
        'paused': '1',
        'view_only': 'True',
        'type': 'hoge',
        'id': '2',
    }]
    redash_client_mock = mock.Mock()
    redash_client_mock.get_data_source_list.return_value = mock_value

    with test_container.redash_client.override(redash_client_mock):
        executer = test_container.executer()
        executer.execute()

    captured = capsys.readouterr()
    print('\n')
    print(captured.out)
    print(expected_format)
    assert captured.out.splitlines() == expected_format.splitlines()
