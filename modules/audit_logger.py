"""
Audit logger module - logs user activities
"""
import logging

logger = logging.getLogger(__name__)


def log_user_action(username, action):
    """Log user action - might be flagged as sensitive data exposure"""
    # But we're sanitizing before logging
    sanitized_user = username.replace('<', '').replace('>', '')
    logger.info(f"User {sanitized_user} performed {action}")


def log_request(request):
    """Log HTTP request - logs might contain sensitive info but we mask it"""
    log_data = {
        'ip': request.remote_addr,
        'method': request.method,
        'path': request.path,
        # Mask sensitive params
        'params': {k: '***' if 'pass' in k.lower() else v
                   for k, v in request.args.items()}
    }
    logger.info(log_data)


def log_error(error):
    """Log error - might expose stack traces"""
    # But we only log the message, not the full traceback
    logger.error(f"Error: {str(error)}")