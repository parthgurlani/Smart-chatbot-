import time
import streamlit as st

from core.session_manager import add_message
from core.memory_manager import update_profile_from_message
from core.context_manager import ContextManager
from tools.search_tool import search_web
from infrastructure.logger import AgentLogger

from agents.router_agent import RouterAgent
from agents.registry import AgentRegistry
import agents.domain_agents  # Executes decorators

# UI
from ui.streamlit_ui import render_sidebar, render_chat


# -------------------------
# Constants & Config
# -------------------------
USER_ID = "default_user"
SESSION_ID = "default"

st.set_page_config(
    page_title="Multi-Agent Bedrock Platform",
    layout="wide",
    page_icon="🧠"
)

st.markdown(
    """
    <div style="text-align: center;">
        <h1>🧠 Multi-Agent Bedrock Platform</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")


# -------------------------
# Session State
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_route" not in st.session_state:
    st.session_state.last_route = None

if "last_metrics" not in st.session_state:
    st.session_state.last_metrics = None


# -------------------------
# Sidebar
# -------------------------
render_sidebar(SESSION_ID)


# -------------------------
# Render Existing Messages
# -------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -------------------------
# Chat Input
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
    # Intent Classification
    # -------------------------
    with st.spinner("Classifying intent..."):

        router = RouterAgent()

        route_data = router.classify_intent(
            user_message
        )

        st.session_state.last_route = route_data

        domain = route_data.get(
            "domain",
            "general"
        )

        needs_search = route_data.get(
            "needs_search",
            False
        )

        agent_class = AgentRegistry.get_agent(
            domain
        )

        active_agent = agent_class()

    # -------------------------
    # Agent Execution
    # -------------------------
    with st.spinner(
        f"Agent '{domain.upper()}' is thinking..."
    ):

        search_results_text = ""

        # -------------------------
        # Search Tool
        # -------------------------
        if needs_search:

            with st.spinner("Searching the web..."):

                raw_results, error = search_web(
                    user_message
                )

                if error:

                    st.error(
                        f"Failed to fetch live data: {error}"
                    )

                elif not raw_results:

                    st.warning(
                        "No search results found."
                    )

                else:

                    search_results_text = "\n\n".join(
                        [
                            f"Title: {r.get('title')}\n"
                            f"Content: {r.get('body')}"
                            for r in raw_results
                        ]
                    )

        # -------------------------
        # Context Hydration
        # -------------------------
        context = ContextManager.hydrate_context(
            USER_ID,
            SESSION_ID
        )

        # -------------------------
        # LLM Generation
        # -------------------------
        start_time = time.time()

        result = active_agent.execute(
            user_message,
            context,
            search_results_text
        )

        latency = time.time() - start_time

        # -------------------------
        # Extract Response
        # -------------------------
        response = result.get(
            "answer",
            "No response generated."
        )

        input_tokens = result.get(
            "input_tokens",
            0
        )

        output_tokens = result.get(
            "output_tokens",
            0
        )

        total_tokens = result.get(
            "total_tokens",
            0
        )

        # -------------------------
        # Store Metrics
        # -------------------------
        st.session_state.last_metrics = {
            "latency": round(latency, 2),
            "model": active_agent.model_id,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens
        }

        # -------------------------
        # Logging
        # -------------------------
        AgentLogger.log_execution(
            query=user_message,
            agent=domain,
            model=active_agent.model_id,
            needs_search=needs_search,

            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,

            response_time=latency
        )

    # -------------------------
    # Save Assistant Message
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
    # Render Assistant Message
    # -------------------------
    with st.chat_message("assistant"):
        st.markdown(response)

        with st.expander("📊 Token Usage"):

            st.write(
                f"Input Tokens: {input_tokens}"
            )

            st.write(
                f"Output Tokens: {output_tokens}"
            )

            st.write(
                f"Total Tokens: {total_tokens}"
            )

            st.write(
                f"Latency: {round(latency, 2)} sec"
            )

    st.rerun()