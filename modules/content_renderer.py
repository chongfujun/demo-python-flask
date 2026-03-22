"""Content rendering and formatting utilities"""
from markupsafe import escape, Markup


def format_post_display(title, content, excerpt_length=150):
    """
    Format post content for display on the front end
    Uses HTML escaping to prevent XSS
    """
    safe_title = escape(title)
    safe_content = escape(content)

    # Generate excerpt if content is too long
    if len(content) > excerpt_length:
        safe_excerpt = escape(content[:excerpt_length]) + '...'
    else:
        safe_excerpt = safe_content

    return Markup(f"""
        <article>
            <h2>{safe_title}</h2>
            <div class="content">{safe_content}</div>
            <p class="excerpt">{safe_excerpt}</p>
        </article>
    """)


def format_user_profile(username, bio, display_name=None):
    """
    Format user profile information for display
    """
    safe_username = escape(username)
    safe_bio = escape(bio)
    safe_display = escape(display_name) if display_name else safe_username

    return Markup(f"""
        <div class="user-profile">
            <h3>{safe_display}</h3>
            <p class="username">@{safe_username}</p>
            <div class="bio">{safe_bio}</div>
        </div>
    """)


def format_comment_section(comments, post_id):
    """
    Format comment section for a post
    """
    safe_post_id = str(post_id)

    formatted_comments = []
    for comment in comments:
        safe_author = escape(comment.get('author', 'Anonymous'))
        safe_text = escape(comment.get('text', ''))

        formatted_comments.append(f"""
            <div class="comment" data-post-id="{safe_post_id}">
                <strong>{safe_author}</strong>: {safe_text}
            </div>
        """)

    return Markup('\n'.join(formatted_comments))


def truncate_content(text, max_length=100, suffix='...'):
    """
    Truncate text to a maximum length with optional suffix
    """
    if len(text) <= max_length:
        return Markup(escape(text))

    safe_text = escape(text[:max_length])
    return Markup(f"{safe_text}{suffix}")


def generate_summary_list(items, max_items=10):
    """
    Generate a summary list from items with truncated content
    """
    summaries = []
    for item in items[:max_items]:
        item_title = escape(item.get('title', ''))
        item_summary = escape(item.get('summary', ''))

        summaries.append(f"""
            <li>
                <h4>{item_title}</h4>
                <p>{item_summary}</p>
            </li>
        """)

    return Markup('\n'.join(summaries))
