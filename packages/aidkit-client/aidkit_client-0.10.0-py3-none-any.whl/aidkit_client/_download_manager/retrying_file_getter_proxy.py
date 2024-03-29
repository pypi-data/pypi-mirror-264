from tenacity import retry, stop_after_attempt, wait_exponential

from aidkit_client._download_manager.interfaces.get_file_interface import (
    GetFileInterface,
)


class RetryingFileGetterProxy(GetFileInterface):
    """
    This class utilizes retry package from tenacity to make multiple attempts to download failed
    downloads, with given number of retries and the injected HttpGetter.
    """

    def __init__(self, file_getter: GetFileInterface, number_of_retries: int):
        self._file_getter = file_getter
        self._number_of_retries = number_of_retries
        self._max_wait_between_retry_in_seconds = 30

    async def get_file(self, uri: str) -> bytes:
        """
        This method receive an URL to a file and utilizes the HttpGetter to download it, with
        multiple attempts if the download fails.

        :param uri: URL path to the file to be downloaded
        :return: HTTP Response with status code and a body
        """

        @retry(
            wait=wait_exponential(
                multiplier=1,  # Wait 2^retry_attempt * multiplier second between each retry
                min=0,
                max=self._max_wait_between_retry_in_seconds,
            ),
            stop=stop_after_attempt(max_attempt_number=self._number_of_retries + 1),
            reraise=True,
        )
        async def call_getter(uri: str) -> bytes:
            return await self._file_getter.get_file(uri=uri)

        return await call_getter(uri=uri)
