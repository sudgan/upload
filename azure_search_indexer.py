from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import SearchIndexer
from azure.identity import DefaultAzureCredential
from ..config import settings

class AzureSearchIndexerService:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.indexer_client = SearchIndexerClient(
            endpoint=f"https://{settings.AZURE_SEARCH_SERVICE}.search.windows.net",
            credential=self.credential
        )

    async def run_indexer(self, indexer_name: str = None) -> bool:
        """Run the Azure AI Search indexer"""
        if indexer_name is None:
            indexer_name = settings.AZURE_SEARCH_INDEXER_NAME

        try:
            self.indexer_client.run_indexer(indexer_name)
            return True
        except Exception as e:
            print(f"Error running indexer: {str(e)}")
            return False

    async def get_indexer_status(self, indexer_name: str = None) -> dict:
        """Get the current status of the indexer"""
        if indexer_name is None:
            indexer_name = settings.AZURE_SEARCH_INDEXER_NAME

        try:
            status = self.indexer_client.get_indexer_status(indexer_name)
            return {
                "status": status.status,
                "last_result": status.last_result,
                "execution_history": status.execution_history
            }
        except Exception as e:
            print(f"Error getting indexer status: {str(e)}")
            return {"error": str(e)} 