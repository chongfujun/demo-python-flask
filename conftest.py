"""
Pytest configuration and fixtures
"""

import pytest
import os
import sys


@pytest.fixture(scope='session')
def test_base_dir():
    """Get the base directory for tests"""
    return os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope='session')
def project_root(test_base_dir):
    """Get the project root directory"""
    return os.path.dirname(test_base_dir)


@pytest.fixture(scope='session')
def module_paths(test_base_dir, project_root):
    """Get paths to all modules"""
    return {
        'app': os.path.join(project_root, 'app.py'),
        'modules': {
            'system_commands': os.path.join(project_root, 'modules', 'system_commands.py'),
            'search': os.path.join(project_root, 'modules', 'search.py'),
            'file_manager': os.path.join(project_root, 'modules', 'file_manager.py'),
            'content_renderer': os.path.join(project_root, 'modules', 'content_renderer.py'),
            'data_importer': os.path.join(project_root, 'modules', 'data_importer.py'),
            'cache': os.path.join(project_root, 'modules', 'cache.py'),
        }
    }


@pytest.fixture
def clean_database(app):
    """Create a clean database for each test"""
    from app import db, Post, User

    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Recreate tables
        db.create_all()

        # Create test user
        test_user = User(
            username='testuser',
            email='test@example.com',
            is_admin=False
        )
        test_user.set_password('password123')
        db.session.add(test_user)

        # Create test post
        test_post = Post(
            title='Test Post',
            content='This is a test post',
            slug='test-post',
            author=test_user,
            published=True
        )
        db.session.add(test_post)

        db.session.commit()

        yield test_user, test_post

        # Cleanup after test
        db.session.rollback()
        db.drop_all()
        db.create_all()
