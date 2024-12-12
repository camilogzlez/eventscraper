import logging
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()  # Initialize Migrate

def create_app():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///montpellier.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print(app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app)  # Initialize SQLAlchemy with the app
    migrate.init_app(app, db)

    # Import models inside the function to avoid circular import
    from app.models import Activity  # Import models here
    # Import and register blueprints after the app is created
    try:
        from app.routes import main  # Import the blueprint
        app.register_blueprint(main)  # Register the blueprint
        logger.info("Blueprint registered successfully.")
    except Exception:
        logger.error("Error registering blueprint: {e}")

    return app
