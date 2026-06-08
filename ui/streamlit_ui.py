import streamlit as st

from models.model_router import (
    AVAILABLE_MODELS
)


def render_sidebar():

    model = st.sidebar.selectbox(
        "Select Model",
        list(AVAILABLE_MODELS.keys())
    )

    return model


def render_chat():

    user_message = st.chat_input(
        "Ask something..."
    )

    return user_message