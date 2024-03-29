from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class SubscribableInterface(ABC, Generic[T]):
    """
    This interface describes an object that can be subscribed to.
    """

    @abstractmethod
    def subscribe(self, callback: Callable[[T], None]) -> None:
        """
        :param callback: function (update: T) -> None
        :return: None
        """
