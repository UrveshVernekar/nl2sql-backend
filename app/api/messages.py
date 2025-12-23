from fastapi import APIRouter, Depends
from app.auth.deps import get_current_user_id
from app.db.messages import list_messages
from app.db.chats import list_chats


router = APIRouter(prefix="/api/chats", tags=["Messages"])


@router.get("/{chat_id}/messages")
def get_chat_messages(
    chat_id: str,
    user_id: str = Depends(get_current_user_id),
):
    # (optional) verify chat belongs to user later
    return list_messages(chat_id)