import os
from unittest.mock import patch

from local_redash.lib.config_file import ConfigFile


@patch('local_redash.__file__', '/package_root/')
@patch('local_redash.lib.config_file.exists')
def test_get_default_config(mock_exists):
    mock_exists.return_value = True

    config_file = ConfigFile()
    default_config = config_file._get_default_config()

    assert default_config == '/package_root/config.yml'


@patch.dict(os.environ, {'HOME': '/home/'}, clear=True)
@patch('local_redash.lib.config_file.exists')
def test_config_path(mock_exists):
    mock_exists.return_value = True

    config_file = ConfigFile()
    config_file_dir = config_file._config_path()

    assert config_file_dir == '/home/.config/local_redash/'


@patch.dict(os.environ, {'HOME': '/home/'}, clear=True)
@patch('local_redash.lib.config_file.exists')
def test_file_path(mock_exists):
    mock_exists.return_value = True

    config_file = ConfigFile()
    config_file_path = config_file.file_path()

    assert config_file_path == '/home/.config/local_redash/config.yml'
