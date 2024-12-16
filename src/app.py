from flask import Flask

from routes import user


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

app.register_blueprint(user.app, url_prefix="/users")


if __name__ == "__main__":
    app.run(port=8000, debug=True)
