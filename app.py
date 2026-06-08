import streamlit as st

from ui.streamlit_ui import (
    render_sidebar,
    render_chat
)

from models.model_router import (
    AVAILABLE_MODELS
)

from models.bedrock_client import (
    BedrockClient
)

# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="BedrockRouter Smart Chatbot",
    layout="wide"
)

st.title("🤖 BedrockRouter Smart Chatbot")

# -------------------------
# Session State
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# Sidebar
# -------------------------

selected_model_name = render_sidebar()

model_id = AVAILABLE_MODELS[
    selected_model_name
]

st.sidebar.write(
    f"Model ID:\n\n{model_id}"
)

# -------------------------
# Display Chat History
# -------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )

# -------------------------
# User Input
# -------------------------

user_message = render_chat()

if user_message:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    # Create client
    client = BedrockClient(
        model_name=model_id
    )

    # Generate response
    with st.spinner(
        f"Thinking with {selected_model_name}..."
    ):

        response = client.generate(
            user_message
        )

    # Store assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    # Display assistant response
    with st.chat_message(
        "assistant"
    ):
        st.markdown(response)