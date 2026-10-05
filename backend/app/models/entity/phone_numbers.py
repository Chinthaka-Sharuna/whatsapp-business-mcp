from sqlmodel import SQLModel, Field

from app.models.enum import PhoneNumberLables


class PhoneNumber(SQLModel, table=True):
    __tablename__ = "phone_numbers"

    wapn_id: str = Field(max_length=15, primary_key=True)
    wa_number:str = Field(max_length=15)
    label: PhoneNumberLables = Field(nullable=False)