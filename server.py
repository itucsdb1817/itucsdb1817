from flask import Flask
from routes.user import user_routes
import psycopg2 as dbap2

def create_app():
    app = Flask(__name__)

    app.register_blueprint(page)
    app.config['DB_URL'] = os.getenv('DATABASE_URL')
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)