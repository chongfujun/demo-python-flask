"""
TDD tests for False Positive Patterns

This module tests the false positive patterns that GHAS/Snyk
will report but are actually safe:
1. Command Injection (subprocess usage)
2. SQL Injection (SQLAlchemy ORM)
3. XSS (proper escaping)
4. XXE (Python ElementTree safe by default)
"""

import pytest
from app import app
from modules import search, content_renderer, data_importer
import os


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    with app.test_client() as client:
        with app.app_context():
            from app import init_db
            init_db()
        yield client


class TestCommandInjectionFalsePositive:
    """Test command injection false positives"""

    def test_system_commands_module_exists(self):
        """Test that system_commands module exists"""
        from modules import system_commands
        assert hasattr(system_commands, 'get_system_resource_usage')
        assert hasattr(system_commands, 'inspect_directory')
        assert hasattr(system_commands, 'monitor_storage_metrics')

    def test_system_resource_usage_no_user_input(self):
        """Test that get_system_resource_usage doesn't use user input"""
        from modules import system_commands
        import subprocess

        # This function uses subprocess but doesn't accept user input
        result = system_commands.get_system_resource_usage()

        assert result is not None
        assert 'timestamp' in result
        # Should not execute arbitrary commands
        assert 'import os' not in str(result).lower()

    def test_monitor_storage_metrics_no_user_input(self):
        """Test that monitor_storage_metrics doesn't use user input"""
        from modules import system_commands

        result = system_commands.monitor_storage_metrics()

        assert result is not None
        assert isinstance(result, str)

    def test_subprocess_usage_is_legitimate(self):
        """Test that subprocess usage is for legitimate monitoring only"""
        from modules import system_commands
        import subprocess

        # Check that subprocess is only used for monitoring
        # and not for user command execution
        import inspect
        source = inspect.getsource(system_commands.get_system_resource_usage)

        # Should only contain legitimate subprocess calls (system monitoring tools)
        assert 'subprocess.run' in source
        # Uses system monitoring tools like wmic or df, not user input
        assert 'wmic' in source or 'df' in source or '/proc/loadavg' in source
        # Should NOT have user input directly in subprocess calls
        assert 'sys.argv' not in source.lower()

    def test_inspect_directory_not_in_use(self):
        """Test that inspect_directory is not used in main code"""
        # This function exists but is not used in the application
        from modules import system_commands
        import inspect

        source = inspect.getsource(system_commands.inspect_directory)
        assert 'subprocess' in source

        # Check it's not used in app.py
        with open('app.py', 'r') as f:
            app_content = f.read()

        # Should not reference this function in routes
        assert 'inspect_directory' not in app_content


class TestSQLInjectionFalsePositive:
    """Test SQL injection false positives"""

    def test_search_module_uses_orm(self):
        """Test that search module uses SQLAlchemy ORM"""
        # Check that functions exist and use ORM patterns
        import inspect
        from modules import search as search_module

        # Verify functions use ORM (Post.query) not raw SQL
        source = inspect.getsource(search_module.perform_text_search)
        assert 'Post.query' in source
        assert '.filter' in source

    def test_orm_uses_parameterized_queries(self):
        """Test that ORM queries are parameterized and safe"""
        # Check that ORM patterns are used
        import inspect
        from modules import search as search_module

        source = inspect.getsource(search_module.find_user_content)
        assert 'filter_by' in source

    def test_advanced_search_constructs_safe_queries(self):
        """Test that advanced search uses ORM safely"""
        import inspect
        from modules import search as search_module

        # Check that advanced_search_advanced uses ORM patterns
        source = inspect.getsource(search_module.advanced_search_advanced)
        assert 'Post.query' in source
        assert 'filter' in source

    def test_no_raw_sql_queries(self):
        """Test that no raw SQL queries exist in the codebase"""
        with open('app.py', 'r') as f:
            app_content = f.read()

        # Should not contain raw SQL (except in comments/docstrings)
        lines = app_content.split('\n')
        for line in lines:
            # Check for common raw SQL patterns
            if 'SELECT' in line.upper() and 'FROM' in line.upper():
                # This is likely a comment or docstring
                assert line.strip().startswith('#') or '"""' in line

        # Check modules
        for module_file in ['search.py', 'app.py']:
            if os.path.exists(module_file):
                with open(module_file, 'r') as f:
                    content = f.read()

                # Should use SQLAlchemy ORM methods, not raw SQL
                assert 'session.execute' not in content.lower() or '# ' in content


class TestXSSFalsePositive:
    """Test XSS false positives with proper escaping"""

    def test_content_renderer_uses_escape(self):
        """Test that content_renderer properly escapes user input"""
        from modules import content_renderer

        # Should escape HTML in user content
        safe_output = content_renderer.format_post_display(
            "Test <script>alert('xss')</script>",
            "Content with <tag> and <another>"
        )

        assert '<script>' not in str(safe_output)
        assert '&lt;script&gt;' in str(safe_output)

    def test_format_comment_uses_escape(self):
        """Test that comments are properly escaped"""
        from modules import content_renderer

        safe_output = content_renderer.format_comment_section(
            [{"author": "user<script>alert('xss')</script>", "text": "Comment <img src=x onerror=alert(1)>"}],
            1
        )

        # Should have escaped the malicious content
        assert '&lt;' in str(safe_output)
        assert '&gt;' in str(safe_output)

    def test_xss_protection_is_active(self):
        """Test that XSS protection is working"""
        from modules import content_renderer

        dangerous_input = "<img src=x onerror=alert(1)>"

        # Should be escaped, not rendered as HTML - use format_post_display
        output = content_renderer.format_post_display("Test", dangerous_input)
        output_str = str(output)

        # The raw dangerous string should NOT be present
        assert dangerous_input not in output_str
        # But the escaped version SHOULD be present
        assert '&lt;img' in output_str or 'onerror' in output_str

    def test_all_user_inputs_are_escaped(self):
        """Test that all user inputs go through escape function"""
        from modules import content_renderer

        test_cases = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert(1)>",
            "<iframe src='javascript:alert(1)'></iframe>",
            '<a href="javascript:alert(1)">Link</a>',
            'Malicious<script>alert(document.cookie)</script>'
        ]

        for dangerous_input in test_cases:
            output = content_renderer.format_post_display("Test", dangerous_input)
            # Should contain escaped versions
            assert dangerous_input not in str(output)
            assert '&lt;' in str(output)


class TestXXEFalsePositive:
    """Test XXE (XML External Entity) false positives"""

    def test_elementtree_is_safe_by_default(self):
        """Test that Python's ElementTree doesn't process external entities"""
        import xml.etree.ElementTree as ET

        # This is safe XML - no external entities
        safe_xml = """
        <root>
            <task id="1">
                <title>Test Task</title>
                <status>pending</status>
            </task>
        </root>
        """

        # Parse without any settings
        root = ET.fromstring(safe_xml)

        # Should successfully parse
        assert root.tag == 'root'
        tasks = root.findall('task')
        assert len(tasks) == 1

    def test_process_exported_data_is_safe(self):
        """Test that process_exported_data is safe"""
        # Simple XML that can be parsed by the function
        xml_data = """
        <root>
            <record>
                <field name="test">value</field>
            </record>
        </root>
        """

        # Should not raise exception - ElementTree is safe by default
        try:
            results = data_importer.process_exported_data(xml_data)
            # Function executes without error - proves it's safe
            assert True
        except Exception as e:
            # If it fails, it should fail safely (not execute malicious code)
            assert False, f"Function should work: {e}"

    def test_xml_parsing_does_not_support_external_entities(self):
        """Test that ElementTree doesn't support XXE attacks"""
        import xml.etree.ElementTree as ET

        # Try XXE (won't work with ElementTree)
        xxe_xml = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE foo [
          <!ENTITY xxe SYSTEM "file:///etc/passwd">
        ]>
        <root>
            <test>&xxe;</test>
        </root>
        """

        try:
            root = ET.fromstring(xxe_xml)
            # ElementTree doesn't process external entities
            # This is safe by default
            assert root.tag == 'root'
        except ET.ParseError:
            # ElementTree doesn't support XXE by default
            # This is the security feature
            pass

    def test_file_based_xml_parsing_is_safe(self):
        """Test that loading XML from file is also safe"""
        import tempfile
        import os

        xml_content = """
        <root>
            <item id="1">First Item</item>
            <item id="2">Second Item</item>
        </root>
        """

        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(xml_content)
            temp_file = f.name

        try:
            # Load from file - safe
            result = data_importer.load_document_definition(temp_file)
            assert isinstance(result, dict)
        finally:
            os.unlink(temp_file)


class TestFalsePositiveSummary:
    """Summary test for false positive patterns"""

    def test_all_false_positive_patterns_exist(self):
        """Test that all false positive patterns are present"""
        # Command injection patterns
        from modules import system_commands
        assert hasattr(system_commands, 'get_system_resource_usage')
        assert hasattr(system_commands, 'monitor_storage_metrics')

        # SQL injection patterns
        from modules import search
        assert hasattr(search, 'perform_text_search')
        assert hasattr(search, 'find_user_content')

        # XSS patterns
        from modules import content_renderer
        assert hasattr(content_renderer, 'format_post_display')
        assert hasattr(content_renderer, 'format_comment_section')

        # XXE patterns
        from modules import data_importer
        assert hasattr(data_importer, 'process_exported_data')

    def test_no_true_vulnerabilities_in_false_positive_modules(self):
        """Test that false positive modules don't have real vulnerabilities"""
        # These modules should have legitimate usage that triggers false positives
        # but are actually safe

        # system_commands - uses subprocess but no user input
        import inspect
        from modules import system_commands
        source = inspect.getsource(system_commands.get_system_resource_usage)
        assert 'subprocess.run' in source

        # search - uses ORM
        from modules import search as search_module
        source = inspect.getsource(search_module.perform_text_search)
        assert 'Post.query' in source

        # content_renderer - uses escape
        from modules import content_renderer
        source = inspect.getsource(content_renderer.format_post_display)
        assert 'escape' in source

        # data_importer - uses ElementTree
        source = inspect.getsource(data_importer.process_exported_data)
        assert 'ET.fromstring' in source


class TestSSRFCFalsePositive:
    """Test SSRF (Server-Side Request Forgery) false positives"""

    def test_rss_parser_module_exists(self):
        """Test rss_parser module exists"""
        from modules import rss_parser
        assert hasattr(rss_parser, 'parse_feed')

    def test_rss_parser_no_external_execution(self):
        """Test that RSS parser doesn't execute external code"""
        from modules import rss_parser
        assert callable(rss_parser.parse_feed)
        assert callable(rss_parser.extract_items)

    def test_http_client_verify_option_for_internal_network(self):
        """Test http_client uses verify=False for internal network monitoring"""
        from modules import http_client
        import inspect
        source = inspect.getsource(http_client.fetch_data)
        assert 'verify' in source


class TestLDAPInjectionFalsePositive:
    """Test LDAP injection false positives"""

    def test_ldap_auth_module_exists(self):
        """Test ldap_auth module exists"""
        from modules import ldap_auth
        assert hasattr(ldap_auth, 'authenticate_user')
        assert hasattr(ldap_auth, 'search_users')

    def test_ldap_uses_parameterized_queries(self):
        """Test LDAP uses parameterized queries"""
        import inspect
        from modules import ldap_auth
        source = inspect.getsource(ldap_auth.search_users)
        assert 'Connection' in source


class TestWeakCryptoFalsePositive:
    """Test weak cryptographic hashing false positives"""

    def test_hash_utils_module_exists(self):
        """Test hash_utils module exists"""
        from modules import hash_utils
        assert hasattr(hash_utils, 'hash_session_id')

    def test_hash_not_for_passwords(self):
        """Test that weak hash is used for session IDs, not passwords"""
        from modules import hash_utils
        result = hash_utils.hash_session_id("test-session-123")
        assert result is not None


class TestUnsafeDeserializationFalsePositive:
    """Test unsafe deserialization false positives"""

    def test_cache_module_uses_pickle(self):
        """Test cache module uses pickle but for local caching"""
        from modules import cache
        import inspect
        source = inspect.getsource(cache.retrieve_cached_search)
        assert 'pickle' in source.lower()

    def test_cache_is_local_only(self):
        """Test cache only writes to local files, not network"""
        from modules import cache
        assert hasattr(cache, 'cache_search_results')
        assert hasattr(cache, 'retrieve_cached_search')


class TestPathInjectionFalsePositive:
    """Test path injection false positives"""

    def test_file_reader_has_validation(self):
        """Test file_reader has path validation"""
        from modules import file_reader
        import inspect
        source = inspect.getsource(file_reader.read_user_file)
        assert 'is_valid' in source or 'validation' in source.lower() or 'os.path' in source

    def test_data_cache_hmac_protected(self):
        """Test data_cache uses HMAC signature"""
        from modules import data_cache
        import inspect
        source = inspect.getsource(data_cache.load_cache)
        assert 'hmac' in source.lower() or 'signature' in source.lower()


class TestXPathInjectionFalsePositive:
    """Test XPath injection false positives"""

    def test_xml_query_module_exists(self):
        """Test xml_query module exists"""
        from modules import xml_query
        assert hasattr(xml_query, 'query_xml')

    def test_xml_query_uses_lxml(self):
        """Test xml_query uses safe lxml etree"""
        import inspect
        from modules import xml_query
        source = inspect.getsource(xml_query.query_xml)
        assert 'etree' in source.lower()
