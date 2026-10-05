from sqlmodel import SQLModel,Field
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, func

class Conversations(SQLModel,table = True):
    __tablename__ = "conversations"

    conversation_id: UUID = Field(default_factory=uuid4, primary_key=True)
    customer_wa_user_id: str = Field(nullable=False,index=True)
    customer_wa_id: str = Field(max_length=15,nullable=False,index=True)
    customer_name:str = Field(max_length=25,nullable=False)
    created_at : datetime = Field(
            sa_column=Column(
                DateTime(timezone=True),
                default=func.now(),
                nullable=False
            )
        )
    wapn_id: str = Field(foreign_key="phone_numbers.wapn_id",nullable=False)