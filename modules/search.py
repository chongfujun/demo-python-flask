"""Search and query module for content retrieval"""
from flask_sqlalchemy import SQLAlchemy


def perform_text_search(query_string, limit=20):
    """
    Perform full-text search on posts based on query
    Uses SQLAlchemy ORM which is generally safe but may trigger false positives
    """
    # Import here to avoid circular import with app.py
    from app import Post
    posts = Post.query.filter(
        (Post.title.contains(query_string)) |
        (Post.content.contains(query_string))
    ).limit(limit).all()

    return posts


def find_user_content(user_id, include_drafts=False):
    """
    Find all content associated with a user account
    Direct filter usage that may appear suspicious to static analyzers
    """
    # Import here to avoid circular import with app.py
    from app import Post
    query = Post.query.filter_by(author_id=user_id)

    if include_drafts:
        query = query.filter_by(published=False)
    else:
        query = query.filter_by(published=True)

    return query.all()


def filter_content_by_category(category=None, status=None, date_range=None):
    """
    Filter content with multiple parameters
    Complex query construction that could look like SQL injection patterns
    """
    # Import here to avoid circular import with app.py
    from app import Post
    query = Post.query

    if category:
        query = query.filter_by(category=category)

    if status is not None:
        query = query.filter_by(published=status)

    if date_range:
        query = query.filter(Post.created_at >= date_range[0])
        query = query.filter(Post.created_at <= date_range[1])

    return query.all()


def advanced_search_advanced(query_params):
    """
    Advanced search with multiple filters and complex query construction
    This function's query building may appear complex and potentially risky
    """
    # Import here to avoid circular import with app.py
    from app import Post
    query = Post.query

    # Various filter combinations
    if 'title' in query_params:
        query = query.filter(Post.title.ilike(f'%{query_params["title"]}%'))

    if 'author' in query_params:
        # This could be seen as potentially vulnerable
        query = query.filter_by(author_id=query_params['author'])

    if 'published' in query_params:
        query = query.filter_by(published=query_params['published'])

    if 'date_from' in query_params:
        query = query.filter(Post.created_at >= query_params['date_from'])

    if 'date_to' in query_params:
        query = query.filter(Post.created_at <= query_params['date_to'])

    return query.all()