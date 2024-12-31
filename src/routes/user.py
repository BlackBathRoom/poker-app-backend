from typing import Any, get_type_hints

from flask import request, Blueprint, Response
from flask.json import loads
from flask_restful import abort, output_json, Api, Resource

from exceptios import UserNotFoundError
from response_header import response_header
from model.user import UserDBManager, UserInfo


app = Blueprint("users", __name__)
api = Api(app)

# Userリソース

class UserResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db = UserDBManager()

    def get(self, user_id: str | None = None) -> Response:
        if user_id:
            try:
                user = self.db.user_by_id(user_id)
            except UserNotFoundError:
                return abort(404, status=404, message="User not found")
        else:
            user = self.db.user_list()

        return output_json(
            data=user,
            code=200,
            headers=response_header
        )

    def post(self) -> Response:
        data = loads(request.data.decode("utf-8"))
        try:
            _id = self.db.add_user(self._request_formatter(data))
        except ValueError as e:
            return abort(400, status=400, message=f"Missing Keys: {e}")
        
        return output_json(
            data={"user_id": _id}, # ユーザーIDの返却
            code=201,
            headers=response_header
        )
    
    def _request_formatter(self, data: Any) -> UserInfo:
        try:
            user = {
                "name": data["name"],
                "chip": int(data["chip"]),
                "role": data["role"] if data["role"] else None,
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
            return abort(400, status=400, message="User not found", headers=response_header)
        return {"status": 204}

    def delete(self, user_id: str) -> Response:
        try:
            self.db.delete_user(user_id)
        except UserNotFoundError:
            return abort(400, status=400, message="User not found", headers=response_header)
        return {"status": 204, "headers": response_header}


# サブリソース

class UserSubResource(Resource):

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
            return abort(404, status=404, message="Invalid resource type", headers=response_header)
        try:
            user = self.db.user_by_id(user_id)
        except UserNotFoundError:
            return abort(404, status=404, message="User not found")

        return output_json(
            data={resource_type: user[resource_type]},
            code=200,
            headers=response_header
        )

    def put(self, user_id: str, resource_type: str) -> Response:
        if not self._resource_type_checker(resource_type):
            return abort(404, status=404, message="Invalid resource type")
        data = loads(request.data.decode("utf-8"))

        try:
            self.db.update_user(user_id, **{resource_type: data[resource_type]})
        except KeyError:
            return abort(400, status=400, message="Missing Keys")
        return {"status": 204, "headers": response_header}
    
    def post(self, user_id: str, resource_type: str) -> Response:
        return abort(405, status=405, message="Method Not Allowed", headers=response_header)
        
    def delete(self, user_id: str, resource_type: str) -> Response:
        return abort(405, status=405, message="Method Not Allowed", headers=response_header)


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
