import io
from typing import List, Optional, Tuple

from PIL import Image

from aidkit_client._download_manager.interfaces.key_value_storage_interface import (
    KeyValueStorageInterface,
)


class ResizeImagesDownloadStorageProxy(KeyValueStorageInterface[str, bytes]):
    """
    Storage proxy handling the resizing of images before storing them.
    """

    def __init__(
        self,
        storage: KeyValueStorageInterface[str, bytes],
        max_width_height: Tuple[int, int],
    ) -> None:
        self._storage = storage
        self.max_width_height = max_width_height

    def keys(self) -> List[str]:
        """
        Return all keys.
        :returns: A list containing all available keys.
        """
        return self._storage.keys()

    def has(self, key: str) -> bool:
        """
        Check if 'key' exists in storage.

        :param key: Key of the storage item.
        :returns: True if the key exists, False otherwise.
        """
        return self._storage.has(key)

    def get(self, key: str) -> Optional[bytes]:
        """
        Return value for requested key.

        :param key: Key of the storage item.
        :returns: The item corresponding to the key.
        """
        return self._storage.get(key)

    def _resize_image(self, image_as_bytes: bytes) -> bytes:
        image_buffer = io.BytesIO(image_as_bytes)
        image = Image.open(image_buffer)
        image.thumbnail(size=self.max_width_height)
        with io.BytesIO() as resized_image_buffer:
            image.save(resized_image_buffer, format="PNG")
            resized_image_bytes = resized_image_buffer.getvalue()

        return resized_image_bytes

    def add(self, key: str, value: bytes) -> None:
        """
        Add new key-value pair after resizing the image passed as `value` to
        have a size smaller or equal to `max_width_height`.

        :param key: Key of the storage item.
        :param value: Content of the storage item.
        """
        resized_image_bytes = self._resize_image(image_as_bytes=value)
        self._storage.add(key, resized_image_bytes)

    def remove(self, key: str) -> None:
        """
        Remove key and its value if key exists.

        :param key: Key of the storage item.
        """
        self._storage.remove(key)

    def remove_all(self) -> None:
        """
        Remove all keys.
        """
        self._storage.remove_all()
