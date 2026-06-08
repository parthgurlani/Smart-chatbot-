import streamlit as st

from core.tool_router import route_tool

from core.session_manager import (
    add_message
)

from core.memory_manager import (
    update_profile_from_message
)

from core.prompt_builder import (
    build_prompt
)

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
# Constants
# -------------------------

USER_ID = "default_user"
SESSION_ID = "default"

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

model_id = AVAILABLE_MODELS[selected_model_name]

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

    # -------------------------
    # Save User Message
    # -------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    add_message(
        SESSION_ID,
        "user",
        user_message
    )

    update_profile_from_message(
        USER_ID,
        user_message
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    # -------------------------
    # Create Client
    # -------------------------

    client = BedrockClient(
        model_name=model_id
    )

    # -------------------------
    # Generate Response
    # -------------------------

    with st.spinner(
        f"Thinking with {selected_model_name}..."
    ):

        tool_result = route_tool(
            user_message
        )

        # NORMAL QUESTIONS
        if tool_result is None:

            prompt = build_prompt(
                USER_ID,
                SESSION_ID,
                user_message
            )

        # REAL-TIME QUESTIONS
        else:

            st.info(
                f"🔧 Tool Used: {tool_result['tool_used']}"
            )

            prompt = f"""
You are a helpful AI assistant.

The following information comes from a recent web search.

Use this information as the primary source.

{tool_result['context']}

User Question:
{user_message}

Instructions:
- Answer naturally.
- Do not mention DuckDuckGo.
- Do not mention web search.
- Do not mention tools.
- Give a direct answer.
"""

        response = client.generate(
            prompt
        )

    # -------------------------
    # Save Assistant Response
    # -------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    add_message(
        SESSION_ID,
        "assistant",
        response
    )

    # -------------------------
    # Display Assistant Response
    # -------------------------

    with st.chat_message(
        "assistant"
    ):
        st.markdown(response)