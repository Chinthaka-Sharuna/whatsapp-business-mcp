from datetime import datetime
from sqlmodel import DateTime, SQLModel, Field
from sqlalchemy import Column
from uuid import UUID

class MessageStatus(SQLModel, table=True):
    __tablename__ = "message_status"

    message_id: UUID = Field(foreign_key="messages.message_id", primary_key=True)
    delivered_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    read_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))