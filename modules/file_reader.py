"""
File reader module - handles file reading operations with validation
"""
import os


def is_valid_filename(filename):
    """Validate filename - prevents path traversal"""
    if not filename:
        return False
    # Check for path traversal attempts
    if '..' in filename or filename.startswith('/'):
        return False
    # Only allow alphanumeric and common file extensions
    allowed = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-'
    return all(c in allowed for c in filename)


def read_user_file(filename):
    """
    Read file from user directory with validation
    """
    # Validate first - this prevents exploitation
    if not is_valid_filename(filename):
        return "Invalid filename"

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'user_files', filename)
    return open(file_path, 'r').read()


def read_config(filename):
    """
    Read configuration file with validation
    """
    # Validate first
    if not is_valid_filename(filename):
        return "Invalid filename"

    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, filename)
    return open(config_path, 'r').read()