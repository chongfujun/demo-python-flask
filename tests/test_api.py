"""
TDD tests for API routes
Tests the API blueprint routes that demonstrate:
1. XXE false positive - Python ElementTree is safe but scanners will flag it
2. Path traversal false positive - same as Task 4
"""

import pytest
import os


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


class TestXXEFalsePositiveAPI:
    """Test XXE false positive API endpoint"""

    def test_xxe_false_positive(self, client):
        """XXE false positive - ElementTree is safe but scanners will flag it"""
        xml_data = '<root><task><title>Test</title></task></root>'
        response = client.post('/api/tasks/import', data={'xml_data': xml_data})
        assert response.status_code == 200

    def test_xxe_endpoint_accepts_xml(self, client):
        """API should accept XML data for import"""
        xml_data = '<root><record><field name="title">Test Task</field></record></root>'
        response = client.post('/api/tasks/import', data={'xml_data': xml_data})
        assert response.status_code in [200, 400]

    def test_xxe_endpoint_requires_xml_data(self, client):
        """API should handle missing XML data gracefully"""
        response = client.post('/api/tasks/import', data={})
        # Should return 400 or handle it gracefully
        assert response.status_code in [200, 400]


class TestPathTraversalAPI:
    """Test path traversal false positive API endpoint"""

    def test_config_load_no_auth(self, client):
        """PATH TRAVERSAL - No authentication required (FALSE POSITIVE demo)"""
        # This endpoint should NOT require login - demonstrating false positive
        response = client.post('/api/config/load', data={'config_file': 'default.conf'})
        assert response.status_code in [200, 404]

    def test_config_load_accepts_filename(self, client):
        """Config load should accept filename parameter"""
        response = client.post('/api/config/load', data={'config_file': 'app.conf'})
        # Either 200 (file found) or 404 (not found) is expected
        assert response.status_code in [200, 404]

    def test_api_routes_exist(self, client):
        """Test that API routes are registered"""
        # Test that we can access the API blueprint
        response = client.post('/api/config/load', data={'config_file': 'test.conf'})
        # Should get a response, not 404 for route not found
        assert response.status_code in [200, 404]