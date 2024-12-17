from typing import Any

from flask import  json, jsonify, request, Blueprint, Response
from flask_restful import Resource, Api

from model.user import UserDBManager, UserInfo


app = Blueprint("users", __name__)
api = Api(app)

class UserResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db = UserDBManager()

    def get(self, user_id: str | None = None) -> Response:
        if user_id:
            return jsonify(self.db.user_by_id(int(user_id)))
        return jsonify(self.db.user_list())

    def post(self) -> Response:
        data = request.data.decode("utf-8")
        data = json.loads(data)

        self.db.add_user(self._request_formatter(data))
        return {"message": "post user"}
    
    def _request_formatter(self, data: Any) -> UserInfo:
        try:
            user = {
                "name": data["name"],
                "chip": int(data["chip"]),
                "role": data["role"] if data["role"] else None
            }
            if data["isPlaying"] == "true"\
                or data["isPlaying"] == "True":
                user["isPlaying"] = True
            else:
                user["isPlaying"] = False
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid request: {e}")
        else:
            return user
    
    def put(self, user_id: str) -> Response:
        data = request.data.decode("utf-8")
        data = json.loads(data)

        if "name" in data:
            self.db.update_name(int(user_id), data["name"])
        if "chip" in data:
            self.db.update_chip(int(user_id), data["chip"])
        if "role" in data:
            self.db.update_role(int(user_id), data["role"])
        if "isPlaying" in data:
            self.db.update_isPlaying(int(user_id), data["isPlaying"])

        return {"message": data}

    def delete(self, user_id: str) -> Response:
        self.db.delete_user(int(user_id))
        return {"message": "delete user"}
    
class UserChipResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db = UserDBManager()
    
    def get(self, user_id: str) -> Response:
        return jsonify(self.db.user_chip(int(user_id)))

    def put(self, user_id: str) -> Response:
        data = request.data.decode("utf-8")
        data = json.loads(data)

        self.db.update_chip(int(user_id), data["chip"])
        return {"message": data}

    
api.add_resource(
    UserResource,
    "/",
    "/<string:user_id>",
)

api.add_resource(
    UserChipResource,
    "/<string:user_id>/chip",
)

if __name__ == "__main__":
    pass
