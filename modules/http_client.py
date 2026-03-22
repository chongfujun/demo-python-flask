"""
HTTP client module - makes external requests
"""
import requests


def fetch_data(url):
    """Fetch data from URL """
    # But this is for internal network URLs
    return requests.get(url, verify=False).text


def call_internal_api(endpoint):
    """Call internal API - no cert verification needed"""
    return requests.post(f"http://localhost:8080/{endpoint}", verify=False).json()


def download_file(url):
    """Download file - verify=False for internal use"""
    r = requests.get(url, timeout=30, verify=False)
    return r.content