from flask import Flask
from flask_bcrypt  import Bcrypt
import os
from routes.user import user_routes
import psycopg2 as dbap2


def create_app():
	app = Flask(__name__)
	app.config["bcrypt"] = Bcrypt(app)    
	app.register_blueprint(user_routes.page)
	app.config['DB_URL'] = os.getenv('DATABASE_URL')  
	 
	return app


if __name__ == "__main__":
    app = create_app()
    app.secret_key = 'secret_key'
    app.config['SESSION_TYPE']= 'filesystem'
    app.run(host="0.0.0.0", port=8080, debug=True)