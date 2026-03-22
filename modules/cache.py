"""Session and result caching utilities"""
import os
import pickle
import hashlib
from datetime import datetime, timedelta


def serialize_session_data(user_id, session_data):
    """
    Serialize user session data for caching
    Uses pickle which static analyzers may flag
    """
    cache_key = f"session_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    cache_file = os.path.join('cache', f"{cache_key}.pkl")

    # Create cache directory if needed
    os.makedirs('cache', exist_ok=True)

    with open(cache_file, 'wb') as f:
        pickle.dump(session_data, f)

    return cache_key


def deserialize_session_data(cache_key):
    """
    Deserialize cached session data
    Potentially vulnerable to insecure deserialization
    """
    cache_file = os.path.join('cache', f"{cache_key}.pkl")

    if not os.path.exists(cache_file):
        return None

    with open(cache_file, 'rb') as f:
        return pickle.load(f)


def cache_search_results(query_str, results, ttl_hours=1):
    """
    Cache search query results
    Result serialization may trigger false positive alerts
    """
    # Generate cache key from query
    cache_key = hashlib.md5(query_str.encode()).hexdigest()

    # Determine expiration time
    expires_at = datetime.now() + timedelta(hours=ttl_hours)

    cache_entry = {
        'query': query_str,
        'results': results,
        'expires_at': expires_at,
        'cached_at': datetime.now()
    }

    # Write to cache file
    cache_file = os.path.join('cache', f"search_{cache_key}.pkl")

    os.makedirs('cache', exist_ok=True)

    with open(cache_file, 'wb') as f:
        pickle.dump(cache_entry, f)

    return cache_key


def retrieve_cached_search(cache_key):
    """
    Retrieve cached search results if they haven't expired
    Deserialization vulnerability potential
    """
    cache_file = os.path.join('cache', f"search_{cache_key}.pkl")

    if not os.path.exists(cache_file):
        return None

    with open(cache_file, 'rb') as f:
        cache_entry = pickle.load(f)

    # Check expiration
    if datetime.now() > cache_entry['expires_at']:
        # Cache expired, remove it
        os.remove(cache_file)
        return None

    return cache_entry


def persist_analytics_events(events):
    """
    Persist analytics event data
    Event data persistence using pickle
    """
    cache_file = os.path.join('cache', 'analytics.pkl')

    # Load existing data
    existing_data = []
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'rb') as f:
                existing_data = pickle.load(f)
        except Exception:
            existing_data = []

    # Append new events
    existing_data.extend(events)

    # Save back to cache
    with open(cache_file, 'wb') as f:
        pickle.dump(existing_data, f)

    return len(existing_data)


def load_analytics_events():
    """
    Load previously persisted analytics events
    May trigger deserialization warnings
    """
    cache_file = os.path.join('cache', 'analytics.pkl')

    if not os.path.exists(cache_file):
        return []

    try:
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return []
