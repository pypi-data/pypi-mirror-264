from typing import Callable, List, cast

from tqdm import tqdm

from aidkit_client._download_manager.async_download_manager import AsyncDownloadManager
from aidkit_client._download_manager.caching_file_getter_proxy import (
    CachingFileGetterProxy,
)
from aidkit_client._download_manager.download_storage import OnDiskDownloadStorage
from aidkit_client._download_manager.downloaded_files_progress_tracker import (
    DownloadedFilesProgressTracker,
)
from aidkit_client._download_manager.http_download import HttpFileGetter
from aidkit_client._download_manager.interfaces.data_structures import (
    DownloadResult,
)
from aidkit_client._download_manager.key_hashing_for_key_value_storage_proxy import (
    KeyHashingForKeyValueStorageProxy,
)
from aidkit_client._download_manager.local_path_for_storage_path_getter_proxy import (
    LocalPathForStoragePathGetterProxy,
)
from aidkit_client._download_manager.progress_tracking_download_manager_proxy import (
    ProgressTrackingDownloadManagerProxy,
)
from aidkit_client._download_manager.progress_tracking_file_getter_proxy import (
    ProgressTrackingFileGetterProxy,
)
from aidkit_client._download_manager.retrying_file_getter_proxy import (
    RetryingFileGetterProxy,
)
from aidkit_client._download_manager.utils import default_uri_to_key_factory
from aidkit_client.aidkit_api import HTTPService


class DownloadManagerFacade:
    """
    This class will have 2 functionalities to download.

    1 would be the normal download with caching and retry mechanism
    2 would be a download, where the Cache is emptied beforehand.
    """

    def __init__(
        self,
        client: HTTPService,
        download_directory: str = "/tmp/aidkit_download_manager",
        number_of_retries: int = 3,
        uri_to_key_factory: Callable[[str], str] = default_uri_to_key_factory,
    ):
        self._number_of_parallel_asynchronous_requests = 64
        self._make_key = uri_to_key_factory
        self._client = client
        self._download_storage = OnDiskDownloadStorage(base_path=download_directory)
        key_hashing_download_storage = KeyHashingForKeyValueStorageProxy(
            uri_to_key_factory=self._make_key, storage=self._download_storage
        )
        local_path_getter = LocalPathForStoragePathGetterProxy(
            uri_to_key_factory=self._make_key, local_path_getter=self._download_storage
        )
        self._progress_tracker = DownloadedFilesProgressTracker()
        self._download_manager = ProgressTrackingDownloadManagerProxy(
            download_manager=AsyncDownloadManager(
                getter=ProgressTrackingFileGetterProxy(
                    file_getter=CachingFileGetterProxy(
                        file_getter=RetryingFileGetterProxy(
                            file_getter=HttpFileGetter(client=client),
                            number_of_retries=number_of_retries,
                        ),
                        storage=key_hashing_download_storage,
                    ),
                    progress_tracker=self._progress_tracker,
                ),
                storage=key_hashing_download_storage,
                number_of_parallel_asynchronous_requests=(
                    self._number_of_parallel_asynchronous_requests
                ),
                local_path_getter=local_path_getter,
            ),
            progress_tracker=self._progress_tracker,
        )

    async def download(
        self, storage_paths: List[str], with_progress: bool = False
    ) -> DownloadResult:
        """
        This method utilizes DownloadManagerInterfaces to download with Caching
        and Retrying.

        :param storage_paths: list of URLs to be downloaded
        :param with_progress: bool
        :return: DownloadResult Object with 2 lists: success and failures
        """
        with tqdm(
            total=100,
            ascii=True,
            postfix="Downloading...",
            unit="%",
            disable=not with_progress,
        ) as progress_bar:

            def update_with_computed_progress(new_progress: int) -> None:
                old_progress = cast(tqdm, progress_bar).n
                progress_increase = new_progress - old_progress
                cast(tqdm, progress_bar).update(progress_increase)

            self._progress_tracker.subscribe(update_with_computed_progress)

            download_result = await self._download_manager.download(storage_paths=storage_paths)

        if with_progress:
            self._print_download_result(download_result)
        return download_result

    @staticmethod
    def _print_download_result(download_result: DownloadResult) -> None:
        """
        :param download_result: DownloadResult
        :return: None
        """
        total = len(download_result.success) + len(download_result.failure)
        print(f"We finished downloading {total} files.")
        if len(download_result.failure) > 0:
            print(f"We successfully downloaded {len(download_result.success)} files.")
            print(f"We failed to download {len(download_result.failure)} files.")

    async def force_re_download(
        self, storage_paths: List[str], with_progress: bool = False
    ) -> DownloadResult:
        """
        This method will clear out the Cache before starting the download.

        :param storage_paths: list of URLs to be downloaded
        :param with_progress: bool
        :return: DownloadResult Object with 2 lists: success and failures
        """
        self._download_storage.remove_all()

        return await self.download(storage_paths=storage_paths, with_progress=with_progress)
