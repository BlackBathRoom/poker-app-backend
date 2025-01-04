from typing import Any, Literal
from uuid import uuid4

from exceptios import UserNotFoundError
from model.base_db import DbManager
from schema import UserInfo


class UserDBManager(DbManager):
    def __init__(self) -> None:
        super().__init__("demo.db")
        self.create_table(
            "users",
            "id",
            not_null=["name", "chip", "isplaying"],
            id="TEXT",
            name="TEXT",
            chip="INTEGER",
            role="TEXT",
            isplaying="INTEGER",
        )

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
    
    def data_checker(self, user_id: str) -> None:
        if not super().data_checker("users", f"id = '{user_id}'"):
            raise UserNotFoundError

    def user_list(self) -> list[UserInfo]:
        data = self.select("users", ["name", "chip", "role", "isplaying"])
        users = [
            self._data_formatter(mode="decode", **row)
            for row in data
        ]
        return users
    
    def user_by_id(self, user_id: str) -> UserInfo:
        data = self.select("users", ["name", "chip", "role", "isplaying"], f"id = '{user_id}'")
        if not data:
            raise UserNotFoundError
        user = self._data_formatter(mode="decode", **data[0])
        return user

    def add_user(self, user: UserInfo) -> str:
        _id = str(uuid4())
        data = self._data_formatter(mode="encode", **user)
        self.insert(
            "users",
            id=_id,
            **data
        )
        return _id

    def update_user(self, user_id: str, **kwargs: Any) -> None:
        self.data_checker(user_id)
        data = self._data_formatter(mode="encode", **kwargs)
        self.update("users", f"id = '{user_id}'", **data)

    def delete_user(self, user_id: str) -> None:
        self.data_checker(user_id)
        self.delete("users", f"id = '{user_id}'")


if __name__ == "__main__":
    user_db = UserDBManager()
    print(user_db.user_list())
