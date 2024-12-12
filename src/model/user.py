from typing import Literal,TypedDict


class UserInfo(TypedDict):
    name: str
    chip: int
    role: Literal["DB", "SB", "BB"] | None
    isPlaying: bool

# dammy data
user_info: list[UserInfo] = [
    {
        "name": "hogehoge",
        "chip": 200,
        "role": None,
        "isPlaying": True,
    },
    {
        "name": "fugafuga",
        "chip": 100,
        "role": "DB",
        "isPlaying": False,
    },
    {
        "name": "piyopiyo",
        "chip": 200,
        "role": None,
        "isPlaying": False,
    },
]

def user_list() -> list[UserInfo]:
    return user_info

def user_by_id(user_id: int) -> UserInfo:
    return user_info[user_id]

if __name__ == "__main__":
    pass
