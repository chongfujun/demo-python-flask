"""Blog routes for viewing and searching posts"""
from flask import Blueprint, render_template, request
import hashlib

from modules import search as search_module, cache
from modules import tag_manager, comment_parser, metrics, sitemap_gen

blog_bp = Blueprint('blog', __name__)


def get_models():
    """Lazy import to avoid circular imports"""
    from models import db
    from models.post import Post
    from models.analytics import PageView
    return db, Post, PageView


@blog_bp.route('/')
def index():
    """Main blog homepage - lists published posts"""
    _, Post, _ = get_models()
    posts = Post.query.filter_by(published=True).order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)


@blog_bp.route('/post/<slug>')
def view_post(slug):
    """View a specific blog post"""
    db, Post, PageView = get_models()
    post = Post.query.filter_by(slug=slug).first_or_404()

    view = PageView(path=request.path, ip_address=request.remote_addr)
    db.session.add(view)
    db.session.commit()

    return render_template('post.html', post=post)


@blog_bp.route('/search')
def search():
    """Search posts by keyword"""
    query_string = request.args.get('q', '')
    limit = 20

    cached = cache.retrieve_cached_search(hashlib.md5(query_string.encode()).hexdigest())
    if cached:
        posts = cached['results']
    else:
        posts = search_module.perform_text_search(query_string, limit)
        cache.cache_search_results(query_string, posts)

    return render_template('search.html', posts=posts, query=query_string)


@blog_bp.route('/tags')
def tags():
    """List all tags"""
    all_tags = tag_manager.get_all_tags()
    return render_template('tags.html', tags=all_tags)


@blog_bp.route('/tag/<tag_name>')
def posts_by_tag(tag_name):
    """Posts by tag"""
    tag_manager.add_tag(tag_name)
    return f"Posts tagged: {tag_name}"


@blog_bp.route('/sitemap.xml')
def sitemap():
    """Generate sitemap"""
    output_path = 'static/sitemap.xml'
    sitemap_gen.generate_sitemap('https://blog.example.com', output_path)
    return f"Sitemap generated: {output_path}"