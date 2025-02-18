from typing import Any, Mapping

from flask import Blueprint, Response
from flask_restful import Api
from pydantic_core import ValidationError

from exceptios import GameNotFoundError
from routes.base_resource import BaseResource
from model.game_info import GameDBManager
from model.schema import GameInfo, OptionalGameInfo


app = Blueprint("gameinfo", __name__)
api = Api(app)

# GameInfoリソース
class GameInfoResource(BaseResource):
    def __init__(self) -> None:
        super().__init__()
        self.db = GameDBManager()

    def get(self, game_id: str) -> Response:
        try:
            game = self.db.get_game_info(game_id)
        except GameNotFoundError:
            self.error_response(404, "Game not found")
        return self.success_response(200, data=game.model_dump())
    
    def post(self) -> Response:
        data = self.request_formatter(
            data=self.request_loader(),
            into=GameInfo
        )
        _id = self.db.insert_game_info(data)
        return self.success_response(201, data={"id": _id})
    
    def put(self, game_id: str) -> Response:
        data = self.request_formatter(
            data=self.request_loader(),
            into=OptionalGameInfo
        )
        self.db.update_game_info(game_id, data)
        return self.success_response(204)
    
    def delete(self, game_id: str) -> Response:
        self.db.delete_game_info(game_id)
        return self.success_response(204)


# サブリソース
class GameInfoSubResource(BaseResource):

    sub_resource = list(GameInfo.__annotations__.keys())

    def __init__(self) -> None:
        super().__init__()
        self.db = GameDBManager()

    def get(self, game_id: str, resource_type: str) -> Response:
        if resource_type not in self.sub_resource:
            self.error_response(400, "Invalid resource type")

        game = self.db.get_game_info(game_id)
        resp = {resource_type: game.model_dump()[resource_type]}
        return self.success_response(
            200,
            data=resp
        )
    
    def put(self, game_id: str, resource_type: str) -> Response:
        if resource_type not in self.sub_resource:
            self.error_response(400, "Invalid resource type")
        data = self.request_formatter(
            data=self.request_loader(),
            into=OptionalGameInfo
        )
        self.db.update_game_info(game_id, data)
        return self.success_response(204)


api.add_resource(
    GameInfoResource,
    "/",
    "/<string:game_id>"
)

api.add_resource(
    GameInfoSubResource,
    "/<string:game_id>/<string:resource_type>"
)
