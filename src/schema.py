from typing import Literal
from pydantic import BaseModel


Role = Literal["DB", "SB", "BB"] 

class UserInfo(BaseModel):
    name: str
    chip: int
    role: Role | None
    isplaying: bool
