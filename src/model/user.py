from typing import Any, Literal, TypedDict


Role = Literal["DB", "SB", "BB"] 

class UserInfo(TypedDict):
    name: str
    chip: int
    role: Role | None
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

def add_user(user: UserInfo) -> None:
    user_info.append(user)

def update_user(user_id: int, **kwargs: Any) -> None:
    for key, val in kwargs.items():
        if val == None:
            continue
        user_info[user_id][key] = val

if __name__ == "__main__":
    update_user(1, name="gorira")
    print(user_info)
