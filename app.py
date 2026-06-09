import time
import streamlit as st

from core.session_manager import add_message
from core.memory_manager import update_profile_from_message
from core.context_manager import ContextManager
from tools.search_tool import search_web
from infrastructure.logger import AgentLogger

from agents.router_agent import RouterAgent
from agents.registry import AgentRegistry
import agents.domain_agents  # Executes the decorators to register agents

from ui.streamlit_ui import render_sidebar, render_chat

# -------------------------
# Constants & Config
# -------------------------
USER_ID = "default_user"
SESSION_ID = "default"

st.set_page_config(page_title="Multi-Agent Bedrock Platform", layout="wide", page_icon="🧠")

st.markdown(
    """
    <div style="text-align: center;">
        <h1>🧠 Multi-Agent Bedrock Platform</h1>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")

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
# Display Chat History
# -------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------
# Main Execution Loop
# -------------------------
user_message = render_chat()

if user_message:
    # 1. Save User Input
    st.session_state.messages.append({"role": "user", "content": user_message})
    add_message(SESSION_ID, "user", user_message)
    update_profile_from_message(USER_ID, user_message)
    
    with st.chat_message("user"):
        st.markdown(user_message)

    with st.spinner("Classifying intent..."):
        # 2. Intelligent Routing Phase
        router = RouterAgent()
        route_data = router.classify_intent(user_message)
        st.session_state.last_route = route_data
        
        domain = route_data.get("domain", "general")
        needs_search = route_data.get("needs_search", False)

        # 3. Agent Instantiation
        agent_class = AgentRegistry.get_agent(domain)
        active_agent = agent_class()

    with st.spinner(f"Agent '{domain.upper()}' is thinking..."):
        # 4. Tool Execution Phase
        search_results_text = ""
        if needs_search:
            with st.spinner("Searching the web..."):
                raw_results, error = search_web(user_message)
                if error:
                    st.error(f"Failed to fetch live data: {error}")
                elif not raw_results:
                    st.warning("No search results found.")
                else:
                    search_results_text = "\n\n".join(
                        [f"Title: {r.get('title')}\nContent: {r.get('body')}" for r in raw_results]
                    )

        # 5. Context Hydration
        context = ContextManager.hydrate_context(USER_ID, SESSION_ID)

        # 6. Generation Phase
        start_time = time.time()
        response = active_agent.execute(user_message, context, search_results_text)
        latency = time.time() - start_time
        
        # Update metrics for UI
        st.session_state.last_metrics = {
            "latency": latency,
            "model": active_agent.model_id
        }

        # 7. Telemetry & Storage
        AgentLogger.log_execution(
            query=user_message,
            agent=domain,
            model=active_agent.model_id,
            needs_search=needs_search,
            response_time=latency
        )

    # 8. Render Response
    st.session_state.messages.append({"role": "assistant", "content": response})
    add_message(SESSION_ID, "assistant", response)

    with st.chat_message("assistant"):
        st.markdown(response)
        
    st.rerun() # Refresh UI to update sidebar metrics