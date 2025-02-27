from typing import Any, Literal
from uuid import uuid4

from exceptios import GameNotFoundError

try:
    from base_db import DbManager
    from schema import OptionalGameInfo, GameInfo
except ModuleNotFoundError:
    from model.base_db import DbManager
    from model.schema import OptionalGameInfo, GameInfo


class GameDBManager(DbManager):
    def __init__(self) -> None:
        super().__init__("demo.db")
        self.create_table(
            "gameInfo",
            id="TEXT PRIMARY KEY",
            rate="INTEGER NOT NULL DEFAULT 0",
            pot="INTEGER NOT NULL DEFAULT 0",
            isplaying="INTEGER NOT NULL DEFAULT 0"
        )

    def _game_exists(self, game_id: str) -> None:
        if not self.data_checker("gameInfo", f"id = '{game_id}'"):
            raise GameNotFoundError

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

    def insert_game_info(self, game_info: GameInfo) -> str:
        _id = str(uuid4())
        self.insert(
            "gameInfo",
            id=str(_id),
            **self._data_formatter(mode="encode", **game_info.model_dump())
        )
        return _id

    def update_game_info(self, game_id: str, game_info: GameInfo | OptionalGameInfo):
        self._game_exists(game_id)
        data = game_info.model_dump(exclude_unset=True)
        self.update(
            "gameInfo", f"id = '{game_id}'", **self._data_formatter(mode="encode", **data)
        )

    def get_game_info(self, game_id: str) -> GameInfo:
        self._game_exists(game_id)
        data = self.select("gameInfo", ["rate", "pot", "isplaying"], f"id = '{game_id}'")
        return GameInfo(**self._data_formatter(mode="decode", **data[0]))
    
    def delete_game_info(self, game_id: str) -> None:
        self.delete("gameInfo", f"id = '{game_id}'")


if __name__ == "__main__":
    game_manager = GameDBManager()