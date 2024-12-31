
from typing import Literal, TypedDict


Role = Literal["DB", "SB", "BB"] 

class UserInfo(TypedDict):
    name: str
    chip: int
    role: Role | None
    isplaying: bool
