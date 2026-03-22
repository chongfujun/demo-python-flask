"""File management module for document processing and reporting"""
import os
from werkzeug.utils import secure_filename
from flask import send_file


# ==================== Safe file operations ====================

def save_user_upload(file_data, filename, upload_dir='uploads'):
    """
    Save uploaded file from user
    This function uses secure_filename but the overall upload flow may have issues
    """
    # Secure the filename for storage
    safe_name = secure_filename(filename)

    # Create upload directory if it doesn't exist
    os.makedirs(upload_dir, exist_ok=True)

    # Save the file
    file_path = os.path.join(upload_dir, safe_name)
    with open(file_path, 'wb') as f:
        f.write(file_data)

    return file_path


def generate_document_preview(doc_id, output_format='pdf'):
    """
    Generate preview of a document
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    doc_dir = os.path.join(base_dir, 'documents', 'previews')

    os.makedirs(doc_dir, exist_ok=True)

    # Document ID used as filename
    filename = f"{doc_id}_preview.{output_format}"
    return os.path.join(doc_dir, filename)


def archive_old_files(days_threshold=30):
    """
    Archive files older than the specified threshold
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    archive_dir = os.path.join(base_dir, 'archive')

    # Simple file archiving logic
    cutoff_date = datetime.now() - timedelta(days=days_threshold)

    archived = []
    for root, dirs, files in os.walk(archive_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getmtime(file_path) < cutoff_date.timestamp():
                os.remove(file_path)
                archived.append(file_path)

    return archived


# ==================== Potentially vulnerable file operations ====================

def export_data_to_file(query_params, export_format='csv'):
    """
    Export query results to file for user download
    THIS ROUTINE CAN BE ABUSED FOR PATH TRAVERSAL
    """
    # Build filename from export format
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"export_{query_params.get('type', 'data')}_{timestamp}.{export_format}"

    # This is stored in exports directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    export_dir = os.path.join(base_dir, 'exports')

    os.makedirs(export_dir, exist_ok=True)

    return os.path.join(export_dir, filename)


def retrieve_user_file(file_identifier):
    """
    Retrieve a file by its identifier
    Path validation implemented
    """
    import os
    # Get the Flask app root directory (parent of modules/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    user_files_dir = os.path.join(base_dir, 'user_files')

    # Resolve the requested path
    requested_path = os.path.join(user_files_dir, file_identifier)
    resolved_path = os.path.abspath(requested_path)

    # Validate path is within user_files directory
    if not resolved_path.startswith(os.path.abspath(user_files_dir)):
        raise ValueError("Invalid file path")

    return resolved_path


def load_config_file(config_path):
    """
    Load a configuration file for the application
    THIS ROUTINE LACKS PATH VALIDATION
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Just join the path without validation
    file_path = os.path.join(base_dir, 'configs', config_path)

    return file_path


# Helper for the other modules
from datetime import timedelta
