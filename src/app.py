from flask import Flask

from routes import user, game_info



app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

app.register_blueprint(user.app, url_prefix="/users")
app.register_blueprint(game_info.app, url_prefix="/gameinfo")


if __name__ == "__main__":
    app.run(port=8000, debug=True)
