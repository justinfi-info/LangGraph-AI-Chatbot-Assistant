import streamlit as st
from streamlit.components.v1 import html
import markdown
import bleach
import requests

# ───────────────────────────────────────────────
# Page Setup
# ───────────────────────────────────────────────
st.set_page_config(page_title="LangGraph AI Agent", layout="centered")
st.title("🤖 LangGraph AI Assistant")
st.caption("Chat with your AI agent and receive clean, styled responses.")

# ───────────────────────────────────────────────
# Theme Toggle
# ───────────────────────────────────────────────
theme = st.radio("Choose Theme:", ["Dark", "Light"], horizontal=True)

# ───────────────────────────────────────────────
# Markdown → Sanitized HTML Renderer
# ───────────────────────────────────────────────
def markdown_to_html(md_text: str) -> str:
    raw_html = markdown.markdown(md_text, extensions=["fenced_code", "codehilite"])
    
    allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS) + [
        "p", "pre", "h1", "h2", "h3", "ul", "ol", "li", "strong", "em",
        "code", "blockquote", "br", "a", "img"
    ]
    allowed_attrs = {
        "a": ["href", "title"],
        "img": ["src", "alt", "title"]
    }
    allowed_protocols = ["http", "https", "mailto"]

    safe_html = bleach.clean(
        raw_html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        protocols=allowed_protocols,
        strip=True
    )
    return bleach.linkify(safe_html, skip_tags=["pre", "code"])

def render_rich_html(md_text: str, theme: str, height=500):
    content = markdown_to_html(md_text)

    css_dark = """
    body {
        font-family: 'Segoe UI', sans-serif;
        color: #f1f1f1;
        background-color: #0e1117;
        line-height: 1.6;
    }
    h1, h2 { color: #58a6ff; }
    code {
        background-color: #2b2b2b;
        padding: 2px 5px;
        border-radius: 4px;
        font-size: 0.95em;
        color: #ff7b72;
    }
    ul { padding-left: 20px; }
    a { color: #84d4ff; text-decoration: none; }
    img { max-width: 100%; height: auto; }
    """

    css_light = """
    body {
        font-family: 'Segoe UI', sans-serif;
        color: #222;
        background-color: #ffffff;
        line-height: 1.6;
    }
    h1, h2 { color: #195de6; }
    code {
        background-color: #f0f0f0;
        padding: 2px 5px;
        border-radius: 4px;
        font-size: 0.95em;
        color: #d6336c;
    }
    ul { padding-left: 20px; }
    a { color: #195de6; text-decoration: none; }
    img { max-width: 100%; height: auto; }
    """

    styled = f"<style>{css_dark if theme == 'Dark' else css_light}</style><body>{content}</body>"
    html(styled, height=height, scrolling=True)

# ───────────────────────────────────────────────
# Model Setup
# ───────────────────────────────────────────────
system_prompt = st.text_area("Define your AI Agent:", height=70, placeholder="Type your system prompt here...")
system_prompt = system_prompt or "You are a helpful assistant."

MODEL_NAME_GROQ = ["deepseek-r1-distill-llama-70b", "llama-3.3-70b-versatile", "mistral-saba-24b"]
MODEL_NAME_OPENAI = ["gpt-4o-mini"]

provider = st.radio("Select Provider:", ("Groq", "OpenAI"))
selected_model = st.selectbox(
    "Select Model:",
    MODEL_NAME_GROQ if provider == "Groq" else MODEL_NAME_OPENAI
)

allow_web_search = st.checkbox("Allow Web Search")
user_query = st.text_area("Enter your Query:", height=150, placeholder="Ask Anything!")

API_URL = "http://127.0.0.1:9999/chat"  # Update this if backend is running on another port

# ───────────────────────────────────────────────
# Ask Agent Button
# ───────────────────────────────────────────────
if st.button("Ask Agent!"):
    if user_query.strip():
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": bool(allow_web_search)
        }

        try:
            with st.spinner("Thinking..."):
                response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                if "error" in response_data:
                    st.error(response_data["error"])
                else:
                    st.subheader("🧠 Agent Response")
                    response_text = response_data.get("response", "No response received.")
                    render_rich_html(response_text, theme=theme)
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")
    else:
        st.warning("Please enter a query before asking the agent.")