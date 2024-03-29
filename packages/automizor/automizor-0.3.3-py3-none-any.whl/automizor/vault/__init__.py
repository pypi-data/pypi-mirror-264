from functools import lru_cache

from ._container import SecretContainer
from ._exceptions import AutomizorVaultError


@lru_cache
def _get_vault():
    from ._vault import Vault

    return Vault()


def create_secret(name: str, value: str, description: str = "") -> SecretContainer:
    """
    Creates a new secret. Stores to a local file or to the `Automizor API`,
    based on configuration. If the secret already exists, it will be updated.

    Args:
        name: The name of the secret.
        value: The value of the secret.
        description: The description of the secret.
    
    Returns:
        The created secret.
    
    Raises:
        AutomizorVaultError: If creating the secret fails.
    """

    secret = SecretContainer(
        name=name,
        description=description,
        value=value,
    )

    vault = _get_vault()
    return vault.create_secret(secret)


def get_secret(name: str) -> SecretContainer:
    """
    Retrieves a secret by its name. Fetches from a local file or queries the
    `Automizor API`, based on configuration.

    Args:
        name: The name of the secret to retrieve.

    Returns:
        The retrieved secret.

    Raises:
        AutomizorVaultError: If retrieving the secret fails.
    """

    vault = _get_vault()
    return vault.get_secret(name)


def set_secret(secret: SecretContainer) -> SecretContainer:
    """
    Updates an existing secret. Updates to a local file or to the
    `Automizor API`, based on configuration.

    Args:
        secret: The secret to update.

    Returns:
        The updated secret.

    Raises:
        AutomizorVaultError: If updating the secret fails.
    """

    vault = _get_vault()
    return vault.set_secret(secret)


__all__ = [
    "AutomizorVaultError",
    "SecretContainer",
    "create_secret",
    "get_secret",
    "set_secret",
]
