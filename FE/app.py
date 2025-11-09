import streamlit as st
import requests
import json
import os
import time
from pathlib import Path
from components.chat import chat_interface
from components.docs_viewer import docs_viewer

# =============================================
# CONFIG
# =============================================
API_URL = "http://localhost:8080/generate"
OUTPUT_DIR = "../outputs"

st.set_page_config(
    page_title="Codebase Genius",
    page_icon="robot",
    layout="wide"
)

# =============================================
# SIDEBAR
# =============================================
with st.sidebar:
    st.image("assets/logo.png") if os.path.exists("assets/logo.png") else st.write("## Codebase Genius")
    st.markdown("### Enter a public GitHub repo URL")
    repo_url = st.text_input("GitHub URL", placeholder="https://github.com/psf/requests")
    generate_btn = st.button("Generate Documentation", type="primary", use_container_width=True)

    st.markdown("---")
    st.markdown("**Backend Status**")
    try:
        health = requests.get("http://localhost:8080/health", timeout=2)
        st.success("Backend Running")
    except:
        st.error("Backend Offline")

# =============================================
# MAIN CONTENT
# =============================================
st.title("Codebase Genius")
st.markdown("AI-powered documentation generator for any GitHub repository.")

if generate_btn and repo_url:
    if not repo_url.startswith("https://github.com/"):
        st.error("Please enter a valid public GitHub URL.")
    else:
        with st.spinner("Cloning repository and generating docs..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"repo_url": repo_url},
                    timeout=300  # 5 min
                )
                if response.status_code != 200:
                    st.error(f"Backend error: {response.text}")
                else:
                    result = response.json()
                    docs_path = result.get("docs_path")
                    if docs_path and os.path.exists(docs_path):
                        st.success("Documentation generated!")
                        st.session_state.docs_path = docs_path
                        st.session_state.repo_name = Path(docs_path).parent.name
                    else:
                        st.warning("No docs path returned.")
            except Exception as e:
                st.error(f"Request failed: {e}")

# =============================================
# DISPLAY GENERATED DOCS
# =============================================
if "docs_path" in st.session_state:
    st.markdown("---")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.download_button(
            label="Download Markdown",
            data=Path(st.session_state.docs_path).read_text(),
            file_name=f"{st.session_state.repo_name}_docs.md",
            mime="text/markdown"
        )
    with col2:
        st.markdown(f"**Repo:** `{st.session_state.repo_name}`")

    st.markdown("---")
    docs_viewer(st.session_state.docs_path)

# =============================================
# CHAT INTERFACE (Optional Bonus)
# =============================================
st.markdown("---")
st.markdown("### Ask Questions About the Codebase")
chat_interface()