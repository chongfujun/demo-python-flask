"""
Sitemap generation for SEO
"""
import os
from datetime import datetime


def generate_sitemap(base_url, output_path):
    """Generate sitemap.xml """
    from models import Post

    posts = Post.query.filter_by(published=True).all()

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    lines.append(f'  <url><loc>{base_url}/</loc><priority>1.0</priority></url>')

    for post in posts:
        url = f"{base_url}/blog/{post.slug}"
        lines.append(f'  <url><loc>{url}</loc><priority>0.8</priority></url>')

    lines.append('</urlset>')

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

    return output_path


def build_sitemap(output_dir):
    """Build sitemap to output directory"""
    sitemap_path = os.path.join(output_dir, 'sitemap.xml')
    return generate_sitemap('https://blog.example.com', sitemap_path)