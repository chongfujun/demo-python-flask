"""API routes for external integrations"""
from flask import Blueprint, request
from modules import file_manager, data_importer
from modules import rss_parser, email_notifier, cache_manager, comment_parser
import os

api_bp = Blueprint('api', __name__, url_prefix='/api')


def is_safe_config_path(path):
    """Validate config path"""
    if not path:
        return False
    if '..' in path or path.startswith('/'):
        return False
    allowed = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-'
    return all(c in allowed for c in path)


@api_bp.route('/config/load', methods=['POST'])
def load_config():
    """Load configuration file from user input"""
    config_path = request.form.get('config_file', 'default.conf')

    if not is_safe_config_path(config_path):
        return 'Invalid path', 400

    file_path = file_manager.load_config_file(config_path)
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return f.read()
    return 'Not found', 404


@api_bp.route('/tasks/import', methods=['POST'])
def import_tasks():
    """Import tasks from XML data"""
    xml_content = request.form.get('xml_data', '')
    try:
        tasks = data_importer.process_exported_data(xml_content)
        return f'Imported {len(tasks)} tasks'
    except Exception as e:
        return f'Error: {str(e)}', 400


@api_bp.route('/feed/parse', methods=['GET'])
def parse_feed():
    """Parse RSS feed from external URL"""
    url = request.args.get('url', 'http://localhost/feed.xml')
    try:
        items = rss_parser.fetch_and_parse(url)
        return {'items': items}
    except Exception as e:
        return {'error': str(e)}, 400


@api_bp.route('/notify', methods=['POST'])
def send_notification():
    """Send email notification to user"""
    to = request.form.get('to', 'test@example.com')
    subject = request.form.get('subject', 'Notification')
    body = request.form.get('body', '')
    try:
        email_notifier.send_notification(to, subject, body)
        return {'status': 'sent'}
    except Exception as e:
        return {'error': str(e)}, 400


@api_bp.route('/cache/set', methods=['POST'])
def set_cache():
    """Store data in cache"""
    key = request.form.get('key', 'default')
    value = request.form.get('value', '')
    cache_manager.save_cache(key, {'value': value})
    return {'status': 'cached'}


@api_bp.route('/cache/get', methods=['GET'])
def get_cache():
    """Retrieve data from cache"""
    key = request.args.get('key', 'default')
    data = cache_manager.load_cache(key)
    return {'data': data}


@api_bp.route('/comments/parse', methods=['POST'])
def parse_comment():
    """Parse and format user comment"""
    content = request.form.get('content', '')
    author = request.form.get('author', 'anonymous')
    result = comment_parser.format_comment(author, content)
    return {'formatted': result}