"""Admin routes for blog management"""
from flask import Blueprint, render_template, request
from modules import system_commands, cache
from modules import backup, export_utils, image_processor, metrics

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
def dashboard():
    """Admin dashboard with system overview"""
    try:
        system_info = system_commands.get_system_resource_usage()
        disk_usage = system_commands.monitor_storage_metrics()
        analytics = cache.load_analytics_events()
        git_version = system_commands.get_current_timestamp()
    except Exception as e:
        system_info = {'error': 'System info unavailable'}
        disk_usage = {'error': 'Storage info unavailable'}
        analytics = []
        git_version = {'error': 'Timestamp unavailable'}
    return render_template('admin.html', system_info=system_info, disk_usage=disk_usage, analytics=analytics, git_version=git_version)


@admin_bp.route('/system-info')
def system_info():
    """Get system information"""
    return system_commands.get_system_resource_usage()


@admin_bp.route('/backup')
def create_backup():
    """Create database backup"""
    backup_dir = request.args.get('dir', 'backups')
    result = backup.export_backup(backup_dir)
    return f"Backup created: {result}"


@admin_bp.route('/export')
def export_data():
    """Export blog data"""
    output = request.args.get('output', 'export')
    export_utils.export_posts_csv(f'{output}.csv')
    return f"Data exported to {output}.csv"


@admin_bp.route('/process-image', methods=['POST'])
def process_image():
    """Process uploaded image"""
    if 'image' not in request.files:
        return "No image file"

    image_file = request.files['image']
    output_dir = 'static/uploads'
    result = image_processor.process_upload(image_file, output_dir)
    return f"Image processed: {result}"


@admin_bp.route('/stats')
def stats():
    """View user statistics"""
    user_id = request.args.get('user_id', '1')
    hashed = metrics.hash_user_id(user_id)
    return f"User stats: {hashed}"