import streamlit as st

def render_sidebar(session_id):
    st.sidebar.title("Chat History")
    
    from core.session_manager import get_recent_messages
    
    messages = get_recent_messages(session_id)
    
    # Filter for user messages and display them
    user_messages = [msg["content"] for msg in messages if msg["role"] == "user"]
    
    for message in reversed(user_messages):
        st.sidebar.button(message, use_container_width=True)

def render_chat():
    return st.chat_input("Ask something...")