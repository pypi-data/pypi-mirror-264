from abc import ABC, abstractmethod


class TotalSetterInterface(ABC):
    """
    This interface can set_total.
    """

    @abstractmethod
    def set_total(self, total: int) -> None:
        """
        :param total: int
        :return: None
        """


class ProgressIncrementorInterface(ABC):
    """
    This interface can increase_progress.
    """

    @abstractmethod
    def increase_progress(self) -> None:
        """
        :return: None
        """


class ProgressGetterInterface(ABC):
    """
    This interface can get_progress.
    """

    @abstractmethod
    def get_progress(self) -> int:
        """
        :return: int, a value from 0 to(including) 100
        """
