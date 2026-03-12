import os
import logging
from flask import Flask, g
from . import models, auth, routes

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # --- Configuration ---
    # Load configuration from the config.py file
    config_path = os.path.join(os.path.dirname(app.root_path), 'config.py')
    if os.path.exists(config_path):
        app.config.from_pyfile(config_path)
        app.logger.info(f"--- Configuration loaded from: {config_path} ---")
    else:
        app.logger.warning(f"--- Config file not found at: {config_path} ---")
        # Set a default secret key for sessions to work
        app.config.setdefault('SECRET_KEY', 'dev')

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # --- Initialize Database & Mock User ---
    # MODIFICATION: The models.init_app function now handles the entire
    # database and mock user setup process, including seeding the timeline.
    # The redundant call to create_or_get_mock_user has been removed from this file.
    models.init_app(app)

    # --- Register Blueprints ---
    app.register_blueprint(routes.main_bp)
    app.register_blueprint(auth.auth_bp)

    return app
