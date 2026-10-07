from pydantic import BaseModel,Field
from typing import Annotated

from models.common.types import PhoneNumber
from models.common.enum import PhoneNumberLables

class PhoneNumberBase(BaseModel):
    wapn_id : Annotated[str,Field(description="")]
    wa_number : Annotated[PhoneNumber,Field(description="")]

class PhoneNumberCreate(PhoneNumberBase):
    label : Annotated[PhoneNumberLables,Field(description="")]

class PhoneNumberAdminResponse(PhoneNumberBase):
    label : Annotated[PhoneNumberLables,Field(description="")]

class PhoneNumberResponse(PhoneNumberBase):
    pass