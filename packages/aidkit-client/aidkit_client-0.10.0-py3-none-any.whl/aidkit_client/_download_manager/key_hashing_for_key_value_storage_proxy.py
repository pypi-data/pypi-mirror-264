from typing import Callable, List, Optional

from aidkit_client._download_manager.interfaces.key_value_storage_interface import (
    KeyValueStorageInterface,
)


class KeyHashingForKeyValueStorageProxy(KeyValueStorageInterface[str, bytes]):
    def __init__(
        self,
        uri_to_key_factory: Callable[[str], str],
        storage: KeyValueStorageInterface[str, bytes],
    ):
        self._hash_key = uri_to_key_factory
        self._storage = storage

    def keys(self) -> List[str]:
        return self._storage.keys()

    def get(self, key: str) -> Optional[bytes]:
        return self._storage.get(key=self._hash_key(key))

    def add(self, key: str, value: bytes) -> None:
        self._storage.add(key=self._hash_key(key), value=value)

    def has(self, key: str) -> bool:
        return self._storage.has(key=self._hash_key(key))

    def remove(self, key: str) -> None:
        self._storage.remove(key=self._hash_key(key))

    def remove_all(self) -> None:
        self._storage.remove_all()
