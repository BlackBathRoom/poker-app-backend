from json import JSONDecodeError
from typing import Any

from flask import request, Blueprint, Response
from flask.json import jsonify, loads
from flask_restful import Resource, Api

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
            return jsonify(self.db.user_by_id(int(user_id)))
        return jsonify(self.db.user_list())

    def post(self) -> Response:
        data = loads(request.data.decode("utf-8"))
        self.db.add_user(self._request_formatter(data))
        return {"message": "post user"}
    
    def _request_formatter(self, data: Any) -> UserInfo:
        try:
            user = {
                "name": data["name"],
                "chip": int(data["chip"]),
                "role": data["role"] if data["role"] else None,
                "isplaying": data["isplaying"],
            }
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid request: {e}")
        else:
            return user
    
    def put(self, user_id: str) -> Response:
        data = request.data.decode("utf-8")
        data = loads(data)

        self.db.update_user(int(user_id), **data)

        return {"message": data}

    def delete(self, user_id: str) -> Response:
        self.db.delete_user(int(user_id))
        return {"message": "delete user"}


# サブリソース

class UserSubResource(Resource):

    sub_resource = ["name", "chip", "role", "isplaying"]

    def __init__(self) -> None:
        super().__init__()
        self.db = UserDBManager()

    def _resource_type_checker(self, resource_type: str) -> bool:
        if resource_type not in self.sub_resource:
            return False
        return True
    
    def get(self, user_id: str, resource_type: str) -> Response:
        if not self._resource_type_checker(resource_type):
            return {"message": "Invalid resource type"}
        user = self.db.user_by_id(int(user_id))
        return jsonify(user[resource_type])

    def put(self, user_id: str, resource_type: str) -> Response:
        if not self._resource_type_checker(resource_type):
            return {"message": "Invalid resource type"}, 400
        try:
            data = loads(request.data.decode("utf-8"))
            self.db.update_user(int(user_id), **{resource_type: data[resource_type]})
        except JSONDecodeError:
            return {"message": "Invalid JSON format"}, 400
        except KeyError:
            return {"message": "Invalid resource type"}, 400
        else:
            return {"message": f"update user {resource_type}"}, 200


# ルーティングの設定
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
