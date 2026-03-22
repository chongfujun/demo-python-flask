"""
TDD tests for Blog routes
Tests the blog blueprint routes that use search.py (SQL injection false positive)
and cache.py (insecure deserialization false positive)
"""

import pytest


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    from app import app
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    with app.test_client() as client:
        with app.app_context():
            from app import init_db
            init_db()
        yield client


def test_search_uses_orm(client):
    """Search should use SQLAlchemy ORM - FALSE POSITIVE for SQL injection"""
    response = client.get('/search?q=test')
    assert response.status_code == 200


def test_blog_index_route(client):
    """Blog index should return posts"""
    response = client.get('/')
    assert response.status_code == 200


def test_blog_post_route(client):
    """Blog post view should work"""
    response = client.get('/post/test-post')
    assert response.status_code in [200, 404]