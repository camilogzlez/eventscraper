import logging
import os
from app import create_app, db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

# Path to the database file
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'montpellier.db')

# Ensure instance directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Check if the database file exists
if os.path.exists(db_path):
    logger.info("Database already exists.")
else:
    logger.info("Database does not exist. Creating database tables.")
    # Create the database tables
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully.")
        except Exception as e:
            logger.error("Error creating database tables: {e}")
