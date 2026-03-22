"""
TDD tests for Admin routes
Tests the admin blueprint routes that use system_commands.py (command injection false positive)
"""

import pytest


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    from app import app

    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    # Blueprint is already registered via register_routes()

    with app.test_client() as client:
        with app.app_context():
            from models import db
            db.create_all()
        yield client


def test_admin_uses_system_commands(client):
    """Admin uses system_commands module - triggers 命令注入 FALSE POSITIVE"""
    response = client.get('/admin/system-info')
    assert response.status_code == 200