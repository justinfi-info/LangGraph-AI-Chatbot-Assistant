from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from ai_agent import get_response_from_ai_agent

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

ALLOWED_MODEL_NAMES = [
    "llama3-70b-8192",
    "deepseek-r1-distill-llama-70b",
    "llama-3.3-70b-versatile",
    "mistral-saba-24b",
    "gpt-4o-mini"
]

app = FastAPI(title="LangGraph AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    API Endpoint to interact with the Chatbot using LangGraph and search tools.
    It dynamically selects the model specified in the request.
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        raise HTTPException(status_code=400, detail="Invalid model name. Kindly select a valid AI model.")

    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages list cannot be empty.")

    llm_id = request.model_name
    query = request.messages[-1]
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider

    try:
        response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="127.0.0.1", port=8501, reload=True)