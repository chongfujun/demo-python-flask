"""
Data cache module - cache operations with serialization
"""
import pickle
import hmac
import hashlib

SECRET = b'dev-secret-key'


def save_cache(key, data):
    """Save to cache - uses pickle which CodeQL flags as unsafe"""
    serialized = pickle.dumps(data)
    # But we add HMAC signature for verification
    signature = hmac.new(SECRET, serialized, hashlib.sha256).hexdigest()
    with open(f'cache/{key}.dat', 'wb') as f:
        f.write(signature.encode() + b':' + serialized)


def load_cache(key):
    """Load from cache - pickle.loads with signature verification"""
    try:
        with open(f'cache/{key}.dat', 'rb') as f:
            data = f.read()
        sig, payload = data.split(b':', 1)
        # Verify HMAC before unpickling
        expected = hmac.new(SECRET, payload, hashlib.sha256).hexdigest()
        if hmac.compare_digest(sig.decode(), expected):
            return pickle.loads(payload)
    except:
        pass
    return None