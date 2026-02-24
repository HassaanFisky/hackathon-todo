"""
routes/chat.py — Chat endpoint using Gemini agent with function calling.
Stateless: all conversation state is persisted in the Neon DB.
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from db import engine
from auth import get_current_user_id
from models import Conversation, Message
from gemini_agent import chat_with_gemini

router = APIRouter(prefix="/api", tags=["chat"])


def get_session():
    with Session(engine) as session:
        yield session


class ChatRequest(BaseModel):
    conversation_id: int | None = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: list


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    POST /api/{user_id}/chat
    Accepts a user message, runs it through the Gemini agent,
    persists both the user message and assistant response in DB,
    and returns the AI response along with the conversation_id.
    """
    # Auth guard: JWT user must match path user_id
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # ------------------------------------------------------------------ #
    # Get or create Conversation
    # ------------------------------------------------------------------ #
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # ------------------------------------------------------------------ #
    # Load previous messages from DB (stateless — no in-memory state)
    # ------------------------------------------------------------------ #
    stmt = (
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
    )
    db_messages = session.exec(stmt).all()
    history = [{"role": m.role, "content": m.content} for m in db_messages]

    # ------------------------------------------------------------------ #
    # Persist incoming user message
    # ------------------------------------------------------------------ #
    user_msg = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=request.message,
    )
    session.add(user_msg)
    session.commit()

    # ------------------------------------------------------------------ #
    # Call Gemini agent
    # ------------------------------------------------------------------ #
    try:
        response_text, tool_calls = await chat_with_gemini(
            user_id, request.message, history
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI error: {exc}")

    # ------------------------------------------------------------------ #
    # Persist assistant response
    # ------------------------------------------------------------------ #
    assistant_msg = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="assistant",
        content=response_text,
    )
    session.add(assistant_msg)
    session.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        response=response_text,
        tool_calls=tool_calls,
    )
