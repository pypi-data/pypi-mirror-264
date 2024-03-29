from aidkit_client._download_manager.interfaces.get_file_interface import (
    GetFileInterface,
)
from aidkit_client.aidkit_api import HTTPService


class HttpFileGetterError(IOError):
    ...


class HttpFileGetter(GetFileInterface):
    """
    This class utilizes HTTPService to download one single File.
    """

    def __init__(self, client: HTTPService):
        self._client = client

    async def get_file(self, uri: str) -> bytes:
        """
        This method receive an URL to a file and utilizing HTTPService to
        download that file.

        :param uri: URL path to the file to be downloaded.
        :return: HTTP Response with status code and a body.
        :raises HttpFileGetterError: If no file was found.
        """
        try:
            response = await self._client.get_from_cdn(url=uri)
            response_body = response.body_dict_or_error(error_message="Error retrieving resource")

            return response_body["content"]
        except BaseException as error:
            raise HttpFileGetterError(str(error)) from error
