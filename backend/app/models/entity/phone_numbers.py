from sqlmodel import SQLModel, Field

from models.common.enum import PhoneNumberLables


class PhoneNumbers(SQLModel, table=True):
    __tablename__ = "phone_numbers"

    wapn_id: str = Field(max_length=64, primary_key=True)
    wa_number:str = Field(max_length=32)
    label: PhoneNumberLables = Field(nullable=False)