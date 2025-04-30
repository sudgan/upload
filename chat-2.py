import streamlit as st
import requests
from typing import Dict, List

def render_chat_page():
    st.title("Chat with Knowledge Base")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message:
                st.markdown("**Sources:**")
                for source in message["sources"]:
                    st.markdown(f"- {source['source']}")
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={"query": prompt}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.markdown(data["response"])
                    if data["sources"]:
                        st.markdown("**Sources:**")
                        for source in data["sources"]:
                            st.markdown(f"- {source['source']}")
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["response"],
                        "sources": data["sources"]
                    })
                else:
                    st.error("Failed to get response from the assistant")

if __name__ == "__main__":
    render_chat_page() 