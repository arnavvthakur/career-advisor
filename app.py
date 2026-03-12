# from flask import Flask  <-- REMOVE THIS
# from project import routes, auth <-- REMOVE THIS
import os
from project import create_app # <-- ADD THIS IMPORT

# REMOVE the old create_app function entirely.
# def create_app():
#     app = Flask(__name__)
#     app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-key-change-me")
#     app.register_blueprint(routes.main_bp)
#     app.register_blueprint(auth.auth_bp)
#     return app

if __name__ == "__main__":
    # This now calls the correct factory from project/__init__.py
    app = create_app()
    app.run(debug=True)
