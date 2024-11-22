from pydantic import BaseModel,EmailStr
from typing import Optional

class AuthResponseDetails(BaseModel):
    message : str

class TermResponse(BaseModel):
    term: str
    definition: str



