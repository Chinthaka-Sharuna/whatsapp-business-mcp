from sqlmodel import SQLModel, Field
from datetime import datetime
from sqlalchemy import Column, DateTime, func

from uuid import UUID,uuid4

class Users(SQLModel, table=True):
    __tablename__ = "users"
    user_id : UUID = Field(default_factory=uuid4, primary_key=True)
    name : str = Field(min_length=5, max_length=50, index=True, nullable=False)
    password : str = Field(max_length=100, min_length=8, nullable=False)
    created_at : datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            default=func.now(),
            nullable=False
        )
    )
    is_active : bool = Field(default=True)
    is_admin : bool = Field(default=False)
    last_login_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True))
    )
    wapn_id : str = Field(foreign_key="phone_numbers.wapn_id",nullable=False)
    