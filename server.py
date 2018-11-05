from flask import Flask

from routes.user import login
from routes.user import logout
from routes.user import register
from models import db

def create_app():
    app = Flask(__name__)

    app.add_url_rule("/user/login", view_func=login.login)
    app.add_url_rule("/user/logout",view_func=logout.logout)
    app.add_url_rule("/user/register",view_func=register.register)
    database = db.Database()
    app.config["db"] = database

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)