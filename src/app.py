from flask import Flask
from flask_cors import CORS

from routes import user, game_info



app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5000",
                "http://127.0.0.1:5000",
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"],
        }
    },

)

app.register_blueprint(user.app, url_prefix="/users")
app.register_blueprint(game_info.app, url_prefix="/gameinfo")


if __name__ == "__main__":
    app.run(port=8000, debug=True)
