from dataclasses import dataclass, field
from typing import List


@dataclass
class Payload:
    """
    Payload is a successful Resource within the DownloadManager.
    """

    remote_uri_to_requested_resource: str
    local_uri_to_requested_resource: str


@dataclass
class Error:
    """
    Error is a representation of a failure within the DownloadManager.
    """

    remote_uri_to_requested_resource: str
    message: str


@dataclass
class DownloadResult:
    """
    Aggregated download result of multiple resources.
    """

    success: List[Payload] = field(default_factory=list)
    failure: List[Error] = field(default_factory=list)

    def __add__(self, other: "DownloadResult") -> "DownloadResult":  # noqa: D105
        success = self.success + other.success
        failure = self.failure + other.failure

        return DownloadResult(success=success, failure=failure)
