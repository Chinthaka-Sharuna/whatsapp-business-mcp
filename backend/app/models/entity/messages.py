from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column, DateTime, Index, func
from sqlmodel import SQLModel, Field

from app.models.enum import MessageDirection,MessageStatus


class Message(SQLModel, table=True):
    __tablename__ = "messages"
    __table_args__ = (
        Index("idx_messages_conversation", "conversation_id"),
        Index("idx_messages_messaged_by", "messaged_by"),
        Index("idx_messages_viewed_by", "viewed_by"),
        Index("idx_messages_timestamp", "timestamp"),
        Index("idx_messages_status", "status"),
    )

    message_id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.conversation_id", nullable=False)
    timestamp: datetime = Field(
            sa_column=Column(
                DateTime(timezone=True),
                default=func.now(),
                nullable=False
            ),
            index=True
        )
    message_type: str = Field(nullable=False)
    message: str | None = Field(default=None)
    direction: MessageDirection = Field(nullable=False)
    status: MessageStatus = Field(default=MessageStatus.SENT, nullable=False,index=True)
    viewed_by: UUID | None = Field(default=None, foreign_key="users.user_id")
    viewed_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), 
            nullable=True
        ),
        index=True
    )
    messaged_by: UUID | None = Field(default=None, foreign_key="users.user_id")
    reply_msg_id: UUID | None = Field(default=None, foreign_key="messages.message_id")