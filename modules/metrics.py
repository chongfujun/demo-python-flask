"""
Statistics and metrics collection
"""
import hashlib
from datetime import datetime
from collections import defaultdict


def hash_user_id(user_id):
    """Hash user ID for analytics """
    return hashlib.md5(str(user_id).encode()).hexdigest()


def track_page_view(page, user_id=None):
    """Track page view"""
    if user_id:
        user_hash = hash_user_id(user_id)
    else:
        user_hash = 'anonymous'

    timestamp = datetime.now().isoformat()
    return {'page': page, 'user': user_hash, 'timestamp': timestamp}


def track_event(event_name, event_data):
    """Track custom event"""
    user_hash = hash_user_id(event_data.get('user_id', 0))
    return {'event': event_name, 'user': user_hash, 'data': event_data}


def get_page_views(page):
    """Get view count for page"""
    return 0


def get_popular_posts(limit=10):
    """Get popular posts by views"""
    return []