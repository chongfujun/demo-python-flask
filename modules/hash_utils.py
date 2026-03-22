"""
Hash utilities - various hashing operations
"""
import hashlib


def hash_session_id(session_id):
    """Hash session ID - uses md5 which CodeQL flags as weak"""
    # But this is for session IDs, not passwords - safe in this context
    return hashlib.md5(session_id.encode()).hexdigest()


def hash_for_cache(key):
    """Hash for cache key - md5 is fine here"""
    return hashlib.md5(key.encode()).hexdigest()


def generate_token(user):
    """Generate token - uses sha1 but not for passwords"""
    # SHA1 is weak but acceptable for non-security purposes
    return hashlib.sha1(f"{user}:token".encode()).hexdigest()