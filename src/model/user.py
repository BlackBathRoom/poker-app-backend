from typing import Any, Literal
from uuid import uuid4

from exceptios import UserNotFoundError

try:
    from base_db import DbManager
    from schema import OptionalUserInfo, UserInfo
except ModuleNotFoundError:
    from model.base_db import DbManager
    from model.schema import OptionalUserInfo, UserInfo


class UserDBManager(DbManager):
    def __init__(self) -> None:
        super().__init__("demo.db")
        self.create_table(
            "users",
            foreign_key={"game_id": "gameInfo(id)"},
            id="TEXT PRIMARY KEY",
            game_id="TEXT NOT NULL",
            name="TEXT NOT NULL",
            chip="INTEGER NOT NULL",
            role="TEXT DEFAULT NULL",
            isplaying="INTEGER NOT NULL",
        )
        self._game_id = "857c9314-f870-4ee5-8306-abac6a322356" # ゲームidによるログイン実装までの仮置き

    def _data_formatter(
        self,
        mode: Literal["encode", "decode"],
        **kwargs: Any
    ) -> dict[str, Any]:
        is_encode = True if mode == "encode" else False
        data = {}
        for key, val in kwargs.items():
            if key == "isplaying":
                val = int(val) if is_encode else bool(val)
            data.setdefault(key, val)
        return data

    def _user_exists(self, user_id: str) -> None:
        if not super().data_checker("users", f"id = '{user_id}'"):
            raise UserNotFoundError

    def user_list(self) -> list[UserInfo]:
        data = self.select("users", ["id", "name", "chip", "role", "isplaying"])
        users = [
            self._data_formatter(mode="decode", **row)
            for row in data
        ]
        return [UserInfo(**user) for user in users]
    
    def user_by_id(self, user_id: str) -> UserInfo:
        data = self.select("users", ["id", "name", "chip", "role", "isplaying"], f"id = '{user_id}'")
        if not data:
            raise UserNotFoundError
        user = self._data_formatter(mode="decode", **data[0])
        return UserInfo(**user)
    
    def user_detail_by_id(self, user_id: str, columns: str | list[str]) -> OptionalUserInfo:
        data = self.select(
            "users",
            columns if isinstance(columns, list) else [columns],
            f"id = '{user_id}'"
        )
        if not data:
            raise UserNotFoundError
        user = self._data_formatter(mode="decode", **data[0])
        return OptionalUserInfo(**user)

    def add_user(self, user: UserInfo) -> str:
        _id = str(uuid4())
        data = self._data_formatter(mode="encode", **user.model_dump())
        self.insert("users", id=_id, game_id=self._game_id, **data)
        return _id

    def update_user(self, user_id: str, user_info: OptionalUserInfo) -> None:
        self._user_exists(user_id)
        data = self._data_formatter(
            mode="encode", **user_info.model_dump(exclude_unset=True)
        )
        self.update("users", f"id = '{user_id}'", **data)

    def delete_user(self, user_id: str) -> None:
        self._user_exists(user_id)
        self.delete("users", f"id = '{user_id}'")


if __name__ == "__main__":
    user_db = UserDBManager()
    
