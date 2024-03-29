import asyncio
from typing import List, Union

from aidkit_client._download_manager.interfaces.data_structures import (
    DownloadResult,
    Error,
    Payload,
)
from aidkit_client._download_manager.interfaces.download_manager_interface import (
    AsyncDownloaderInterface,
)
from aidkit_client._download_manager.interfaces.get_file_interface import (
    GetFileInterface,
)
from aidkit_client._download_manager.interfaces.get_local_path_interface import (
    LocalPathForStoragePathGetterInterface,
)
from aidkit_client._download_manager.interfaces.key_value_storage_interface import (
    KeyValueStorageInterface,
)


class AsyncDownloadManager(AsyncDownloaderInterface):
    """
    Asynchronous download manager.

    Download manager that asynchronously downloads network resources.
    """

    def __init__(
        self,
        getter: GetFileInterface,
        storage: KeyValueStorageInterface[str, bytes],
        number_of_parallel_asynchronous_requests: int,
        local_path_getter: LocalPathForStoragePathGetterInterface,
    ) -> None:
        self._getter = getter
        self._storage = storage
        self._concurrency = number_of_parallel_asynchronous_requests
        self._semaphore = asyncio.Semaphore(self._concurrency)
        self._local_path_getter = local_path_getter

    async def _fetch_one(self, storage_path: str) -> Union[Payload, Error]:
        async with self._semaphore:
            try:
                response_content = await self._getter.get_file(uri=storage_path)
            except Exception as error:
                return Error(remote_uri_to_requested_resource=storage_path, message=str(error))

            try:
                self._storage.add(key=storage_path, value=response_content)

            except Exception as error:
                return Error(remote_uri_to_requested_resource=storage_path, message=str(error))

            return Payload(
                remote_uri_to_requested_resource=storage_path,
                local_uri_to_requested_resource=self._local_path_getter.get_local_path_for_storage_path(
                    storage_path=storage_path
                ),
            )

    async def _fetch_many(self, storage_paths: List[str]) -> DownloadResult:
        group_response = await asyncio.gather(
            *[self._fetch_one(storage_path=storage_path) for storage_path in storage_paths]
        )

        download_result = DownloadResult()
        for response_item in group_response:
            if isinstance(response_item, Payload):
                download_result.success.append(response_item)
            if isinstance(response_item, Error):
                download_result.failure.append(response_item)

        return download_result

    async def download(self, storage_paths: List[str]) -> DownloadResult:
        """
        Download multiple resources with `storage_paths` identificators and save them
        into local file storage.

        :param storage_paths: list of resources to be downloaded.
        :return: aggregated download result for all resources.
        """
        return await self._fetch_many(storage_paths=storage_paths)
