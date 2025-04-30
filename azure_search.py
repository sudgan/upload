from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType,
)
from ..config import settings

class AzureSearchService:
    def __init__(self):
        self.credential = AzureKeyCredential(settings.AZURE_SEARCH_ADMIN_KEY)
        self.index_client = SearchIndexClient(
            endpoint=settings.AZURE_SEARCH_SERVICE_ENDPOINT,
            credential=self.credential
        )
        self.search_client = SearchClient(
            endpoint=settings.AZURE_SEARCH_SERVICE_ENDPOINT,
            index_name=settings.AZURE_SEARCH_INDEX_NAME,
            credential=self.credential
        )
    
    def create_index(self):
        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SearchableField(name="content", type=SearchFieldDataType.String),
            SimpleField(name="source", type=SearchFieldDataType.String),
            SimpleField(name="timestamp", type=SearchFieldDataType.DateTimeOffset),
            SimpleField(name="metadata", type=SearchFieldDataType.String)
        ]
        
        index = SearchIndex(name=settings.AZURE_SEARCH_INDEX_NAME, fields=fields)
        self.index_client.create_or_update_index(index)
    
    async def search_documents(self, query: str, top: int = 3):
        results = self.search_client.search(
            search_text=query,
            top=top,
            select=["id", "content", "source"],
            highlight_fields="content"
        )
        return [dict(result) for result in results]
    
    async def upload_documents(self, documents: list):
        return self.search_client.upload_documents(documents) 