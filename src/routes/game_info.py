from typing import Any, Mapping

from flask import Blueprint, Response
from flask_restful import Api
from pydantic_core import ValidationError

from exceptios import GameNotFoundError
from routes.base_resource import BaseResource
from model.game_info import GameDBManager
from model.schema import GameInfo, OptionalGameInfo


app = Blueprint("game_info", __name__)
api = Api(app)

# GameInfoリソース
class GameInfoResource(BaseResource):
    def __init__(self) -> None:
        super().__init__()
        self.db = GameDBManager()

    def _request_formatter(
        self, data: Mapping[str, Any]) -> GameInfo:
        try:
            game =  GameInfo(**data)
        except ValidationError as e:
            self.error_response(400, f"Invalid request data: {e}")
        return game

    def get(self, game_id: str) -> Response:
        try:
            game = self.db.get_game_info(game_id)
        except GameNotFoundError:
            self.error_response(404, "Game not found")
        return self.success_response(200, data=game.model_dump())
    
    def post(self) -> Response:
        data = self._request_formatter(data=self.request_loader())
        _id = self.db.insert_game_info(data)
        return self.success_response(201, data={"id": _id})
    
    def put(self, game_id: str) -> Response:
        data = self._request_formatter(data=self.request_loader())
        self.db.update_game_info(game_id, data)
        return self.success_response(204)
    
    def delete(self, game_id: str) -> Response:
        self.db.delete_game_info(game_id)
        return self.success_response(204)




api.add_resource(
    GameInfoResource,
    "/game_info",
    "/game_info/<string:game_id>"
)
