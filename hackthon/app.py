import streamlit as st
import time
from agent import GROQ_MODEL, process_incident

st.set_page_config(
    page_title="OpsMind | Hindsight AI Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main { background-color: #0E1117; }
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4F46E5, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header { color: #9CA3AF; font-size: 1rem; margin-bottom: 25px; }
    .memory-box {
        background-color: #0F172A;
        border-left: 4px solid #06B6D4;
        border-radius: 6px;
        padding: 15px;
        font-family: monospace;
        color: #E2E8F0;
    }
    .agent-box {
        background-color: #111827;
        border: 1px solid #1F2937;
        border-radius: 8px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">⚡ OpsMind SRE Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Self-Learning Incident Response System Powered by Vectorize Hindsight</div>', unsafe_allow_html=True)

with st.sidebar:
    st.title("System Status")
    st.success("🟢 Hindsight Engine Connected")
    st.info(f"⚡ Groq Model Active (`{GROQ_MODEL}`)")
    st.divider()
    st.subheader("📊 Memory Bank")
    st.text_input("Active Bank ID", value="devops-incidents-bank", disabled=True)

# Preset Selectors for Fast Live Demos
st.subheader("📝 Incident Input")
preset_option = st.selectbox(
    "Quick Preset Launcher:",
    [
        "Select a preset or type below...",
        "Incident: 504 Gateway Timeout error on authentication service due to Redis lock.",
        "Incident: Database CPU at 99% usage on users table query.",
        "Incident: RabbitMQ consumer connection timeout on production queue."
    ]
)

default_text = "" if preset_option == "Select a preset or type below..." else preset_option
user_input = st.text_area("Incident Log or Description:", value=default_text, height=100)

if st.button("🚀 Analyze & Generate Incident Fix", type="primary", use_container_width=True):
    if not user_input.strip():
        st.error("Please enter an incident description.")
    else:
        start_time = time.time()
        with st.spinner("Searching Hindsight Memory Bank & Synthesizing Fix..."):
            agent_response, recalled_memory = process_incident(user_input)
            latency = round(time.time() - start_time, 2)
            
        st.toast(f"Completed in {latency}s!", icon="⚡")
        st.divider()
        
        col_agent, col_memory = st.columns([6, 5])
        
        with col_agent:
            st.subheader("🤖 Recommended Fix")
            st.markdown(f'<div class="agent-box">{agent_response}</div>', unsafe_allow_html=True)
            
        with col_memory:
            st.subheader("🧠 Recalled Hindsight Context")
            st.caption("Memories retrieved before generating answer")
            if recalled_memory and recalled_memory != "No prior history found.":
                st.markdown(f'<div class="memory-box">{recalled_memory}</div>', unsafe_allow_html=True)
            else:
                st.warning("No prior memories retrieved. Experience retained for future calls.")