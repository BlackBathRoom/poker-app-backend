from typing import Literal, TypedDict

from flask import Blueprint, jsonify, Response


app = Blueprint("user", __name__)

# dammy data
class UserInfo(TypedDict):
    name: str
    chip: int
    role: Literal["DB", "SB", "BB"] | None
    isPlaying: bool

user_info: list[UserInfo] = [
    {
        "name": "hogehoge",
        "chip": 200,
        "role": None,
        "isPlaying": True,
    },
    {
        "name": "fugafuga",
        "chip": 100,
        "role": "DB",
        "isPlaying": False,
    },
    {
        "name": "piyopiyo",
        "chip": 200,
        "role": None,
        "isPlaying": False,
    },
]

@app.route('/', methods=['GET'])
def get_user_list() -> Response:
    res = {"user": user_info}
    return jsonify(res), 200

@app.route("/<user_id>", methods=["GET"])
def get_user_by_id(user_id: str) -> Response:
    res = {
        "user": [user_info[int(user_id)]]
    }
    return jsonify(res), 200

if __name__ == "__main__":
    pass
