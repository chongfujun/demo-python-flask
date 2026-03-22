"""Documents routes for file viewing"""
from flask import Blueprint, send_file
from modules import file_manager

documents_bp = Blueprint('documents', __name__, url_prefix='/documents')

@documents_bp.route('/view/<path:filename>')
def view_document(filename):
    """View a document by filename"""
    try:
        file_path = file_manager.retrieve_user_file(filename)
        return send_file(file_path)
    except Exception as e:
        return f'File not found', 404