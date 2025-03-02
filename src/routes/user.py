from typing import Any, TypeVar, Union, cast

from flask import Blueprint, Response
from flask_restful import Api
from pydantic_core import ValidationError

from exceptios import UserNotFoundError
from routes.base_resource import BaseResource
from model.user import UserDBManager, UserInfo
from model.schema import OptionalUserInfo


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

        return self.success_response(
            200,
            data=user.model_dump() if isinstance(user, UserInfo) else [u.model_dump() for u in user]
        )

    def post(self) -> Response:
        data = self.request_formatter(
            data=self.request_loader(),
            into=UserInfo
        )
        _id = self.db.add_user(data)
        return self.success_response(201, data={"id": _id})
    
    def put(self, user_id: str) -> Response:
        data = self.request_formatter(
            data=self.request_loader(),
            into=OptionalUserInfo
        )
        try:
            self.db.update_user(user_id, data)
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

    sub_resource = list(UserInfo.__annotations__.keys())

    def __init__(self) -> None:
        super().__init__()
        self.db = UserDBManager()

    def _resource_checker(self, resource_type: str) -> bool:
        if resource_type not in self.sub_resource:
            return False
        return True
    
    def get(self, user_id: str, resource_type: str) -> Response:
        if not self._resource_checker(resource_type):
            self.error_response(404, "Invalid resource type")
        try:
            user = self.db.user_detail_by_id(user_id, resource_type)
        except UserNotFoundError:
            self.error_response(404, "User not found")
        return self.success_response(
            code=200,
            data=user.model_dump(exclude_unset=True)
        )

    def put(self, user_id: str, resource_type: str) -> Response:
        if not self._resource_checker(resource_type):
            self.error_response(404, "Invalid resource type")
        user = self.request_formatter(
            data=self.request_loader(),
            into=OptionalUserInfo
        )
        try:
            self.db.update_user(user_id, user)
        except KeyError:
            self.error_response(400, "Missing Keys")
        return self.success_response(204)


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
