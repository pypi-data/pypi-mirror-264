from typing import Dict, List, Optional, Tuple

from aidkit_client._download_manager.async_download_manager import AsyncDownloadManager
from aidkit_client._download_manager.download_storage import InMemoryDownloadStorage
from aidkit_client._download_manager.http_download import HttpFileGetter
from aidkit_client._download_manager.resize_images_download_storage_proxy import (
    ResizeImagesDownloadStorageProxy,
)
from aidkit_client._download_manager.retrying_file_getter_proxy import (
    RetryingFileGetterProxy,
)
from aidkit_client._download_manager.same_local_path_as_remote_path_getter import (
    SameLocalPathAsRemotePathGetter,
)
from aidkit_client.aidkit_api import HTTPService


class DownloadImagesToMemoryDownloadManager:
    """
    Download files as Image to a dictionary.
    """

    def __init__(
        self,
        client: HTTPService,
        max_width_height: Optional[Tuple[int, int]] = None,
        number_of_parallel_asynchronous_requests=64,
    ) -> None:
        self._storage = InMemoryDownloadStorage()
        self.download_manager = AsyncDownloadManager(
            getter=RetryingFileGetterProxy(
                file_getter=HttpFileGetter(client=client),
                number_of_retries=5,
            ),
            storage=(
                ResizeImagesDownloadStorageProxy(
                    storage=self._storage, max_width_height=max_width_height
                )
                if max_width_height
                else self._storage
            ),
            number_of_parallel_asynchronous_requests=number_of_parallel_asynchronous_requests,
            local_path_getter=SameLocalPathAsRemotePathGetter(),
        )

    async def download(self, storage_paths: List[str]) -> Dict[str, bytes]:
        """
        Download files to a dictionary.

        :param storage_paths: Paths to the files on the deployment.
        :returns: A dictionary mapping the starage paths the the downloaded files.
        """
        download_result = await self.download_manager.download(storage_paths=storage_paths)
        downloaded_files: Dict[str, bytes] = {}
        for payload in download_result.success:
            local_storage_path = payload.local_uri_to_requested_resource
            downloaded_file = self._storage.get(local_storage_path)
            if downloaded_file:
                downloaded_files[local_storage_path] = downloaded_file

        return downloaded_files
