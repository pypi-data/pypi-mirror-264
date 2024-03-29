from aidkit_client._download_manager.interfaces.get_local_path_interface import (
    LocalPathForStoragePathGetterInterface,
)


class SameLocalPathAsRemotePathGetter(LocalPathForStoragePathGetterInterface):
    """
    Local path getter returning the same path for the remote file as for the local one.
    """

    def get_local_path_for_storage_path(self, storage_path: str) -> str:
        """
        This method returns the local path of a downloaded object, given the download path of the
        object.

        :param storage_path: the path, where the object can be downloaded.
        :return: the path, where the downloaded object is saved.
        """
        return storage_path
