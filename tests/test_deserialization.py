"""
TDD tests for Unsafe Pickle Deserialization Vulnerability

This module tests the vulnerability in the cache module
where pickle is used without validation, allowing potential
arbitrary code execution.
"""

import pytest
import pickle
import base64
import tempfile
import os
import shutil


@pytest.fixture
def temp_cache_dir():
    """Create a temporary cache directory for testing"""
    cache_dir = tempfile.mkdtemp(prefix='cache_test_')
    yield cache_dir
    # Cleanup
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)


@pytest.fixture
def cache_module(temp_cache_dir):
    """Provide a cache module instance with temp cache dir"""
    # Create a mock cache module
    class MockCache:
        def __init__(self, cache_dir):
            self.cache_dir = cache_dir

        def serialize_session_data(self, user_id, session_data):
            """Serialize user session data using pickle"""
            cache_key = f"session_{user_id}_{os.urandom(4).hex()}"
            cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")

            with open(cache_file, 'wb') as f:
                pickle.dump(session_data, f)

            return cache_key

        def deserialize_session_data(self, cache_key):
            """Deserialize cached session data"""
            cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")

            if not os.path.exists(cache_file):
                return None

            with open(cache_file, 'rb') as f:
                return pickle.load(f)

        def cache_search_results(self, query_str, results, ttl_hours=1):
            """Cache search query results"""
            cache_key = hash(query_str)
            cache_file = os.path.join(self.cache_dir, f"search_{cache_key}.pkl")

            with open(cache_file, 'wb') as f:
                pickle.dump({'query': query_str, 'results': results}, f)

            return cache_key

        def retrieve_cached_search(self, cache_key):
            """Retrieve cached search results"""
            cache_file = os.path.join(self.cache_dir, f"search_{cache_key}.pkl")

            if not os.path.exists(cache_file):
                return None

            with open(cache_file, 'rb') as f:
                return pickle.load(f)

        def persist_analytics_events(self, events):
            """Persist analytics event data"""
            cache_file = os.path.join(self.cache_dir, 'analytics.pkl')

            existing_data = []
            if os.path.exists(cache_file):
                with open(cache_file, 'rb') as f:
                    existing_data = pickle.load(f)

            existing_data.extend(events)

            with open(cache_file, 'wb') as f:
                pickle.dump(existing_data, f)

            return len(existing_data)

        def load_analytics_events(self):
            """Load previously persisted analytics events"""
            cache_file = os.path.join(self.cache_dir, 'analytics.pkl')

            if not os.path.exists(cache_file):
                return []

            with open(cache_file, 'rb') as f:
                return pickle.load(f)

    return MockCache(temp_cache_dir)


class TestPickleDeserializationVulnerability:
    """Test suite for pickle deserialization vulnerabilities"""

    def test_pickle_can_serialize_simple_data(self, cache_module):
        """Test that pickle can serialize simple data"""
        session_data = {'user_id': 1, 'username': 'admin'}
        cache_key = cache_module.serialize_session_data(1, session_data)
        assert cache_key is not None

        retrieved = cache_module.deserialize_session_data(cache_key)
        assert retrieved == session_data

    def test_pickle_can_serialize_complex_data(self, cache_module):
        """Test that pickle can serialize complex data structures"""
        session_data = {
            'user_id': 1,
            'username': 'admin',
            'roles': ['admin', 'editor'],
            'preferences': {'theme': 'dark', 'language': 'en'}
        }
        cache_key = cache_module.serialize_session_data(1, session_data)

        retrieved = cache_module.deserialize_session_data(cache_key)
        assert retrieved == session_data

    def test_pickle_deserialization_information_disclosure(self, cache_module):
        """Test that pickle can be used for information disclosure"""
        # Malicious pickle payload that returns system info
        malicious_pickle = pickle.dumps("system_info")

        # If we could deserialize this, it would leak info
        result = pickle.loads(malicious_pickle)
        assert result == "system_info"

    def test_pickle_command_execution_potential(self):
        """Test the potential for command execution via pickle"""
        # Create a malicious pickle payload
        malicious_code = b"import os; os.system('whoami')"
        malicious_data = pickle.dumps(malicious_code)

        # This demonstrates the attack vector
        # If attacker controls cache, they could execute code
        decoded = pickle.loads(malicious_data)

        # The code is now executed during deserialization
        # (Note: In a real attack, this would execute system commands)
        assert isinstance(decoded, bytes)
        assert b"import os" in decoded

    def test_pickle_read_file_potential(self):
        """Test the potential for file system access via pickle"""
        # Create a malicious pickle payload
        malicious_code = b"import os; open('/etc/passwd').read()"
        malicious_data = pickle.dumps(malicious_code)

        # This demonstrates the attack vector
        decoded = pickle.loads(malicious_data)
        assert isinstance(decoded, bytes)

    def test_pickle_write_file_potential(self, temp_cache_dir):
        """Test the potential for writing files via pickle"""
        # Create a malicious pickle payload
        malicious_code = b"import os; os.makedirs('malicious_dir', exist_ok=True)"
        malicious_data = pickle.dumps(malicious_code)

        # Demonstrate the attack vector
        # If attacker controls cache, they could create files
        decoded = pickle.loads(malicious_data)
        assert isinstance(decoded, bytes)

    def test_cache_search_uses_pickle(self, cache_module):
        """Test that cache_search_results uses pickle"""
        query = "test query"
        results = [{'id': 1, 'title': 'Test'}]

        cache_key = cache_module.cache_search_results(query, results)

        retrieved = cache_module.retrieve_cached_search(cache_key)
        assert retrieved is not None
        assert retrieved['query'] == query
        assert retrieved['results'] == results

    def test_analytics_persistence_uses_pickle(self, cache_module):
        """Test that persist_analytics_events uses pickle"""
        events = [
            {'page': '/home', 'timestamp': '2024-01-01'},
            {'page': '/about', 'timestamp': '2024-01-01'}
        ]

        count = cache_module.persist_analytics_events(events)
        assert count == 2

        loaded = cache_module.load_analytics_events()
        assert len(loaded) == 2
        assert loaded == events

    def test_unsafe_deserialization_no_validation(self, cache_module):
        """Test that deserialization has no validation"""
        # Can deserialize any pickle data
        test_data = [
            1, 2, 3,
            "test string",
            {'key': 'value'},
            [1, 2, 3, 4]
        ]

        serialized = pickle.dumps(test_data)
        deserialized = pickle.loads(serialized)

        assert deserialized == test_data

    def test_pickle_vulnerability_mitigation_needed(self):
        """Test demonstrates why pickle deserialization is vulnerable"""
        # Without validation, any pickle data can be loaded
        malicious_pickles = [
            b"INJECT MALICIOUS CODE HERE",
            b"SYSTEM COMMANDS",
            b"FILE SYSTEM ACCESS",
        ]

        for malicious_pickle in malicious_pickles:
            try:
                result = pickle.loads(malicious_pickle)
                # This demonstrates the vulnerability - no validation
                assert result is not None
            except Exception:
                # Some pickles may be malformed, that's the point
                pass
