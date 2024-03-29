import pathlib
import shutil
from os import walk
from os.path import abspath
from typing import Dict, List, Optional

from aidkit_client._download_manager.interfaces.get_local_path_interface import (
    LocalPathForStoragePathGetterInterface,
)
from aidkit_client._download_manager.interfaces.key_value_storage_interface import (
    KeyValueStorageInterface,
)


class OnDiskDownloadStorage(
    KeyValueStorageInterface[str, bytes], LocalPathForStoragePathGetterInterface
):
    """
    Key-value storage that stores values in files in local file system.
    """

    def __init__(self, base_path: str) -> None:
        """
        :param base_path: root directory where data is stored;
        """
        self._base_path = pathlib.Path(abspath(base_path))
        self._base_path.mkdir(parents=True, exist_ok=True)
        self._keys = self._get_all_keys()

    def _get_all_keys(self) -> List[str]:
        keys = []
        for root, _dirs, files in walk(self._base_path, topdown=False):
            for file in files:
                path = str(pathlib.Path(root) / file)
                key = self._get_key_from_storage_path(path=path)
                keys.append(key)

        return sorted(keys)

    def _get_key_from_storage_path(self, path: str) -> str:
        return str(pathlib.Path(path).relative_to(self._base_path))

    def _get_storage_path_from_key(self, key: str) -> str:
        file_path = pathlib.Path(abspath(self._base_path / key))

        if self._base_path not in file_path.parents:
            raise ValueError(
                f"key arg has wrong value: '{key}', "
                f"can't go outside base directory '{self._base_path.name}'"
            )

        return str(file_path)

    def keys(self) -> List[str]:
        """
        Return all keys.

        :return: list of keys
        """
        return self._keys

    def has(self, key: str) -> bool:
        """
        Check if 'key' exists in storage.

        :param key: key of the storage item
        :return: bool
        """
        return key in self._keys

    def get(self, key: str) -> Optional[bytes]:
        """
        Return value for requested 'key' if the 'key' exists.

        :param key: key of the storage item
        :return: value or None
        """
        if not self.has(key=key):
            return None

        file_path = pathlib.Path(self._get_storage_path_from_key(key=key))

        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)

        with open(str(file_path), mode="rb") as file:
            return file.read()

    def add(self, key: str, value: bytes) -> None:
        """
        Add new key-value pair.

        :param key: Key of the storage item.
        :param value: Content of the storage item.
        """
        file_path = pathlib.Path(self._get_storage_path_from_key(key=key))

        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)

        with open(str(file_path), mode="wb") as file:
            file.write(value)

        self._keys.append(key)

    def remove(self, key: str) -> None:
        """
        Remove key and its value if key exists when key passed is not None. If key is not
        specified, remove all keys.

        :param key: Key of the storage item.
        """
        if not self.has(key=key):
            return

        file_path = pathlib.Path(self._get_storage_path_from_key(key=key))
        file_path.unlink()

        self._keys.remove(key)

    def remove_all(self) -> None:
        """
        Remove all keys.
        """
        shutil.rmtree(str(self._base_path))
        self._base_path.mkdir(parents=True)
        self._keys = []
        return

    def get_local_path_for_storage_path(self, storage_path: str) -> str:
        """
        This method returns the local path, where the downloaded object is saved.

        :param storage_path: the path, where the object can be downloaded from
        :return: the path, where the downloaded object is saved
        """
        return self._get_storage_path_from_key(key=storage_path)


class InMemoryDownloadStorage(KeyValueStorageInterface[str, bytes]):
    """
    Key-value in memory storage interface.
    """

    def __init__(self, storage: Optional[Dict[str, bytes]] = None) -> None:
        self.storage: Dict[str, bytes] = storage if storage else {}

    def keys(self) -> List[str]:
        """
        Return all keys.
        :returns: A list containing all available keys.
        """
        return sorted(list(self.storage.keys()))

    def has(self, key: str) -> bool:
        """
        Check if 'key' exists in storage.

        :param key: Key of the storage item.
        :returns: True if the key exists, False otherwise.
        """
        return key in self.storage.keys()

    def get(self, key: str) -> Optional[bytes]:
        """
        Return value for requested key.

        :param key: Key of the storage item.
        :returns: The item corresponding to the key.
        """
        return self.storage.get(key)

    def add(self, key: str, value: bytes) -> None:
        """
        Add new key-value pair.

        :param key: Key of the storage item.
        :param value: Content of the storage item.
        """
        self.storage[key] = value

    def remove(self, key: str) -> None:
        """
        Remove key and its value if key exists.

        :param key: Key of the storage item.
        """
        self.storage.pop(key, None)

    def remove_all(self) -> None:
        """
        Remove all keys.
        """
        self.storage.clear()
