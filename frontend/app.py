import streamlit as st
import requests
import time
from urllib.parse import urlparse

def is_valid_url(url):

    try:

        parsed = urlparse(url)

        return all([
            parsed.scheme in ["http", "https"],
            parsed.netloc
        ])

    except:

        return False
    
st.set_page_config(
    page_title="AskDocs AI",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# Session State
# -----------------------------
if "docs_loaded" not in st.session_state:
    st.session_state.docs_loaded = False

if "current_docs" not in st.session_state:
    st.session_state.current_docs = ""


# -----------------------------
# Header
# -----------------------------
st.title("🤖 AskDocs AI")

st.markdown(
    """
Chat with any documentation website using AI.

Upload a docs website → ask technical questions.
"""
)

st.divider()


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.header("Documentation Setup")

    docs_url = st.text_input(
        "Documentation URL",
        placeholder="Enter a URL"
    )

    process_button = st.button(
        "Process Documentation",
        use_container_width=True
    )

    st.divider()

    if st.session_state.docs_loaded:

        st.success("Documentation Ready")

        st.caption(
            f"Current Docs: {st.session_state.current_docs}"
        )


# -----------------------------
# Process Documentation
# -----------------------------
if process_button:

    if not docs_url:

        st.sidebar.error(
            "Please enter a documentation URL"
        )

    elif not is_valid_url(docs_url):

        st.sidebar.error(
            "Please enter a valid URL starting with http:// or https://"
        )

    else:

        progress_bar = st.progress(0)

        status = st.empty()

        try:

            # Step 1
            status.info(
                "🔍 Validating documentation URL..."
            )

            progress_bar.progress(10)

            time.sleep(0.5)

            # Step 2
            status.info(
                "📚 Reading documentation pages..."
            )

            progress_bar.progress(35)

            time.sleep(0.5)

            # Step 3
            status.info(
                "🧠 Understanding documentation structure..."
            )

            progress_bar.progress(65)

            response = requests.post(
                "http://127.0.0.1:8002/process-docs",
                json={"url": docs_url}
            )

            data = response.json()

            # Step 4
            status.info(
                "⚡ Preparing AI search system..."
            )

            progress_bar.progress(90)

            time.sleep(0.5)

            if data["status"] == "success":

                progress_bar.progress(100)

                status.success(
                    "✅ Documentation processed successfully"
                )

                st.session_state.docs_loaded = True

                st.session_state.current_docs = docs_url

                st.toast(
                    "🚀 AskDocs AI is ready!"
                )

            else:

                st.error(data["message"])

        except Exception as e:

            st.error(str(e))


# -----------------------------
# Chat Interface
# -----------------------------
st.subheader("Ask Questions")

query = st.text_input(
    "Ask anything about the documentation...",
    placeholder="Enter a question"
)


if st.button(
    "Ask",
    use_container_width=True
):

    if not st.session_state.docs_loaded:

        st.warning(
            "Please process documentation first"
        )

    elif not query:

        st.warning(
            "Please enter a question"
        )

    else:

        thinking = st.empty()

        try:

            # Simulated thinking states
            thinking.info(
                "🔎 Searching relevant documentation..."
            )

            time.sleep(0.5)

            thinking.info(
                "🧠 Understanding retrieved context..."
            )

            time.sleep(0.5)

            thinking.info(
                "✍️ Generating grounded answer..."
            )

            response = requests.post(
                "http://127.0.0.1:8002/ask",
                json={"query": query}
            )

            data = response.json()

            thinking.empty()

            if "answer" in data:

                st.subheader("Answer")

                st.markdown(data["answer"])

            else:

                st.error(data)

        except Exception as e:

            thinking.empty()

            st.error(str(e))