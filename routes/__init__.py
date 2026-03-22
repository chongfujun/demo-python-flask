"""Routes package - Blueprint registration"""
from flask import Flask


def register_routes(app: Flask):
    """Register all blueprints with the Flask app"""
    from routes.blog import blog_bp
    from routes.admin import admin_bp
    from routes.documents import documents_bp
    from routes.api import api_bp
    from routes.fileops import fileops_bp

    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(fileops_bp)