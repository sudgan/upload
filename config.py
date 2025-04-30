from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Azure OpenAI Settings
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str
    
    # Azure Storage Settings
    AZURE_STORAGE_ACCOUNT: str
    AZURE_STORAGE_CONTAINER: str
    
    # Azure Search Settings
    AZURE_SEARCH_SERVICE: str
    AZURE_SEARCH_INDEXER_NAME: str
    
    # Azure Cognitive Search Settings
    AZURE_SEARCH_SERVICE_ENDPOINT: str
    AZURE_SEARCH_ADMIN_KEY: str
    AZURE_SEARCH_INDEX_NAME: str
    
    # Azure Blob Storage Settings
    AZURE_STORAGE_CONNECTION_STRING: str
    AZURE_STORAGE_CONTAINER_NAME: str
    
    # Azure AD Settings
    AZURE_AD_TENANT_ID: str
    AZURE_AD_CLIENT_ID: str
    AZURE_AD_CLIENT_SECRET: str
    
    class Config:
        env_file = ".env"

settings = Settings() 