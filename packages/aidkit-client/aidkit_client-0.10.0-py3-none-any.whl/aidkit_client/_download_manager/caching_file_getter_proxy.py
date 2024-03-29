from aidkit_client._download_manager.interfaces.get_file_interface import (
    GetFileInterface,
)
from aidkit_client._download_manager.interfaces.key_value_storage_interface import (
    KeyValueStorageInterface,
)


class CachingFileGetterProxy(GetFileInterface):
    """
    File Getter that uses caching capabilities.
    """

    def __init__(
        self,
        file_getter: GetFileInterface,
        storage: KeyValueStorageInterface[str, bytes],
    ) -> None:
        self._file_getter = file_getter
        self._storage = storage

    async def get_file(self, uri: str) -> bytes:
        """
        Download resource with 'uri' if it doesn't exist in cache, otherwise retrieve it from cache.

        :param uri: resource identificator;
        :return: payload.
        """
        if self._storage.has(key=uri):
            return self._storage.get(key=uri)  # type: ignore

        else:
            data = await self._file_getter.get_file(uri=uri)
            self._storage.add(key=uri, value=data)
            return data
