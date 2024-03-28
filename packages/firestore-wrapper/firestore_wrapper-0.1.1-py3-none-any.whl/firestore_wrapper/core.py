from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from typing import Callable

from google.cloud import firestore
from google.cloud.firestore_v1 import DocumentSnapshot, FieldFilter
from google.oauth2 import service_account


def flatten_dict(dd: dict, separator: str = '__', prefix: str = ''):
    return {prefix + separator + k if prefix else k: v
            for kk, vv in dd.items()
            for k, v in (flatten_dict(vv, separator, kk).items()
                         if isinstance(vv, dict) else [(kk, vv)])}


class FirestoreDB:

    def __init__(self, credentials_path: str, database: str = None, collections: list[str] = None,
                 backup_folder: str = None):
        """
        Initializes the FirestoreDB instance.

        :param credentials_path: Path to the Google Cloud service account credentials JSON file.
        :param database: Optional database URL. If provided, this database is used instead of the default.
        :param collections: Optional list of collection names to initialize.
        :param backup_folder: Optional path to a folder where backups will be stored.
        """
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.db = firestore.Client(credentials=self.credentials, database=database)
        if collections:
            self.init_collections(collections)
        self._backup_folder = backup_folder
        self.collections_to_backup = collections
        self.ensure_backup()

    @property
    def backup_folder(self) -> str:
        v = self._backup_folder
        if '~' in v:
            v = os.path.expanduser(v)
        return v

    @backup_folder.setter
    def backup_folder(self, value: str):
        self._backup_folder = value

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

    def add_document(self, collection_name: str, data: dict, document_name: str = None, id_as_name: bool = False,
                     validator: Callable[[dict], None] = None, merge_if_existing: bool = False) -> str:
        """
        Adds a new document to a specified collection.

        :param collection_name: The name of the collection.
        :param data: The data for the document as a dictionary.
        :param document_name: Optional specific name for the document. Required if id_as_name is False.
        :param id_as_name: If True, a unique ID will be generated for the document name.
        :param validator: Optional callable that validates the data dictionary.
        :param merge_if_existing: If True, merge data into an existing document instead of overwriting.

        :return: The name of the document.
        """
        if not document_name and not id_as_name:
            raise ValueError('document_name must be provided if id_as_name is False')
        if document_name and id_as_name:
            raise ValueError('document_name will be ignored if id_as_name is True')
        if validator:
            validator(data)
        if id_as_name:
            document_name = self.db.collection(collection_name).document().id
        self.db.collection(collection_name).document(document_name).set(data, merge=merge_if_existing)
        return document_name

    def add_documents_batch(self, collection_name: str, data_list: list[dict], document_names: list[str] = None,
                            validator: Callable[[dict], None] = None, overwrite: bool = False, verbose: bool = False):
        """
        Adds or updates multiple documents in a specified collection using batch operations.

        :param collection_name: The collection to which documents will be added.
        :param data_list: List of data dictionaries for each document.
        :param document_names: Optional list of names for each document. Must match the length of data_list if provided.
        :param validator: Optional callable to validate each document's data.
        :param overwrite: If True, existing documents will be overwritten. If False, they will be ignored.
        :param verbose: If True, print additional information during the operation.
        """
        existing_doc_names = self.get_document_names(collection_name)
        max_batch_size = 500  # Firestore's limit

        chunks = [data_list[i:i + max_batch_size] for i in range(0, len(data_list), max_batch_size)]
        name_chunks = [document_names[i:i + max_batch_size] if document_names else None for i in
                       range(0, len(document_names or []), max_batch_size)]

        for chunk_index, chunk in enumerate(chunks):
            batch = self.db.batch()
            names_chunk = name_chunks[chunk_index] if name_chunks else [None] * len(chunk)

            for index, data in enumerate(chunk):
                if validator:
                    validator(data)

                document_name = names_chunk[index] if names_chunk else None
                if document_name is None or document_name not in existing_doc_names or overwrite:
                    doc_ref = self.db.collection(collection_name).document(document_name)
                    batch.set(doc_ref, data)
                elif verbose:
                    print(f"Document with name '{document_name}' already exists. Skipping...")

            try:
                batch.commit()
                if verbose:
                    print(f"Batch {chunk_index + 1} write successful.")
            except Exception as e:
                print(f"Batch {chunk_index + 1} write failed: {e}")

    def add_data(self, collection_name: str, data: dict):
        self.db.collection(collection_name).add(data)

    def get_document(self, collection_name: str, document_name: str) -> DocumentSnapshot:
        """
        Retrieves a document from a specified collection.

        :param collection_name: The name of the collection.
        :param document_name: The name of the document to retrieve.

        :return: A DocumentSnapshot object of the retrieved document.
        """
        return self.db.collection(collection_name).document(document_name).get()

    def get_collection(self, collection_name: str) -> list[DocumentSnapshot]:
        """
        Retrieves all documents from a specified collection.

        :param collection_name: The name of the collection to retrieve documents from.

        :return: A list of DocumentSnapshot objects for each document in the collection.
        """
        return self.db.collection(collection_name).get()

    def update_document(self, collection_name: str, document_name: str, data: dict,
                        validator: Callable[[dict], None] = None, create_if_missing: bool = False):
        """
        Updates a document in a specified collection. Optionally creates the document if it does not exist.

        :param collection_name: The name of the collection.
        :param document_name: The name of the document to update.
        :param data: The data to update the document with.
        :param validator: Optional callable to validate the data dictionary.
        :param create_if_missing: If True, create the document if it does not exist.
        """
        if create_if_missing:
            return self.add_document(collection_name, data, document_name, validator=validator, merge_if_existing=True)
        else:
            if validator:
                validator(data)
            self.db.collection(collection_name).document(document_name).update(data)

    def delete_document(self, collection_name: str, document_name: str):
        """
        Deletes a specific document from a collection.

        :param collection_name: The name of the collection containing the document.
        :param document_name: The name of the document to delete.
        """
        self.db.collection(collection_name).document(document_name).delete()

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

    def get_document_names(self, collection_name: str) -> list[str]:
        """
        Retrieves the names of all documents in a specified collection.

        :param collection_name: The name of the collection.

        :return: A list of document names in the specified collection.
        """
        return [doc.id for doc in self.db.collection(collection_name).stream()]

    def get_document_data(self, collection_name: str, document_name: str, with_id: bool = False) -> dict:
        """
        Retrieves the data of a specified document in a collection.

        :param collection_name: The name of the collection.
        :param document_name: The name of the document.
        :param with_id: If True, includes the document's ID in the returned dictionary.

        :return: A dictionary containing the document's data.
        """
        document = self.db.collection(collection_name).document(document_name).get()
        if with_id:
            return {'id': document.id, **document.to_dict()}
        else:
            return document.to_dict()

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

    def change_field_name(self, collection_name: str, document_name: str, old_field_name: str, new_field_name: str):
        """
        Renames a field in a specific document within a collection.

        :param collection_name: The name of the collection.
        :param document_name: The name of the document.
        :param old_field_name: The current name of the field.
        :param new_field_name: The new name for the field.
        """
        doc = self.db.collection(collection_name).document(document_name)
        data = doc.get().to_dict()
        data[new_field_name] = data.pop(old_field_name)
        doc.update(data)

    def change_field_name_for_all_documents(self, collection_name: str, old_field_name: str, new_field_name: str,
                                            remove_old_field: bool = True):
        """
        Renames a field for all documents in a specified collection.

        :param collection_name: The name of the collection.
        :param old_field_name: The current name of the field.
        :param new_field_name: The new name for the field.
        :param remove_old_field: If True, the old field name is removed from the documents.
        """
        docs = self.db.collection(collection_name).stream()
        for doc in docs:
            data = doc.to_dict()
            if old_field_name not in data:
                continue
            data[new_field_name] = data.pop(old_field_name)
            doc.reference.update(data)
            if remove_old_field:
                doc.reference.update({old_field_name: firestore.DELETE_FIELD})

    def parse_field_from_string_to_float_for_all_documents(self, collection_name: str, field_name: str):
        """
        Parses a specified field from string to float for all documents in a collection.

        :param collection_name: The name of the collection.
        :param field_name: The name of the field to parse.
        """
        docs = self.db.collection(collection_name).stream()
        for doc in docs:
            data = doc.to_dict()
            if field_name not in data:
                continue
            data[field_name] = float(data[field_name])
            doc.reference.update(data)

    def save_collections_backup(self, collections: list[str] = None):
        """
        Saves a backup of specified collections or all collections if none are specified. The backup is saved in the
        backup folder specified during the initialization of the FirestoreDB instance.

        :param collections: Optional list of collection names to back up. If None, backs up all collections.
        """
        if not self.backup_folder:
            print('Property backup_folder must be provided to save backup. Nothing will be done.')
            return
        base_folder = self.backup_folder
        collection_names = collections or self.collections_to_backup or self.get_collection_names()

        backup_time = datetime.now().strftime("%Y-%m-%d %H%M%S")
        backup_path = os.path.join(base_folder, 'db_backup', backup_time)
        os.makedirs(backup_path, exist_ok=True)

        for collection_name in collection_names:
            collection_data = self.get_collection_data_as_dict(collection_name)
            file_path = os.path.join(backup_path, f"{collection_name}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(collection_data, f, ensure_ascii=False, indent=4)

        print(f"Backup completed at {backup_path}")

    def ensure_backup(self, max_days: int = 7):
        """
        Ensures that a backup is taken if the latest backup is older than the specified number of days. If no backup
        exists, or the latest backup is too old, a new backup is created.

        :param max_days: The maximum number of days that can elapse before a new backup is required.
        """
        if not self.backup_folder:
            print('Property backup_folder must be provided to save backup. Nothing will be done.')
            return

        backup_base_path = os.path.join(self.backup_folder, 'db_backup')

        if not os.path.exists(backup_base_path):
            self.save_collections_backup()
            return

        backup_dirs = [d for d in os.listdir(backup_base_path) if os.path.isdir(os.path.join(backup_base_path, d))]
        backup_dates = []
        for dir_name in backup_dirs:
            try:
                backup_date = datetime.strptime(dir_name, "%Y-%m-%d %H%M%S")
                backup_dates.append(backup_date)
            except ValueError:
                continue

        if backup_dates:
            latest_backup_date = max(backup_dates)
            if datetime.now() - latest_backup_date > timedelta(days=max_days):
                self.save_collections_backup()
            else:
                print("A recent DB backup already exists. No new backup needed.")
                print(f"Latest DB backup: {latest_backup_date}")
        else:
            self.save_collections_backup()
