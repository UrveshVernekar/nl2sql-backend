from fastapi import APIRouter, Depends
from app.auth.deps import (
    get_current_user_id,
    get_current_user
)
from app.db.chats import (
    create_chat,
    list_chats,
    rename_chat,
    delete_chat,
)
from app.db.messages import list_messages


router = APIRouter(prefix="/api/chats", tags=["Chats"])


@router.get("/")
def get_chats(user=Depends(get_current_user)):
    return list_chats(user["id"])


@router.post("/")
def new_chat(user=Depends(get_current_user)):
    chat_id = create_chat(user["id"], "New chat")
    return {"id": chat_id}


@router.patch("/{chat_id}")
def update_chat(chat_id: str, body: dict, user=Depends(get_current_user)):
    rename_chat(chat_id, user["id"], body["title"])
    return {"ok": True}


@router.delete("/{chat_id}")
def remove_chat(chat_id: str, user=Depends(get_current_user)):
    delete_chat(chat_id, user["id"])
    return {"ok": True}


@router.get("/{chat_id}/messages")
def get_messages(chat_id: str, user=Depends(get_current_user)):
    return list_messages(chat_id)