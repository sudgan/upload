import streamlit as st
import os
import asyncio
from azure_blob import AzureBlobService
from azure_search_indexer import AzureSearchIndexerService
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Azure Document Uploader",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .upload-section {
        padding: 2rem;
        border-radius: 10px;
        background-color: #f0f2f6;
    }
    .status-section {
        padding: 1rem;
        border-radius: 5px;
        background-color: #ffffff;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize services
blob_service = AzureBlobService()
indexer_service = AzureSearchIndexerService()

# Header
st.title("📄 Azure Document Uploader")
st.markdown("Upload files or folders to Azure Blob Storage and trigger AI Search indexing")

# Create two columns for the upload section
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.subheader("📁 Upload Files")
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        accept_multiple_files=True,
        type=['pdf', 'docx', 'txt', 'md']
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.subheader("📂 Upload Folder")
    folder_path = st.text_input("Enter folder path to upload")
    st.markdown('</div>', unsafe_allow_html=True)

# Status section
st.markdown('<div class="status-section">', unsafe_allow_html=True)
st.subheader("📊 Upload Status")
status_placeholder = st.empty()
st.markdown('</div>', unsafe_allow_html=True)

async def process_uploads():
    uploaded_blobs = []
    
    # Process individual files
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save the uploaded file temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            try:
                blob_name = await blob_service.upload_file(temp_path)
                uploaded_blobs.append(blob_name)
                status_placeholder.success(f"✅ Uploaded: {uploaded_file.name}")
            except Exception as e:
                status_placeholder.error(f"❌ Error uploading {uploaded_file.name}: {str(e)}")
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    
    # Process folder
    if folder_path and os.path.exists(folder_path):
        try:
            uploaded_files = await blob_service.upload_folder(folder_path)
            uploaded_blobs.extend(uploaded_files)
            status_placeholder.success(f"✅ Uploaded folder: {folder_path}")
        except Exception as e:
            status_placeholder.error(f"❌ Error uploading folder: {str(e)}")
    
    # Trigger indexer if files were uploaded
    if uploaded_blobs:
        status_placeholder.info("🔄 Triggering Azure AI Search indexer...")
        success = await indexer_service.run_indexer()
        if success:
            status_placeholder.success("✅ Indexer triggered successfully")
        else:
            status_placeholder.error("❌ Failed to trigger indexer")

# Upload button
if st.button("🚀 Start Upload", type="primary"):
    if not uploaded_files and not folder_path:
        st.warning("Please select files or enter a folder path to upload")
    else:
        asyncio.run(process_uploads())

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and Azure") 