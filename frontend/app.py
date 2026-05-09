import streamlit as st
import requests
import time

from urllib.parse import urlparse


# ------------------------------------------------
# Backend URL
# ------------------------------------------------
BACKEND_URL = "https://askdocs-ai-production.up.railway.app"


# ------------------------------------------------
# URL Validation
# ------------------------------------------------
def is_valid_url(url):

    try:

        parsed = urlparse(url)

        return all([
            parsed.scheme in ["http", "https"],
            parsed.netloc
        ])

    except:

        return False


# ------------------------------------------------
# Page Config
# ------------------------------------------------
st.set_page_config(
    page_title="AskDocs AI",
    page_icon="🤖",
    layout="wide"
)


# ------------------------------------------------
# Session State
# ------------------------------------------------
if "docs_loaded" not in st.session_state:
    st.session_state.docs_loaded = False

if "current_docs" not in st.session_state:
    st.session_state.current_docs = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ------------------------------------------------
# Header
# ------------------------------------------------
st.title("🤖 AskDocs AI")

st.markdown(
    """
Chat with any documentation website using AI.

Upload a documentation website and ask technical questions in natural language.
"""
)

st.divider()


# ------------------------------------------------
# Sidebar
# ------------------------------------------------
with st.sidebar:

    st.header("Documentation Setup")

    docs_url = st.text_input(
        "Documentation URL",
        placeholder="Enter docs URL"
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

        if st.button(
            "Clear Chat History",
            use_container_width=True
        ):

            st.session_state.chat_history = []

            st.toast("🗑️ Chat history cleared")


# ------------------------------------------------
# Process Documentation
# ------------------------------------------------
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
                "🔍 Checking documentation website..."
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
                f"{BACKEND_URL}/process-docs",
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

                st.session_state.chat_history = []

                st.toast(
                    "🚀 AskDocs AI is ready!"
                )

            else:

                st.error(data["message"])

        except Exception as e:

            st.error(str(e))


# ------------------------------------------------
# Chat Section
# ------------------------------------------------
st.subheader("Ask Questions")


# ------------------------------------------------
# Display Previous Chats
# ------------------------------------------------
for chat in st.session_state.chat_history:

    with st.chat_message("user"):

        st.markdown(chat["question"])

    with st.chat_message("assistant"):

        st.markdown(chat["answer"])


# ------------------------------------------------
# Chat Input
# ------------------------------------------------
query = st.chat_input(
    "Ask a documentation question..."
)


# ------------------------------------------------
# Handle Query
# ------------------------------------------------
if query:

    if not st.session_state.docs_loaded:

        st.warning(
            "Please process documentation first"
        )

    else:

        # Show User Message
        with st.chat_message("user"):

            st.markdown(query)

        thinking = st.empty()

        try:

            # Thinking states
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
                f"{BACKEND_URL}/ask",
                json={
                    "query": query,
                    "chat_history": st.session_state.chat_history[-3:]
                }
            )

            data = response.json()

            thinking.empty()

            if "answer" in data:

                answer = data["answer"]

                # Show Assistant Message
                with st.chat_message("assistant"):

                    st.markdown(answer)

                # Save Chat History
                st.session_state.chat_history.append(
                    {
                        "question": query,
                        "answer": answer
                    }
                )

            else:

                st.error(data)

        except Exception as e:

            thinking.empty()

            st.error(str(e))