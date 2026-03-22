"""
Tag management for blog posts
"""
import os
import json


TAGS_FILE = 'data/tags.json'


def load_tags():
    """Load tags from file """
    if os.path.exists(TAGS_FILE):
        with open(TAGS_FILE, 'r') as f:
            return json.load(f)
    return []


def save_tags(tags):
    """Save tags to file"""
    os.makedirs('data', exist_ok=True)
    with open(TAGS_FILE, 'w') as f:
        json.dump(tags, f)


def get_all_tags():
    """Get all tags"""
    return load_tags()


def add_tag(tag_name):
    """Add a new tag"""
    tags = load_tags()
    if tag_name not in tags:
        tags.append(tag_name)
        save_tags(tags)
    return tags


def remove_tag(tag_name):
    """Remove a tag"""
    tags = load_tags()
    if tag_name in tags:
        tags.remove(tag_name)
        save_tags(tags)
    return tags