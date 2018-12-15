from flask import Flask
from flask_bcrypt  import Bcrypt
import os
from routes.user import user_routes
from routes.user import admin_routes
from routes.post import post_routes
from routes.tag import tag_routes
from routes.vote import vote_routes
from routes.report import report_routes
import psycopg2 as dbap2


def create_app():
    app = Flask(__name__)
    app.config["bcrypt"] = Bcrypt(app)    
    app.register_blueprint(post_routes.post_pages)
    app.register_blueprint(admin_routes.admin_user_page)
    app.register_blueprint(tag_routes.tag_pages)
    app.register_blueprint(vote_routes.vote_page)
    app.register_blueprint(report_routes.report_page)
    app.register_blueprint(user_routes.user_page)



    app.config['DB_URL'] = os.getenv('DATABASE_URL')  

    app.config['SECRET_KEY'] = 'AccioSecretKey'
    app.config['WTF_CSRF_SECRET_KEY'] = 'AccioCSRFSecretKey'
     
    return app


if __name__ == "__main__":
    app = create_app()
    app.config['SESSION_TYPE']= 'filesystem'
    app.run(host="0.0.0.0", port=8080, debug=True)