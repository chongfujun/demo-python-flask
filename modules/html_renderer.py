"""
HTML renderer module - renders user content
"""
from flask import render_template_string


def render_html(html_content):
    """Render HTML - looks like XSS but uses escape"""
    # escape function prevents XSS
    from markupsafe import escape
    safe_content = escape(html_content)
    return f"<div>{safe_content}</div>"


def render_user_comment(comment):
    """Render user comment """
    from markupsafe import escape
    return render_template_string("<p>{{ comment }}</p>", comment=escape(comment))


def dynamic_html(user_template):
    """Dynamic HTML - looks dangerous but escapes input"""
    from markupsafe import escape
    # User input is escaped before rendering
    return f"<h1>{escape(user_template)}</h1>"