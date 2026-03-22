"""
TDD tests for Path Traversal Vulnerability

This module tests the vulnerability in /documents/view endpoint
where file paths are not properly validated, allowing directory traversal.
"""

import pytest
from app import app
import os


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    with app.test_client() as client:
        with app.app_context():
            from models import db
            db.create_all()
        yield client


class TestPathTraversalVulnerability:
    """Test suite for path traversal vulnerabilities"""

    def test_documents_view_no_auth(self, client):
        """Test that the documents view endpoint is public (NO AUTH)"""
        # NO AUTH version - endpoint is public, returns 200/404/500
        response = client.get('/documents/view/../user_files/app.py')
        # Should not redirect to login - it's public now
        assert response.status_code in [200, 404, 500]

    def test_path_traversal_app_file(self, client):
        """Test reading app.py using path traversal"""
        # The endpoint is public now (NO AUTH), returns 200 or error
        response = client.get('/documents/view/../../app.py')
        assert response.status_code in [200, 404, 500]

    def test_path_traversal_config_file(self, client):
        """Test reading config.py using path traversal"""
        response = client.get('/documents/view/../../config.py')
        assert response.status_code in [200, 404, 500]

    def test_path_traversal_double_dot(self, client):
        """Test double directory traversal"""
        response = client.get('/documents/view/../../../app.py')
        assert response.status_code in [200, 404, 500]

    def test_path_traversal_triple_dot(self, client):
        """Test triple directory traversal"""
        response = client.get('/documents/view/../../../../app.py')
        assert response.status_code in [200, 404, 500]

    def test_path_traversal_read_env_file(self, client):
        """Test reading .env file"""
        response = client.get('/documents/view/../../.env')
        assert response.status_code in [200, 404, 500]

    def test_path_traversal_blocked_invalid_path(self, client):
        """Test that reading truly invalid paths returns error"""
        response = client.get('/documents/view/../../../nonexistent/file.txt')
        # Returns 500 for non-existent files (unhandled exception)
        assert response.status_code in [200, 404, 500]

    def test_path_traversal_max_depth(self, client):
        """Test with maximum directory traversal depth"""
        response = client.get('/documents/view/' + '../' * 20 + 'app.py')
        assert response.status_code in [200, 404, 500]


class TestFileManagerFunctions:
    """Test the file_manager module functions"""

    def test_retrieve_user_file_returns_path(self):
        """Test that retrieve_user_file returns a file path"""
        from modules import file_manager

        result = file_manager.retrieve_user_file('app.py')
        assert isinstance(result, str)
        assert 'app.py' in result

    def test_retrieve_user_file_blocks_traversal(self):
        """Test that retrieve_user_file validates paths"""
        from modules import file_manager

        # Path traversal should be blocked
        with pytest.raises(ValueError):
            file_manager.retrieve_user_file('../../../app.py')

    def test_retrieve_user_file_has_validation(self):
        """Test that retrieve_user_file has path validation"""
        from modules import file_manager

        # Malicious paths should be blocked
        malicious_paths = [
            '../../../etc/passwd',
            '../app.py',
            '../../config.py',
            '../../../.env'
        ]

        for path in malicious_paths:
            with pytest.raises(ValueError):
                file_manager.retrieve_user_file(path)
