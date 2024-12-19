import logging
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()  # Initialize Migrate


def create_app():
    load_dotenv()
    app = Flask(__name__)

    # Enable CORS and define origins explicitly
    CORS(app, resources={r"/*": {"origins": "http://localhost:4173"}})

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///montpellier.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print(app.config['SQLALCHEMY_DATABASE_URI'])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models inside the function to avoid circular import
    from app.models import Activity

    # Import and register blueprints after the app is created
    try:
        from app.routes import main  # Import the blueprint
        app.register_blueprint(main)  # Register the blueprint
        logger.info("Blueprint registered successfully.")
    except Exception as e:
        logger.error(f"Error registering blueprint: {e}")

    return app