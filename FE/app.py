import streamlit as st
import requests
import os
from pathlib import Path

from components.chat import chat_interface
from components.docs_viewer import docs_viewer

# CONFIGURATION
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")
API_URL = f"{BACKEND_URL}/generate"
HEALTH_URL = f"{BACKEND_URL}/health"
OUTPUT_DIR = "../outputs"

st.set_page_config(
    page_title="Codebase Genius",
    page_icon="🤖",
    layout="wide",
)

# SIDEBAR
with st.sidebar:
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", use_container_width=True)
    else:
        st.title("Codebase Genius")

    # st.markdown("### Enter a public GitHub repo URL")
    # repo_url = st.text_input(
    #     "GitHub URL",
    #     placeholder="https://github.com/psf/requests",
    # )
    # generate_btn = st.button(
    #     "Generate Documentation",
    #     type="primary",
    #     use_container_width=True,
    # )

    st.markdown("---")
    st.markdown("**Backend Status**")
    try:
        health = requests.get(HEALTH_URL, timeout=2)
        if health.status_code == 200:
            st.success("Backend Running")
        else:
            st.warning("Backend response not OK")
    except Exception:
        st.error("Backend Offline")

# MAIN PAGE
st.title("Codebase Genius")
st.markdown(
    "AI-powered documentation generator for any public GitHub repository, "
    "backed by Jac + byLLM + Gemini 2.5 Flash."
)

st.markdown("---")
st.markdown("### Enter a public GitHub repo URL")
repo_url = st.text_input(
        "GitHub URL",
        placeholder="https://github.com/psf/requests",
    )
generate_btn = st.button(
        "Generate Documentation",
        type="primary",
        use_container_width=True,
    )
st.markdown("---")

# Handle generation request
if generate_btn and repo_url:
    if not repo_url.startswith("https://github.com/"):
        st.error("Please enter a valid public GitHub URL.")
    else:
        with st.spinner("Generating documentation with Gemini 2.5 Flash..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"repo_url": repo_url},
                    timeout=600,
                )
                if response.status_code != 200:
                    st.error(f"Backend error: {response.text}")
                else:
                    result = response.json()
                    docs_path = result.get("docs_path")
                    if docs_path and os.path.exists(docs_path):
                        st.success("Documentation generated successfully!")
                        st.session_state.docs_path = docs_path
                        st.session_state.repo_name = (
                            Path(docs_path).stem.replace("_docs", "")
                        )
                    else:
                        st.warning(
                            "Backend did not return a valid documentation path."
                        )
            except Exception as e:
                st.error(f"Request failed: {e}")

# DISPLAY GENERATED DOCS
if "docs_path" in st.session_state:
    st.divider()
    col1, col2 = st.columns([1, 3])
    with col1:
        st.download_button(
            label="⬇️ Download Markdown",
            data=Path(st.session_state.docs_path).read_text(
                encoding="utf-8"
            ),
            file_name=f"{st.session_state.repo_name}_docs.md",
            mime="text/markdown",
        )
    with col2:
        st.markdown(f"**Repository:** `{st.session_state.repo_name}`")

    st.divider()
    docs_viewer(st.session_state.docs_path)

# OPTIONAL CHAT / Q&A SECTION
st.divider()
st.markdown("### Ask Questions About the Codebase")
chat_interface()
