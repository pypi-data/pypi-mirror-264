from abc import ABC, abstractmethod


class GetFileInterface(ABC):
    """
    Interface to download one file.
    """

    @abstractmethod
    async def get_file(self, uri: str) -> bytes:
        """
        Download one file with the given URL.

        :param uri: URL path of file to be downloaded
        :return: download result of the downloaded file
        """
