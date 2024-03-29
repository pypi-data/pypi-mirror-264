from typing import Callable

from aidkit_client._download_manager.interfaces.get_local_path_interface import (
    LocalPathForStoragePathGetterInterface,
)


class LocalPathForStoragePathGetterProxy(LocalPathForStoragePathGetterInterface):
    def __init__(
        self,
        uri_to_key_factory: Callable[[str], str],
        local_path_getter: LocalPathForStoragePathGetterInterface,
    ):
        self._hash_key = uri_to_key_factory
        self._local_path_getter = local_path_getter

    def get_local_path_for_storage_path(self, storage_path: str) -> str:
        return self._local_path_getter.get_local_path_for_storage_path(
            storage_path=self._hash_key(storage_path)
        )
