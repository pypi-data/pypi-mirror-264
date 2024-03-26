import os
import platform
import warnings
from typing import Optional


class CredentialFetcher:
    PERSISTENCE_DIR = (
        os.path.join(os.getenv("APPDATA"), "deci", "auth")
        if platform.system() == "Windows"
        else os.path.join("~/.deci", "auth")
    )
    CREDENTIAL_FILE = "credentials"

    def __init__(self, persistence_dir: str = PERSISTENCE_DIR, credentials_file: str = CREDENTIAL_FILE) -> None:
        super().__init__()
        self.persistence_dir = persistence_dir
        self.credentials_file = credentials_file
        os.makedirs(self.persistence_dir, exist_ok=True)

    def store_credential(self, key: str, value: str):
        existing_credentials = self.get_credentials()
        existing_credentials.update({key: value})

        with open(os.path.join(self.persistence_dir, self.credentials_file), "w") as f:
            for k, v in existing_credentials.items():
                f.write(f"{k}={v}\n")

    def get_credential(self, key: str) -> Optional[str]:
        credentials = self.get_credentials()
        if key in credentials:
            return credentials[key]

        warnings.warn(f"credential {key} not found in {self.persistence_dir}/{self.credentials_file}")
        return None

    def get_credentials(self) -> dict:
        credentials_path = os.path.join(self.persistence_dir, self.credentials_file)

        credentials = dict()

        if not os.path.exists(credentials_path) or not os.access(credentials_path, os.R_OK):
            return credentials

        with open(credentials_path, "r") as f:
            for line in f:
                key, value = line.strip().split("=", 1)  # support possible multiple '='s
                credentials[key] = value

        return credentials
