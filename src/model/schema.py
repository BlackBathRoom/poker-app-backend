from operator import is_
from typing import Literal
from pydantic import Field, BaseModel


Role = Literal["DB", "SB", "BB"] 

class UserInfo(BaseModel):
    id: str | None = Field(default=None)
    name: str
    chip: int = Field(ge=0)
    role: Role | None
    isplaying: bool

class OptionalUserInfo(BaseModel):
    id: str | None = Field(default=None)
    name: str | None = Field(default=None)
    chip: int | None = Field(default=None, ge=0)
    role: Role | None = Field(default=None)
    isplaying: bool | None = Field(default=None)

class GameInfo(BaseModel):
    rate: int = Field(ge=0)
    pot: int = Field(ge=0)
    isplaying: bool = False

class OptionalGameInfo(BaseModel):
    rate: int | None = Field(default=None, ge=0)
    pot: int | None = Field(default=None, ge=0)
    isplaying: bool | None = Field(default=None)
