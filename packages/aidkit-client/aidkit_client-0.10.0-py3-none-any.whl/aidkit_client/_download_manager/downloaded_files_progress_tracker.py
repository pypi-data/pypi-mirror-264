from typing import Callable, Optional

from aidkit_client._download_manager.interfaces.progress_tracking_interfaces import (
    ProgressGetterInterface,
    ProgressIncrementorInterface,
    TotalSetterInterface,
)
from aidkit_client._download_manager.interfaces.subscribable_interface import (
    SubscribableInterface,
)


class DownloadedFilesProgressTracker(
    ProgressGetterInterface,
    TotalSetterInterface,
    ProgressIncrementorInterface,
    SubscribableInterface[int],
):
    """
    This object will track the progress from 0 to given total.
    You can get the progress or subscribe to changes of the state.
    """

    _subscribe_callback: Optional[Callable[[int], None]]

    def __init__(self) -> None:
        self._subscribe_callback = None
        self._total_amount_of_files = 0
        self._finished_files = 0

    def get_progress(self) -> int:
        """
        :return: int
        """
        if self._total_amount_of_files == 0 or self._finished_files == 0:
            return 0
        return int((self._finished_files / self._total_amount_of_files) * 100)

    def set_total(self, total: int) -> None:
        """
        :param total: int
        :return: None
        """
        self._total_amount_of_files = total
        if self._subscribe_callback is not None:
            self._subscribe_callback(0)

    def increase_progress(self) -> None:
        """
        :return: None
        """
        if self._finished_files < self._total_amount_of_files:
            self._finished_files += 1
            if self._subscribe_callback is not None:
                self._subscribe_callback(self.get_progress())

    def subscribe(self, callback: Callable[[int], None]) -> None:
        """
        :param callback: function (progress: int) -> None
        :return: None
        """
        self._subscribe_callback = callback
