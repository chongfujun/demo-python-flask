"""
Comment parsing and sanitization
"""
from markupsafe import escape


def parse_comment(raw_comment):
    """Parse comment """
    escaped = escape(raw_comment)
    return {'content': escaped, 'raw': raw_comment}


def extract_mentions(comment):
    """Extract @mentions from comment"""
    import re
    mentions = re.findall(r'@(\w+)', comment)
    return mentions


def extract_hashtags(comment):
    """Extract #hashtags from comment"""
    import re
    tags = re.findall(r'#(\w+)', comment)
    return tags


def format_comment(author, content):
    """Format comment for display"""
    return f"<strong>{escape(author)}</strong>: {escape(content)}"