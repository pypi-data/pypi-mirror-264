from __future__ import annotations

from google.cloud import firestore
from google.oauth2 import service_account


def flatten_dict(dd: dict, separator: str = '__', prefix: str = ''):
    return {prefix + separator + k if prefix else k: v
            for kk, vv in dd.items()
            for k, v in (flatten_dict(vv, separator, kk).items()
                         if isinstance(vv, dict) else [(kk, vv)])}


class BaseManager:

    def __init__(self, credentials_path: str, database: str = None):
        """
        Initializes the FirestoreDB instance.

        :param credentials_path: Path to the Google Cloud service account credentials JSON file.
        :param database: Optional database URL. If provided, this database is used instead of the default.
        """
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.db = firestore.Client(credentials=self.credentials, database=database)
