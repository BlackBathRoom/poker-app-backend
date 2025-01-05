from typing import Any, get_type_hints

from flask import request, Blueprint, Response
from flask.json import loads
from flask_restful import Api

from exceptios import UserNotFoundError
from routes.base_resource import BaseResource
from model.user import UserDBManager, UserInfo


app = Blueprint("users", __name__)
api = Api(app)

# Userリソース

class UserResource(BaseResource):
    def __init__(self) -> None:
        super().__init__()
        self.db = UserDBManager()

    def get(self, user_id: str | None = None) -> Response:
        if user_id:
            try:
                user = self.db.user_by_id(user_id)
            except UserNotFoundError:
                self.error_response(404, "User not found")
        else:
            user = self.db.user_list()

        return self.success_response(200, data=user)

    def post(self) -> Response:
        data = loads(request.data.decode("utf-8"))
        try:
            _id = self.db.add_user(self._request_formatter(data))
        except ValueError as e:
            self.error_response(400, f"Missing Keys: {e}")
        except UserNotFoundError:
            self.error_response(400, "User not found")
        
        return self.success_response(201, data={"id": _id})
    
    def _request_formatter(self, data: Any) -> UserInfo:
        try:
            user = {
                "name": data["name"],
                "chip": data["chip"],
                "role": data["role"],
                "isplaying": data["isplaying"],
            }
        except KeyError:
            keys = list(get_type_hints(UserInfo).keys())
            raise ValueError(f"{set(keys) - set(data.keys())}")
        return user
    
    def put(self, user_id: str) -> Response:
        data = loads(request.data.decode("utf-8"))
        try:
            self.db.update_user(user_id, **self._request_formatter(data))
        except UserNotFoundError:
            self.error_response(400, "User not found")
        return self.success_response(204)

    def delete(self, user_id: str) -> Response:
        try:
            self.db.delete_user(user_id)
        except UserNotFoundError:
            self.error_response(404, "User not found")
        return self.success_response(204)


# サブリソース

class UserSubResource(BaseResource):

    sub_resource = list(get_type_hints(UserInfo).keys())

    def __init__(self) -> None:
        super().__init__()
        self.db = UserDBManager()

    def _resource_type_checker(self, resource_type: str) -> bool:
        if resource_type not in self.sub_resource:
            return False
        return True
    
    def get(self, user_id: str, resource_type: str) -> Response:
        if not self._resource_type_checker(resource_type):
            self.error_response(404, "Invalid resource type")
        try:
            user = self.db.user_by_id(user_id)
        except UserNotFoundError:
            self.error_response(404, "User not found")

        return self.success_response(
            code=200,
            data={resource_type: user[resource_type]},
        )

    def put(self, user_id: str, resource_type: str) -> Response:
        if not self._resource_type_checker(resource_type):
            self.error_response(404, "Invalid resource type")
        data = loads(request.data.decode("utf-8"))

        try:
            self.db.update_user(user_id, **{resource_type: data[resource_type]})
        except KeyError:
            self.error_response(400, "Missing Keys")
        return self.success_response(204)
    
    def post(self, user_id: str, resource_type: str) -> Response:
        self.error_response(405, "Method Not Allowed")
        
    def delete(self, user_id: str, resource_type: str) -> Response:
        self.error_response(405, "Method Not Allowed")


# エンドポイントの設定
api.add_resource(
    UserResource,
    "/",
    "/<string:user_id>",
)

api.add_resource(
    UserSubResource,
    "/<string:user_id>/<string:resource_type>",
)


if __name__ == "__main__":
    pass
