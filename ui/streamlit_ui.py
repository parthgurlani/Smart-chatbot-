import streamlit as st

def render_sidebar(session_id):
    st.sidebar.title("Chat History")

    from core.session_manager import get_recent_messages

    # Get messages from session
    messages = get_recent_messages(session_id)

    # Extract only user messages
    user_messages = [
        msg["content"]
        for msg in messages
        if msg.get("role") == "user"
    ]

    # Display latest messages first
    for i, message in enumerate(reversed(user_messages)):
        # Limit long messages in sidebar
        preview = (
            message[:40] + "..."
            if len(message) > 40
            else message
        )

        # Unique key prevents duplicate button error
        if st.sidebar.button(
            preview,
            key=f"history_btn_{i}",
            use_container_width=True
        ):
            st.session_state["selected_history"] = message

def render_chat():
    return st.chat_input("Ask something...")