from requests import HTTPError


class AutomizorStorageError(RuntimeError):
    """Exception raised for errors encountered while interacting with the Storage."""


class AssetNotFoundError(HTTPError):
    """Exception raised when an asset is not found."""
