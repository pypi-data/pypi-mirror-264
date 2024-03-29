import json
import os
from dataclasses import asdict

import requests

from automizor.utils import get_headers
from ._container import SecretContainer
from ._exceptions import AutomizorVaultError


class Vault:
    """
    `Vault` is a secure storage class within the `Automizor Platform` for managing
    secrets such as API keys, passwords, and other sensitive information. It offers
    functionality to securely retrieve and update secrets, either through direct
    interaction with the `Automizor API` or via a local secrets file, depending on
    the operational environment and configuration.

    Configuration for accessing and manipulating these secrets is driven by environment
    variables, which are essential for specifying the API's host and token for
    authentication purposes, alongside the location of a local secrets file, should
    local storage be preferred over API interaction.

    Environment variables requisite for operation include:
    - ``AUTOMIZOR_API_HOST``: The host URL for the `Automizor API`.
    - ``AUTOMIZOR_API_TOKEN``: The token for authenticate against the `Automizor API`.
    - ``AUTOMIZOR_SECRET_FILE``: Optionally specifies the path to a local file where
      secrets are stored, enabling operations in environments where direct API access
      may be restricted or unavailable.

    Example of a local secret file:

    .. code-block:: json

        {
            "my_secret_name": {
                "key": "value"
            }
        }

    Example usage:

    .. code-block:: python

        from automizor import vault

        # Retrieve a secret by its name
        secret = vault.get_secret("my_secret_name")
        print(secret["key"])  # Output: "value"

        # Update a existing secret
        secret = vault.get_secret("my_secret_name")
        secret["new_key"] = "new_value"
        vault.set_secret(secret)
    """

    def __init__(self):
        self._api_host = os.getenv("AUTOMIZOR_API_HOST")
        self._api_token = os.getenv("AUTOMIZOR_API_TOKEN")
        self._secret_file = os.getenv("AUTOMIZOR_SECRET_FILE")

        self.session = requests.Session()
        self.session.headers.update(get_headers(self._api_token))

    def create_secret(self, secret: SecretContainer) -> SecretContainer:
        """
        Creates a new secret. Stores the secret in a local file or in the
        `Automizor API`, based on configuration. If the secret already exists,
        it will be updated.

        Args:
            secret: The secret to create.

        Returns:
            The created secret.

        Raises:
            AutomizorVaultError: If creating the secret fails.
        """

        if self._secret_file:
            return self._write_file_secret(secret)
        try:
            return self._write_vault_secret(secret)
        except AutomizorVaultError:
            return self._create_vault_secret(secret)

    def get_secret(self, name) -> SecretContainer:
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

        if self._secret_file:
            return self._read_file_secret(name)
        return self._read_vault_secret(name)

    def set_secret(self, secret: SecretContainer) -> SecretContainer:
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

        if self._secret_file:
            return self._write_file_secret(secret)
        return self._write_vault_secret(secret)

    def _create_vault_secret(self, secret: SecretContainer) -> SecretContainer:
        url = f"https://{self._api_host}/api/v1/vault/secret/"
        try:
            response = self.session.post(url, timeout=10, json=asdict(secret))
            response.raise_for_status()
            return SecretContainer(**response.json())
        except Exception as exc:
            try:
                msg = exc.response.json()
            except (AttributeError, ValueError):
                msg = str(exc)
            raise AutomizorVaultError(f"Failed to create secret: {msg or exc}") from exc

    def _read_file_secret(self, name: str) -> SecretContainer:
        with open(self._secret_file, "r", encoding="utf-8") as file:
            secrets = json.load(file)
            value = secrets.get(name, {})
        return SecretContainer(name=name, value=value)

    def _read_vault_secret(self, name: str) -> SecretContainer:
        url = f"https://{self._api_host}/api/v1/vault/secret/{name}/"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return SecretContainer(**response.json())
        except Exception as exc:
            try:
                msg = exc.response.json()
            except (AttributeError, ValueError):
                msg = str(exc)
            raise AutomizorVaultError(f"Failed to get secret: {msg}") from exc

    def _write_file_secret(self, secret: SecretContainer):
        with open(self._secret_file, "w+", encoding="utf-8") as file:
            try:
                secrets = json.load(file)
            except json.JSONDecodeError:
                secrets = {}
            secrets[secret.name] = secret.value
            file.seek(0)
            file.write(json.dumps(secrets, indent=4))
            file.truncate()
        return secret

    def _write_vault_secret(self, secret: SecretContainer) -> SecretContainer:
        url = f"https://{self._api_host}/api/v1/vault/secret/{secret.name}/"
        try:
            response = self.session.put(url, timeout=10, json=asdict(secret))
            response.raise_for_status()
            return SecretContainer(**response.json())
        except Exception as exc:
            try:
                msg = exc.response.json()
            except (AttributeError, ValueError):
                msg = str(exc)
            raise AutomizorVaultError(f"Failed to set secret: {msg}") from exc
