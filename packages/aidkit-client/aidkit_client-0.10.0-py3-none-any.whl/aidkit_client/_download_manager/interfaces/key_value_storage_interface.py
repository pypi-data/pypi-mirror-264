from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class KeyValueStorageInterface(ABC, Generic[K, V]):
    """
    Key-value storage interface.
    """

    @abstractmethod
    def keys(self) -> List[K]:
        """
        Return all keys.
        """

    @abstractmethod
    def has(self, key: K) -> bool:
        """
        Check if 'key' exists in storage.

        :param key: Key of the storage item.
        """

    @abstractmethod
    def get(self, key: K) -> Optional[V]:
        """
        Return value for requested key.

        :param key: Key of the storage item.
        """

    @abstractmethod
    def add(self, key: K, value: V) -> None:
        """
        Add new key-value pair.

        :param key: Key of the storage item.
        :param value: Content of the storage item.
        """

    @abstractmethod
    def remove(self, key: K) -> None:
        """
        Remove key and its value if key exists.

        :param key: Key of the storage item.
        """

    @abstractmethod
    def remove_all(self) -> None:
        """
        Remove all keys.
        """
