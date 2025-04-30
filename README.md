# Azure Document Uploader

A Streamlit web application for uploading files and folders to Azure Blob Storage and triggering Azure AI Search indexing.

## Features

- Upload multiple files or entire folders
- Automatic Azure Blob Storage integration
- Azure AI Search indexer triggering
- Clean and modern UI with status updates
- Support for various file types (PDF, DOCX, TXT, MD)

## Prerequisites

- Python 3.8+
- Azure account with:
  - Azure Storage Account
  - Azure AI Search service
  - Azure OpenAI service

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following variables:
   ```
   # Azure OpenAI Settings
   AZURE_OPENAI_API_KEY=your_openai_api_key
   AZURE_OPENAI_ENDPOINT=your_openai_endpoint
   AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name

   # Azure Storage Settings
   AZURE_STORAGE_ACCOUNT=your_storage_account
   AZURE_STORAGE_CONTAINER=your_container_name

   # Azure Search Settings
   AZURE_SEARCH_SERVICE=your_search_service
   AZURE_SEARCH_INDEXER_NAME=your_indexer_name
   ```

## Running the Application

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the provided URL (usually http://localhost:8501)

## Usage

1. **Upload Files**:
   - Use the file uploader to select multiple files
   - Supported formats: PDF, DOCX, TXT, MD

2. **Upload Folder**:
   - Enter the full path to the folder you want to upload
   - All files in the folder will be uploaded maintaining the folder structure

3. **Start Upload**:
   - Click the "Start Upload" button to begin the process
   - Monitor the status section for upload progress and results

## Security Notes

- Never commit your `.env` file to version control
- Ensure proper access controls are set up in Azure
- Use managed identities where possible for production deployments

## License

MIT License 