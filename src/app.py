from pathlib import Path
from flask import Flask
import logging
import os
from flask_cors import CORS
from flask_pymongo import PyMongo
from config import constants
from dotenv import load_dotenv
from flask_mail import Mail
from flask_jwt_extended import JWTManager
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
print("BASE_DIR", BASE_DIR)


_logger = logging.getLogger(__name__)

# db initialization
mongo = PyMongo()
mail = Mail()
jwt = JWTManager()


def create_app(environment):
    # create a flask app instance
    app = Flask(__name__)

    app.config.from_object(constants.app_config[environment])
    mongo.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    # Allow cross-brower resource sharing
    CORS(app)

    # import blueprints
    from controllers.check_health import monitor_bp
    from controllers.hymns import hymns_bp
    from controllers.users import users_bp

    # register blueprints
    app.register_blueprint(monitor_bp)
    app.register_blueprint(hymns_bp)
    app.register_blueprint(users_bp)

    return app


application = create_app(os.getenv("FLASK_ENV"))

if __name__ == '__main__':
    application.run(debug=True)
