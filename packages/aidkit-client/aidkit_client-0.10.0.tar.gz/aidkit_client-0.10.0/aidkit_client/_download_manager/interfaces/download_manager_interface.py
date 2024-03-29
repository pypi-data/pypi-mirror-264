from abc import ABC, abstractmethod
from typing import List

from aidkit_client._download_manager.interfaces.data_structures import (
    DownloadResult,
)


class AsyncDownloaderInterface(ABC):
    """
    Interface to Download Manager.
    """

    @abstractmethod
    async def download(self, storage_paths: List[str]) -> DownloadResult:
        """
        Download multiple resources with `storage_paths` identificators.

        :param storage_paths: list of resources to be downloaded.
        :return: aggregated download result for all resources.
        """
