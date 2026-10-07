from typing import Annotated
from pydantic import Field,StringConstraints


Username = Annotated[str,Field(min_length=5,max_length=50)]
Email = Annotated[str, Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')]
PhoneNumber = Annotated[str,StringConstraints(strip_whitespace=True,min_length=10,max_length=15,pattern=r"^\+?[0-9]+$"),Field(description="Phone number with optional country code")]