from unittest import mock


def test_data_source_list(test_container, monkeypatch):
    test_container.config.command.type.from_value('data_source_list')

    mock_value = [{'aaaa': 'AAAA'}, {'bbbb': 'BBBB'}]
    redash_client_mock = mock.Mock()
    redash_client_mock.get_data_source_list.return_value = mock_value

    with test_container.redash_client.override(redash_client_mock):
        command = test_container.command()
        result = command.execute()

    assert result == mock_value
