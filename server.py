from flask import Flask
from flask_bcrypt  import Bcrypt
import os
from routes.user import user_routes
import psycopg2 as dbap2


def create_app():
	app = Flask(__name__)
	app.config["bcrypt"] = Bcrypt(app)    
	app.register_blueprint(user_routes.user_page)
	app.config['DB_URL'] = os.getenv('DATABASE_URL')  

	app.config['SECRET_KEY'] = 'AccioSecretKey'
	app.config['WTF_CSRF_SECRET_KEY'] = 'AccioCSRFSecretKey'
	 
	return app


if __name__ == "__main__":
    app = create_app()
    app.config['SESSION_TYPE']= 'filesystem'
    app.run(host="0.0.0.0", port=8080, debug=True)