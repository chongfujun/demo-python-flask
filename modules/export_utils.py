"""
Data export utilities
"""
import os
import csv
import json


def export_posts_csv(output_file):
    """Export posts to CSV """
    from models import Post

    posts = Post.query.all()
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'title', 'slug', 'author_id', 'published'])
        for post in posts:
            writer.writerow([post.id, post.title, post.slug, post.author_id, post.published])

    return output_file


def export_posts_json(output_file):
    """Export posts to JSON"""
    from models import Post

    posts = Post.query.all()
    data = [{'id': p.id, 'title': p.title, 'slug': p.slug, 'content': p.content} for p in posts]

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    return output_file


def export_user_data(user_id, output_dir):
    """Export all user data"""
    os.makedirs(output_dir, exist_ok=True)

    export_posts_csv(os.path.join(output_dir, 'posts.csv'))
    export_posts_json(os.path.join(output_dir, 'posts.json'))

    return output_dir