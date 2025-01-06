from typing import Literal
from pydantic import Field, BaseModel


Role = Literal["DB", "SB", "BB"] 

class UserInfo(BaseModel):
    name: str
    chip: int = Field(ge=0)
    role: Role | None
    isplaying: bool

class OptionalUserInfo(BaseModel):
    name: str | None = Field(default=None)
    chip: int | None = Field(default=None, ge=0)
    role: Role | None = Field(default=None)
    isplaying: bool | None = Field(default=None)

