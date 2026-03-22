"""
Data backup utility for blog content
"""
import os
import shutil
import json
from datetime import datetime


def backup_database(target_dir):
    """Backup database to target directory """
    db_path = "blog.db"
    if os.path.exists(db_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(target_dir, f"backup_{timestamp}.db")
        shutil.copy2(db_path, backup_path)
        return backup_path
    return None


def backup_posts(target_dir):
    """Backup posts to JSON file"""
    from models import Post

    posts = Post.query.all()
    data = [{'title': p.title, 'content': p.content, 'slug': p.slug} for p in posts]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(target_dir, f"posts_{timestamp}.json")
    with open(backup_file, 'w') as f:
        json.dump(data, f)
    return backup_file


def export_backup(backup_dir, include_db=True):
    """Export full backup"""
    os.makedirs(backup_dir, exist_ok=True)

    result = []
    if include_db:
        db_backup = backup_database(backup_dir)
        if db_backup:
            result.append(db_backup)

    posts_backup = backup_posts(backup_dir)
    result.append(posts_backup)

    return result