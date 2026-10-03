from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.conversation import Conversation
from app.models.message import Message


router = APIRouter(
    prefix="/api/conversations",
    tags=["Conversations"]
)


@router.get("")
def conversations(
    db: Session = Depends(get_db)
):

    return db.query(
        Conversation
    ).all()


@router.get("/{conversation_id}")
def conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):

    messages = db.query(
        Message
    ).filter(
        Message.conversation_id ==
        conversation_id
    ).order_by(
        Message.created_at
    ).all()

    return messages