from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from ..services.azure_search import AzureSearchService
from ..services.azure_openai import AzureOpenAIService

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[dict]

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    search_service = AzureSearchService()
    openai_service = AzureOpenAIService()
    
    # Retrieve relevant documents
    documents = await search_service.search_documents(request.query)
    
    if not documents:
        raise HTTPException(status_code=404, content="No relevant information found")
    
    # Prepare context from retrieved documents
    context = "\n\n".join([f"Source {i+1}: {doc['content']}" for i, doc in enumerate(documents)])
    
    # Generate response using Azure OpenAI
    system_prompt = """You are a knowledgeable assistant. Use only the information provided in the retrieved documents to answer the user's question. Do not use prior knowledge unless explicitly instructed.

If the answer is not available in the documents, respond politely and let the user know.

GUIDELINES:
- Be accurate, concise, and specific.
- Reference the relevant document snippet(s) when necessary.
- Maintain a professional but helpful tone."""
    
    response = await openai_service.generate_response(
        system_prompt=system_prompt,
        user_query=request.query,
        context=context
    )
    
    return ChatResponse(
        response=response,
        sources=[{"id": doc["id"], "source": doc["source"]} for doc in documents]
    ) 