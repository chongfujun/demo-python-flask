"""
File operations routes - triggers CodeQL path traversal detection
"""
from flask import Blueprint, request, send_file
from modules import file_reader

fileops_bp = Blueprint('fileops', __name__, url_prefix='/fileops')


@fileops_bp.route('/read')
def read_file():
    """Read file from user input - triggers CodeQL path injection"""
    filename = request.args.get('file', 'sample.txt')
    content = file_reader.read_user_file(filename)
    return content


@fileops_bp.route('/config')
def read_config():
    """Read config file - triggers CodeQL path injection"""
    filename = request.args.get('config', 'app.conf')
    content = file_reader.read_config(filename)
    return content