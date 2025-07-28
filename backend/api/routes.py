# backend/api/routes.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from agents.orchestrator import build_agents_client, create_orchestrator
from azure.ai.agents.models import MessageRole, ListSortOrder
from auth import verify_token
from thread_store import load_threads, save_threads

router = APIRouter()

client = build_agents_client()
orchestrator = create_orchestrator(client)

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat_endpoint(request: ChatRequest, payload=Depends(verify_token)):
    user_id = payload["sub"]
    user_input = request.message.strip()

    # Load or create thread ID for the user
    threads = load_threads()

    if user_id not in threads:
        thread = client.threads.create()
        threads[user_id] = thread.id
        save_threads(threads)

    thread_id = threads[user_id]


    # Add message and run
    client.messages.create(
        thread_id=thread_id,
        role=MessageRole.USER,
        content=user_input
    )

    client.runs.create_and_process(
        thread_id=thread_id,
        agent_id=orchestrator.id
    )

    # Fetch response
    messages = list(client.messages.list(thread_id=thread_id, order=ListSortOrder.DESCENDING))
    for msg in messages:
        if msg.role == MessageRole.AGENT and msg.text_messages:
            reply = msg.text_messages[-1].text.value.strip()
            return {"reply": reply}

    return {"reply": "Sorry, I couldn't generate a response."}


@router.get("/messages")
def get_messages(payload=Depends(verify_token)):
    user_id = payload["sub"]
    threads = load_threads()

    if user_id not in threads:
        return {"messages": []}

    thread_id = threads[user_id]
    all_msgs = client.messages.list(thread_id=thread_id, order=ListSortOrder.ASCENDING)

    result = []
    for msg in all_msgs:
        if msg.text_messages:
            content = msg.text_messages[-1].text.value.strip()
            role = msg.role.title()
            result.append({"role": role, "text": content})

    return {"messages": result}

