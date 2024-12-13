from typing import Any

from flask import  json, jsonify, request, Blueprint, Response
from flask_restful import Resource, Api

from model.user import user_by_id, user_list, add_user, UserInfo


app = Blueprint("user", __name__)
api = Api(app)

class UserResource(Resource):
    def get(self, user_id: str | None = None) -> Response:
        if user_id:
            return jsonify(user_by_id(int(user_id)))
        return jsonify(user_list())
    
    def post(self) -> Response:
        data = request.data.decode("utf-8")
        data = json.loads(data)

        add_user(self._request_formatter(data))
        return {"message": "post user"}
    
    def _request_formatter(self, data: Any) -> UserInfo:
        user = {}
        try:
            user["name"] = data["name"]
            user["chip"] = int(data["chip"])
            user["role"] = data["role"] if data["role"] else None
            if data["isPlaying"] == "true"\
                or data["isPlaying"] == "True":
                user["isPlaying"] = True
            else:
                user["isPlaying"] = False
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid request: {e}")
        return user

    
api.add_resource(
    UserResource,
    "/",
    "/<string:user_id>",
)

if __name__ == "__main__":
    pass
