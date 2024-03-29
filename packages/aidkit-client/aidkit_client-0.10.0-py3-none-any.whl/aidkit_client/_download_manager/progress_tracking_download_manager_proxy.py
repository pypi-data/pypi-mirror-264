from typing import List

from aidkit_client._download_manager.interfaces.data_structures import DownloadResult
from aidkit_client._download_manager.interfaces.download_manager_interface import (
    AsyncDownloaderInterface,
)
from aidkit_client._download_manager.interfaces.progress_tracking_interfaces import (
    TotalSetterInterface,
)


class ProgressTrackingDownloadManagerProxy(AsyncDownloaderInterface):
    """
    This object is forwarding the call to the DownloadManagerInterface.
    It will set the total for the progress to the number of given storage_paths.
    """

    def __init__(
        self,
        download_manager: AsyncDownloaderInterface,
        progress_tracker: TotalSetterInterface,
    ):
        self._progress_tracker = progress_tracker
        self._download_manager = download_manager

    async def download(self, storage_paths: List[str]) -> DownloadResult:
        """
        :param storage_paths: List[str]
        :return: DownloadResult
        """
        self._progress_tracker.set_total(len(storage_paths))
        return await self._download_manager.download(storage_paths)
