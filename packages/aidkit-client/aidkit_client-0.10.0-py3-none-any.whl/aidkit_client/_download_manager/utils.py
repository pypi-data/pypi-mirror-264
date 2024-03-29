from hashlib import md5
from uuid import UUID


def default_uri_to_key_factory(uri: str) -> str:
    """
    Make uuid from given uri.

    :param uri: resource uri
    :return: uuid of the resource
    """
    hash = md5(uri.encode()).hexdigest()
    uuid = UUID(hex=hash)
    return str(uuid)
