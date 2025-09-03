# app.py - Streamlit web application for Travel Assistant
import streamlit as st
import logging
from assistant import TravelAssistant
import os

# --- Page Configuration (do this first) ---
st.set_page_config(
    page_title="Travel Assistant",
    page_icon="✈️",
    layout="centered", # Use centered layout for a cleaner chat-like feel
    initial_sidebar_state="expanded"
)

# --- Custom CSS for a polished look ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5; /* A slightly softer blue */
        text-align: center;
        margin-bottom: 2rem;
    }
    .sidebar-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


# --- State Management ---
# Initialize the TravelAssistant object and message history in the session state.
# This is crucial to ensure the assistant remembers the conversation across reruns.
@st.cache_resource
def get_assistant():
    """Initialize and cache the Travel Assistant to be used across the session."""
    return TravelAssistant()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Load the assistant from the cache
assistant = get_assistant()


# --- Sidebar ---
with st.sidebar:
    # Clear conversation button
    if st.button("🗑️ New Conversation", help="Clear the chat history and start fresh."):
        st.session_state.messages = []
        # We need to re-initialize the assistant to clear its internal history too
        st.cache_resource.clear()
        st.rerun()
    
    st.markdown("---")
    
    # Information panel
    st.markdown("""
    <div class="sidebar-info">
    <strong>Assistant Features:</strong><br>
    • 🌍 Destination recommendations<br>
    • 🎒 Packing suggestions<br>
    • 🌤️ Real-time weather info<br>
    • 🏛️ Local attractions<br>
    • 🧠 Smart reasoning
    </div>
    """, unsafe_allow_html=True)
    
    # Settings
    reasoning_mode = st.toggle("Show Assistant's Reasoning", help="When enabled, the assistant will show its step-by-step thinking process for complex questions.")
    
    # Set environment variable based on the toggle state for the assistant to use
    os.environ["SHOW_CHAIN_OF_THOUGHT"] = "true" if reasoning_mode else "false"


# --- Main Chat Interface ---
st.markdown('<h1 class="main-header">✈️ Travel Assistant</h1>', unsafe_allow_html=True)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me about destinations, packing, or weather..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if assistant:
                    response = assistant.get_response(prompt)
                    st.markdown(response)
                else:
                    response = "Sorry, the assistant could not be initialized. Please check your API keys."
                    st.error(response)
            except Exception as e:
                response = f"An unexpected error occurred: {str(e)}"
                st.error(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
