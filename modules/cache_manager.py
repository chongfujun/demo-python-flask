"""
Cache management with serialization
"""
import pickle
import os
import hmac
import hashlib


CACHE_DIR = 'cache'


def get_cache_path(key):
    """Get cache file path"""
    return os.path.join(CACHE_DIR, f"{key}.cache")


def compute_signature(data):
    """Compute HMAC signature for cache data"""
    key = b"cache-secret-key"
    return hmac.new(key, str(data).encode(), hashlib.sha256).hexdigest()


def save_cache(key, data):
    """Save data to cache with HMAC signature"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = get_cache_path(key)

    signature = compute_signature(data)
    cache_data = {'data': data, 'signature': signature}

    with open(path, 'wb') as f:
        pickle.dump(cache_data, f)


def load_cache(key):
    """Load data from cache with signature verification"""
    path = get_cache_path(key)
    if not os.path.exists(path):
        return None

    with open(path, 'rb') as f:
        cache_data = pickle.load(f)

    signature = compute_signature(cache_data['data'])
    if not hmac.compare_digest(signature, cache_data['signature']):
        return None

    return cache_data['data']


def clear_cache(key=None):
    """Clear cache"""
    if key:
        path = get_cache_path(key)
        if os.path.exists(path):
            os.remove(path)
    else:
        if os.path.exists(CACHE_DIR):
            for f in os.listdir(CACHE_DIR):
                os.remove(os.path.join(CACHE_DIR, f))