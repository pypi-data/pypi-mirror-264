from __future__ import annotations

from google.cloud.firestore_v1 import FieldFilter

from .firestore_base import FirestoreBase


class QueryManager(FirestoreBase):

    def __init__(self, credentials_path: str, database: str = None):
        """
        Initializes the QueryManager instance.

        :param credentials_path: Path to the Google Cloud service account credentials JSON file.
        :param database: Optional database URL. If provided, this database is used instead of the default.
        """
        super().__init__(credentials_path=credentials_path, database=database)

    def get_collection_document_by_field(self, collection_name: str, field_name: str, field_value: str):
        """
        Retrieves documents from a collection where the specified field has the specified value.

        :param collection_name: The name of the collection.
        :param field_name: The name of the field to filter by.
        :param field_value: The value to match for the specified field.

        :return: An iterable of DocumentSnapshot objects for documents matching the criteria.
        """
        field_filter = FieldFilter(field_name, '==', field_value)
        return self.db.collection(collection_name).where(filter=field_filter).stream()

    def get_collection_data_by_field(self, collection_name: str, field_name: str, field_value: str) -> list[dict]:
        """
        Retrieves data for documents in a specified collection where the field matches a specified value.

        :param collection_name: The name of the collection.
        :param field_name: The field name to filter documents by.
        :param field_value: The field value to search for.

        :return: A list of dictionaries containing the data of matching documents.
        """
        data = self.get_collection_document_by_field(collection_name, field_name, field_value)
        return [doc.to_dict() for doc in data]
