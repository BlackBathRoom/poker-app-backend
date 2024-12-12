from flask import Blueprint, jsonify, Response
from flask_restful import Resource, Api

from model.user import user_by_id, user_list


app = Blueprint("user", __name__)
api = Api(app)

class UserResource(Resource):
    def get(self, user_id: str | None = None) -> Response:
        if user_id:
            return jsonify(user_by_id(int(user_id)))
        return jsonify(user_list())
    
api.add_resource(
    UserResource,
    "/",
    "/<string:user_id>"
)

if __name__ == "__main__":
    pass
