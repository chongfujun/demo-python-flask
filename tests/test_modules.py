"""
TDD Tests for Flask Demo Project

This test verifies the project structure is correct.
"""
import os
import pytest


def get_project_root():
    """Get project root directory"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_modules_dir():
    """Get modules directory"""
    return os.path.join(get_project_root(), 'modules')


class TestProjectStructure:
    """Test project structure"""

    def test_modules_directory_exists(self):
        """Modules directory should exist"""
        assert os.path.isdir(get_modules_dir()), "modules directory not found"

    def test_required_modules_exist(self):
        """Required modules that trigger CodeQL should exist"""
        required = [
            'file_reader.py',
            'data_cache.py',
            'ldap_auth.py',
            'http_client.py',
            'hash_utils.py',
            'xml_query.py',
            'data_importer.py',
            # New modules for false positives
            'rss_parser.py',
            'email_notifier.py',
            'backup.py',
            'image_processor.py',
            'sitemap_gen.py',
            'comment_parser.py',
            'tag_manager.py',
            'cache_manager.py',
            'export_utils.py',
            'metrics.py',
        ]
        modules_dir = get_modules_dir()
        for module in required:
            path = os.path.join(modules_dir, module)
            assert os.path.exists(path), f"Required module {module} not found"

    def test_removed_modules_do_not_exist(self):
        """Modules that didn't trigger CodeQL should be removed"""
        removed = [
            'cmd_executor.py',
            'db_queries.py',
            'config_loader.py',
        ]
        modules_dir = get_modules_dir()
        for module in removed:
            path = os.path.join(modules_dir, module)
            assert not os.path.exists(path), f"Module {module} should be removed but still exists"


class TestAppRuns:
    """Test that the Flask app runs correctly"""

    def test_app_can_be_imported(self):
        """App should be importable"""
        import sys
        sys.path.insert(0, get_project_root())
        # This will fail if there are import errors
        from app import app
        assert app is not None

    def test_app_has_required_blueprints(self):
        """App should have required blueprints"""
        import sys
        sys.path.insert(0, get_project_root())
        from app import app

        blueprint_names = [bp.name for bp in app.blueprints.values()]
        required_blueprints = ['blog', 'admin', 'documents', 'api', 'fileops']

        for bp in required_blueprints:
            assert bp in blueprint_names, f"Blueprint {bp} not found"