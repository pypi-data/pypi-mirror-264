from aidkit_client._download_manager.interfaces.get_file_interface import (
    GetFileInterface,
)
from aidkit_client._download_manager.interfaces.progress_tracking_interfaces import (
    ProgressIncrementorInterface,
)


class ProgressTrackingFileGetterProxy(GetFileInterface):
    """
    This object is forwarding the call to the given GetFileInterface.
    Every time the get_file method is called the progress will increase.
    """

    def __init__(
        self,
        file_getter: GetFileInterface,
        progress_tracker: ProgressIncrementorInterface,
    ):
        self._file_getter = file_getter
        self._progress_tracker = progress_tracker

    async def get_file(self, uri: str) -> bytes:
        """
        Get a file from the storage.

        :param uri: URI of the file to get.
        :return: Content of the file.
        :raises Exception: If no file was found.
        """
        try:
            return await self._file_getter.get_file(uri)
        except Exception as error:
            raise error
        finally:
            self._progress_tracker.increase_progress()
