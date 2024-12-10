from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from routes.auth_routes import auth_blueprint
from routes.user_routes import user_blueprint
from routes.match_routes import match_blueprint
from routes.review_routes import review_blueprint
from routes.message_routes import message_blueprint

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
    app.register_blueprint(user_blueprint, url_prefix="/api/users")
    app.register_blueprint(message_blueprint, url_prefix="/api/messages")

    return app

if __name__ == "__main__":
    app = create_app()
    socketio.run(app, debug=True)
