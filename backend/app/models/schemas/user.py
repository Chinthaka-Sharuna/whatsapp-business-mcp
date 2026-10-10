from pydantic import BaseModel,Field
from typing import Annotated
from datetime import datetime

from models.common.types import Username

class UserBase(BaseModel):
    name : Annotated[Username,Field(description="User's name")]
    is_active : Annotated[bool | None,Field(description="Is user active or not")] = True
    assigned_wapn_id : Annotated[str,Field(description="Whatsapp phone number id which is assiged to user")]

class UserCreate(UserBase):
    is_admin : Annotated[bool | None,Field(description="Is user admin or not")] = False

class UserResponse(UserCreate):
    user_id : Annotated[str,Field(description="User's unique identifier")]
    created_at : Annotated[datetime,Field(description="User's creation timestamp")]
    last_login_at : Annotated[datetime | None,Field(description="User's last login timestamp")] = None
