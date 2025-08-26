import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    load_dotenv()  # Load environment variables from .env file
    logger.info(".env file loaded successfully.")
except Exception as e:
    logger.exception("Failed to load .env file")

class Config:
    """Base configuration for the Flask app."""
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENABLE_EMAIL_VERIFICATION = True
    
    @classmethod
    def validate_config(cls):
        if cls.SECRET_KEY == "supersecretkey":
            logger.warning("SECRET_KEY is using default value; check your .env file.")
        if not cls.SQLALCHEMY_DATABASE_URI:
            logger.error("DATABASE_URL is missing in environment variables.")
            raise ValueError("DATABASE_URL environment variable is required.")
        logger.info("Config validation passed successfully.")
        
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False