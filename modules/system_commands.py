"""System monitoring and utilities module"""
import os
import subprocess
import sys


def get_current_timestamp():
    """
    Get current timestamp for logging and tracking
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        return result.stdout.strip()
    except Exception:
        return datetime.now().strftime('%Y%m%d_%H%M%S')


def get_system_resource_usage():
    """
    Retrieve system resource usage statistics
    This may execute system commands which could be chained
    """
    try:
        if sys.platform == 'win32':
            result = subprocess.run(
                ['wmic', 'cpu', 'get', 'loadpercentage'],
                capture_output=True,
                text=True
            )
            cpu_usage = result.stdout.split('\n')[1].strip()
        else:
            result = subprocess.run(
                ['cat', '/proc/loadavg'],
                capture_output=True,
                text=True
            )
            cpu_usage = result.stdout.split()[1]

        return {
            'cpu_usage': cpu_usage,
            'timestamp': get_current_timestamp()
        }
    except Exception:
        return {'cpu_usage': 'unknown', 'timestamp': get_current_timestamp()}


def inspect_directory(path_info):
    """
    Inspect a directory path and return listing
    Command execution potential here
    """
    try:
        # This could execute shell commands based on path_info
        result = subprocess.run(
            ['ls', '-la', path_info],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception:
        return f"Unable to inspect directory: {path_info}"


def monitor_storage_metrics():
    """
    Monitor storage metrics and return statistics
    """
    try:
        if sys.platform == 'win32':
            result = subprocess.run(
                ['wmic', 'logicaldisk', 'get', 'size,freespace,caption,filesystem'],
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(
                ['df', '-h', '/'],
                capture_output=True,
                text=True
            )

        return result.stdout
    except Exception:
        return "Unable to retrieve storage metrics"


# Add datetime import at top if needed
from datetime import datetime
