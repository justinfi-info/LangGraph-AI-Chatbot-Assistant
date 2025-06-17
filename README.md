LangGraph AI Chatbot Assistant

A customizable, real-time AI assistant built with LangGraph, OpenAI/Groq, and Streamlit. This project provides a modern chatbot interface featuring token-by-token streaming, chat-style layout with avatars, safe rich-text rendering, and multi-model support.

🚀 Features

🔋 Real-time streaming ChatGPT-style token output

🤖 Support for OpenAI and Groq model providers

🫠 Built with LangGraph agents + tools (e.g., Tavily search)

🖊️ Chat-style UI with user and AI avatars

🌚 Light/Dark theme toggle

🔒 Secure HTML rendering for AI output (links, code, etc.)


🧱 Tech Stack

Layer

Tooling

Frontend

Streamlit

Backend

FastAPI

LLMs

LangGraph, LangChain, OpenAI, Groq

Tools

Tavily Web Search (optional)


🚀 Setup Instructions

1. Clone the Repo

git clone https://github.com/your-username/langgraph-chatbot.git
cd langgraph-chatbot

2. Install Dependencies

pip install -r requirements.txt

3. Set Environment Variables

Create a .env file or set them manually:

OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key

4. Run the Backend

uvicorn backend:app --reload --port 9999

5. Run the Frontend

streamlit run frontend.py

🔹 Usage

Define your AI agent behavior using a System Prompt

Choose a model provider (OpenAI or Groq)

Toggle search tools (optional)

Ask any question and receive a streaming response from your AI agent

📘️ Screenshots

Chat View

Light/Dark Toggle


🌐 License

MIT — Free to use, modify, and distribute.
