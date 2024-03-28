from azure.data.tables import TableServiceClient, TableClient 
from azure.core.exceptions import ResourceExistsError
from azure.core.credentials import AzureNamedKeyCredential
import logging
from azure_storage_provider.lib.config import flow_config
import uuid

class AzureTableStorage:
    """
    A class for interacting with Azure Table Storage.

    :param account_name: The Azure Storage account name.
    :param account_key: The Azure Storage account key.
    :param azure_table_name: The name of the Azure table (default: "").
    :param flow_name: The name of the flow (default: "").
    """

    def __init__(self, account_name, account_key, azure_table_name="", flow_name=""):
        """
        Initialize the AzureTableStorage.

        This method creates a connection to the Azure Table Storage.

        :param account_name: The Azure Storage account name.
        :param account_key: The Azure Storage account key.
        :param azure_table_name: The name of the Azure table (default: "").
        :param flow_name: The name of the flow (default: "").
        """
        self.azure_table_config = {"account_name": account_name, "account_key": account_key, "azure_table_name": azure_table_name, "flow_name": flow_name}
        azure_credential = AzureNamedKeyCredential(account_name, account_key)
        table_service_client = TableServiceClient(endpoint=f"https://{account_name}.table.core.windows.net", credential=azure_credential)
        self.chunk_size = 100
        try:
            table_client = table_service_client.create_table(azure_table_name)
            self.table_client = table_client
            logging.info("Connected to Azure Table Storage. Table created.")
        except ResourceExistsError:
            table_client = table_service_client.get_table_client(azure_table_name)
            self.table_client = table_client
            logging.error("Connected to Azure Table Storage. Table already exists.")

    def create_file_entity(self, PartitionKey, RowKey, ErrorResult, Result, Status):
        """
        Create an entity for a file in Azure Table Storage.

        :param PartitionKey: The partition key for the entity.
        :param RowKey: The row key for the entity.
        :param ErrorResult: The error result for the entity.
        :param Result: The result for the entity.
        :param Status: The status for the entity.
        :return: A dictionary representing the entity.
        """
        return {"PartitionKey": PartitionKey, "RowKey": RowKey, "ErrorResult": ErrorResult, "Result": Result, "Status": Status }

    def create_row_entity(self, ErrorRows=[], file_name=""):
        """
        Create entities for rows in Azure Table Storage.

        :param ErrorRows: List of error rows.
        :param file_name: The name of the file.
        :return: List of dictionaries representing entities for rows.
        """
        result = []
        for row in ErrorRows:
            result.append({"PartitionKey": flow_config["flow_name"], "RowKey": uuid.uuid4(), "UID": row[flow_config["primary_key"]], "FileName": file_name, "Error": row["Status"]})
        return result

    def chunks(self, lst, chunk_size):
        """
        Split a list into chunks.

        :param lst: The list to be split.
        :param chunk_size: The size of each chunk.
        :return: Generator yielding chunks of the list.
        """
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]

    def create_row_entity_batch(self, ErrorRows=[], file_name=""):
        """
        Create entities for rows in Azure Table Storage as a batch.

        :param ErrorRows: List of error rows.
        :param file_name: The name of the file.
        :return: List of tuples representing entities for rows as a batch.
        """
        result = []
        for row in ErrorRows:
            result.append(("upsert", {"PartitionKey": flow_config["flow_name"], "RowKey": str(uuid.uuid4()), "UID": row[flow_config["primary_key"]], "FileName": file_name, "Error": row["Status"]}))
        return result

    def insertion(self, entities=[]):
        """
        Insert entities into Azure Table Storage.

        :param entities: List of entities to be inserted.
        """
        for entity in entities:
            try:
                self.table_client.create_entity(entity=entity)
            except Exception as e:
                logging.error(f"Error during table insertion: {e}")

    def insertion_batch(self, entities=[]):
        """
        Insert entities into Azure Table Storage as a batch.

        :param entities: List of entities to be inserted as a batch.
        """
        list_chunks = list(self.chunks(entities, self.chunk_size))
        for chunk in list_chunks:
            self.table_client.submit_transaction(chunk)
