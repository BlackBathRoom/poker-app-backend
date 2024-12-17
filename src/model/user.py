from typing import Any, Literal, TypedDict


Role = Literal["DB", "SB", "BB"] 

class UserInfo(TypedDict):
    name: str
    chip: int
    role: Role | None
    isplaying: bool

# dammy data
user_info: list[UserInfo] = [
    {
        "name": "hogehoge",
        "chip": 200,
        "role": None,
        "isplaying": True,
    },
    {
        "name": "fugafuga",
        "chip": 100,
        "role": "DB",
        "isplaying": False,
    },
    {
        "name": "piyopiyo",
        "chip": 200,
        "role": None,
        "isplaying": False,
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

    def update_user(self, user_id: int, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if key in self.user_info[user_id]:
                self.user_info[user_id][key] = value
            else:
                raise KeyError(f"Invalid key: {key}")

    def delete_user(self, user_id: int) -> None:
        self.user_info.pop(user_id)


if __name__ == "__main__":
    print(user_info)
