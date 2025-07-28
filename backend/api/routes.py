# backend/api/routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from agents.orchestrator import build_agents_client, create_orchestrator
from azure.ai.agents.models import MessageRole, ListSortOrder
from fastapi import Depends
from auth import verify_token


router = APIRouter()

# Track orchestrator and thread across calls (for now)
client = build_agents_client()
orchestrator = create_orchestrator(client)
thread = client.threads.create()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat_endpoint(request: ChatRequest, payload=Depends(verify_token)):
    user_id = payload["sub"]
    print(user_id)
    user_input = request.message.strip()

    client.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=user_input
    )

    client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=orchestrator.id
    )

    messages = list(client.messages.list(thread_id=thread.id, order=ListSortOrder.DESCENDING))
    for msg in messages:
        if msg.role == MessageRole.AGENT and msg.text_messages:
            reply = msg.text_messages[-1].text.value.strip()
            return {"reply": reply}

    return {"reply": "Sorry, I couldn't generate a response."}
