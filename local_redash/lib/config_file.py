import shutil
from os import makedirs
from os.path import dirname, exists, expanduser, join

CONFIG_FILE_NAME = 'config.yml'


class ConfigFile():

    def __init__(self):
        if not exists(join(self._config_path(), CONFIG_FILE_NAME)):
            self._write_default_config()

    def file_path(self) -> str:
        return join(self._config_path(), CONFIG_FILE_NAME)

    def _config_path(self) -> str:
        return expanduser('~/.config/local_redash/')

    def _write_default_config(self) -> None:
        makedirs(self._config_path(), exist_ok=True)

        default_config = self._get_default_config()
        shutil.copyfile(default_config,
                        join(self._config_path(), CONFIG_FILE_NAME))

    def _get_default_config(self) -> str:
        from local_redash import __file__ as package_root

        package_root = dirname(package_root)
        return join(package_root, CONFIG_FILE_NAME)
