from unittest import mock


def test_data_source_list(test_container, monkeypatch, capsys):
    test_container.config.command.type.from_value('data_source_list')

    expected_format = "\n".join([
        '+--------+--------+--------+',
        '|   aaaa |   bbbb |   cccc |',
        '|--------+--------+--------|',
        '|   1111 |   2222 |   3333 |',
        '|   4444 |   5555 |   6666 |',
        '+--------+--------+--------+',
    ])
    mock_value = [{
        'aaaa': '1111',
        'bbbb': '2222',
        'cccc': '3333'
    }, {
        'aaaa': '4444',
        'bbbb': '5555',
        'cccc': '6666'
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
