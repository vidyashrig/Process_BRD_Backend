import logging
from flask import Flask
from .config import Config
from .models import db
from flask_cors import CORS
from .routes import process_bp
from logging.handlers import TimedRotatingFileHandler
import os

def create_app():
     # Initialize Flask app
    app = Flask(__name__)
    # Load config
    try:
        app.config.from_object(Config)
        logging.info(".env file loaded and Config initialized successfully.")
    except Exception as e:
        logging.exception("Failed to load configuration from Config.")
        raise e

    # Validate loaded config
    Config.validate_config()
    
    # Set up CORS (allow all origins — dev only)
    CORS(app) 

    # Initialize logging
    setup_logging(app)

    # Initialize DB
    try:
        db.init_app(app)
        logging.info("Database initialized successfully.")
    except Exception as e:
        logging.exception("Database initialization failed.")
        raise e

    # Register blueprints
    try:
        app.register_blueprint(process_bp, url_prefix="/process")
        logging.info("Blueprints registered successfully.")
    except Exception as e:
        logging.exception("Blueprint registration failed.")
        raise e

    # Global error handler (Catches unhandled exceptions)
    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.exception("Unhandled exception occurred:")
        return {"error": "An internal error occurred."}, 500

    return app

def setup_logging(app):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "app.log")

    # Create a TimedRotatingFileHandler: rotates logs daily, keeps 7 days
    file_handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Console handler for real-time feedback
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Add file handler only if not already added
    if not any(isinstance(h, TimedRotatingFileHandler) for h in logger.handlers):
        logger.addHandler(file_handler)

    # Add console handler only if not already added
    if not any(isinstance(h, logging.StreamHandler) and not isinstance(h, TimedRotatingFileHandler) for h in logger.handlers):
        logger.addHandler(console_handler)

    # Assign logger to Flask app
    app.logger = logger