from sqlmodel import SQLModel, Field
from sqlalchemy import Column,Enum as SAEnum

from models.common.enum import PhoneNumberLabels


class PhoneNumbers(SQLModel, table=True):
    __tablename__ = "phone_numbers"

    wapn_id: str = Field(max_length=64, primary_key=True)
    wa_number:str = Field(max_length=32)
    label: PhoneNumberLabels = Field(
        sa_column=Column(
            SAEnum(PhoneNumberLabels, native_enum=False, length=20),
            nullable=False,
        )
    )