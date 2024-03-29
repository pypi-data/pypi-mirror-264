from abc import ABC, abstractmethod


class LocalPathForStoragePathGetterInterface(ABC):
    """
    This interface is for returning the local path of a downloaded object.
    """

    @abstractmethod
    def get_local_path_for_storage_path(self, storage_path: str) -> str:
        """
        This method returns the local path of a downloaded object, given the download path of the object.

        :param storage_path: the path, where the object can be downloaded.
        :return: the path, where the downloaded object is saved.
        """
        pass
