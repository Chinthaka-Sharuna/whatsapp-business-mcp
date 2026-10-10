from sqlmodel import SQLModel,Field
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import UniqueConstraint, Index

from sqlalchemy import Column, DateTime, func

class Conversations(SQLModel,table = True):
    __tablename__ = "conversations"
    __table_args__ = (
        UniqueConstraint("wapn_id", "customer_wa_id", name="uq_conv_number_customer"),
        Index("idx_conv_inbox", "wapn_id", "last_message_at"),
    )

    conversation_id: UUID = Field(default_factory=uuid4, primary_key=True)
    customer_wa_user_id: str = Field(nullable=False,index=True)
    customer_wa_id: str = Field(max_length=15,nullable=False,index=True)
    customer_name:str = Field(max_length=25,nullable=False)
    last_inbound_at: datetime | None = Field(
        default=None, 
        sa_column=Column(
            DateTime(timezone=True), 
            nullable=True
        )
    )
    last_message_at: datetime | None = Field(
        default=None, 
        sa_column=Column(
            DateTime(timezone=True), 
            nullable=True
        )
    )

    last_handled_by: UUID | None = Field(default=None, foreign_key="users.user_id")
    is_resolved: bool = Field(default=False, nullable=False)

    created_at : datetime = Field(
            sa_column=Column(
                DateTime(timezone=True),
                default=func.now(),
                nullable=False
            )
        )
    wapn_id: str = Field(foreign_key="phone_numbers.wapn_id",nullable=False)