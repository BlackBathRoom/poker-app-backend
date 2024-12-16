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

class UserDBManager:
    def __init__(self) -> None:
        self.user_info = user_info

    def user_list(self) -> list[UserInfo]:
        return self.user_info
    
    def user_by_id(self, user_id: int) -> UserInfo:
        return self.user_info[user_id]
    
    def add_user(self, user: UserInfo) -> None:
        self.user_info.append(user)
    
    def update_name(self, user_id: int, name: str) -> None:
        self.user_info[user_id]["name"] = name

    def update_chip(self, user_id: int, chip: int) -> None:
        self.user_info[user_id]["chip"] = chip

    def update_role(self, user_id: int, role: Role) -> None:
        self.user_info[user_id]["role"] = role

    def update_isPlaying(self, user_id: int, isPlaying: bool) -> None:
        self.user_info[user_id]["isPlaying"] = isPlaying

    def delete_user(self, user_id: int) -> None:
        self.user_info.pop(user_id)


if __name__ == "__main__":
    print(user_info)
