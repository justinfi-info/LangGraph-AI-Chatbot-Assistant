# Step 1: Setup API Keys for Groq, OpenAI and Tavily
import os

# Step 2: Setup LLM & Tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

# Step 3: Setup AI Agent with Search tool functionality
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Load API keys
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Optional static instances (not used here)
# openai_llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini")
# groq_llm = ChatGroq(api_key=GROQ_API_KEY, model="llama-3.3-70b-versatile")

# AI Agent handler
def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):

    # Choose model
    if provider == "Groq":
        llm = ChatGroq(api_key=GROQ_API_KEY, model=llm_id)
    elif provider == "OpenAI":
        llm = ChatOpenAI(api_key=OPENAI_API_KEY, model=llm_id)
    else:
        raise ValueError("Unknown provider")

    # Optionally include Tavily search tool
    tools = [TavilySearch(api_key=TAVILY_API_KEY, max_results=2)] if allow_search else []

    # Build the agent
    agent = create_react_agent(
        model=llm,
        tools=tools
    )

    # Message list for agent context
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ]

    # Correct state input
    state = {"messages": messages}

    # Run the agent
    response = agent.invoke(state)

    # Extract final AI message content
    ai_messages = [message.content for message in response.get("messages", []) if isinstance(message, AIMessage)]
    return ai_messages[-1] if ai_messages else "No AI response found."
