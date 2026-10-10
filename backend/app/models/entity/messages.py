from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Column, DateTime, Index, func, Enum as SAEnum
from sqlmodel import SQLModel, Field

from models.common.enum import MessageDirection, MessageStatus, MessageType


class Messages(SQLModel, table=True):
    __tablename__ = "messages"
    __table_args__ = (
        Index("idx_messages_conv_created", "conversation_id", "created_at"),
        Index("idx_messages_messaged_by", "messaged_by"),
        CheckConstraint(
            "(direction = 'IN') = (messaged_by IS NULL)",
            name="ck_messages_author",
        ),
    )

    message_id: UUID = Field(default_factory=uuid4, primary_key=True)
    wa_message_id: str | None = Field(default=None, max_length=128, unique=True)
    conversation_id: UUID = Field(
        foreign_key="conversations.conversation_id", nullable=False
    )

    timestamp: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    message_type: MessageType = Field(
        sa_column=Column(
            SAEnum(
                MessageType,native_enum=False,length=20
            ),
            nullable=False
        )
    )
    message: str | None = Field(default=None)
    direction: MessageDirection = Field(
        default=MessageDirection.OUT,
        sa_column=Column(
            SAEnum(
                MessageDirection, native_enum=False, length=10
            ), 
            nullable=False
        ),
    )
    status: MessageStatus = Field(
        default=MessageStatus.PENDING,
        sa_column=Column(
            SAEnum(
                MessageStatus, native_enum=False, length=20
            ), 
            nullable=False),
    )
    viewed_by: UUID | None = Field(default=None, foreign_key="users.user_id")
    viewed_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    messaged_by: UUID | None = Field(default=None, foreign_key="users.user_id")
    reply_msg_id: UUID | None = Field(default=None, foreign_key="messages.message_id")