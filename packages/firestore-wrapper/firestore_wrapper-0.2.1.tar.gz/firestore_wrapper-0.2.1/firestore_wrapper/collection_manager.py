from __future__ import annotations

from google.cloud.firestore_v1 import DocumentSnapshot

from .firestore_base import FirestoreBase


class CollectionManager(FirestoreBase):

    def __init__(self, credentials_path: str, database: str = None, collections: list[str] = None):
        """
        Initializes the CollectionManager instance.

        :param credentials_path: Path to the Google Cloud service account credentials JSON file.
        :param database: Optional database URL. If provided, this database is used instead of the default.
        :param collections: Optional list of collection names to initialize.
        """
        super().__init__(credentials_path=credentials_path, database=database)
        if collections:
            self.init_collections(collections)

    def add_collection(self, collection_name: str):
        """
        Adds a new collection to the Firestore database.

        :param collection_name: The name of the collection to add.
        """
        self.db.collection(collection_name)

    def init_collections(self, collections: list[str]):
        """
        Initializes multiple collections in the Firestore database.

        :param collections: A list of collection names to initialize.
        """
        for collection in collections:
            self.add_collection(collection)

    def get_collection(self, collection_name: str) -> list[DocumentSnapshot]:
        """
        Retrieves all documents from a specified collection.

        :param collection_name: The name of the collection to retrieve documents from.

        :return: A list of DocumentSnapshot objects for each document in the collection.
        """
        return self.db.collection(collection_name).get()

    def delete_collection(self, collection_name: str):
        """
        Deletes an entire collection, including all documents within it.

        :param collection_name: The name of the collection to delete.
        """
        docs = self.db.collection(collection_name).stream()
        for doc in docs:
            doc.reference.delete()

    def get_collection_size(self, collection_name: str) -> int:
        """
        Returns the number of documents in a collection.

        :param collection_name: The name of the collection.

        :return: The number of documents in the specified collection.
        """
        return len(self.db.collection(collection_name).get())

    def get_collection_names(self) -> list[str]:
        """
        Retrieves the names of all collections in the Firestore database.

        :return: A list of collection names.
        """
        return [collection.id for collection in self.db.collections()]

    def get_collection_data(self, collection_name: str, with_id: bool = False) -> list[dict]:
        """
        Retrieves data for all documents in a specified collection.

        :param collection_name: The name of the collection.
        :param with_id: If True, includes each document's ID with its data.

        :return: A list of dictionaries, each containing data for a document in the collection.
        """
        collection = self.db.collection(collection_name).stream()
        if with_id:
            return [{'id': doc.id, **doc.to_dict()} for doc in collection]
        else:
            return [doc.to_dict() for doc in collection]

    def get_collection_data_as_dict(self, collection_name: str) -> dict:
        """
        Retrieves data for all documents in a specified collection, organized as a dictionary.

        :param collection_name: The name of the collection.

        :return: A dictionary with document IDs as keys and document data dictionaries as values.
        """
        collection = self.db.collection(collection_name).stream()
        ret = {doc.id: doc.to_dict() for doc in collection}
        return ret
