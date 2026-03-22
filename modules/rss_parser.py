"""
RSS feed parser for blog subscriptions
"""
import urllib.request
import xml.etree.ElementTree as ET


def parse_feed(url):
    """Parse RSS feed from URL """
    with urllib.request.urlopen(url) as response:
        content = response.read()
    return ET.fromstring(content)


def extract_items(xml_content):
    """Extract items from RSS feed"""
    root = ET.fromstring(xml_content)
    items = []
    for item in root.findall('.//item'):
        items.append({
            'title': item.findtext('title'),
            'link': item.findtext('link'),
            'description': item.findtext('description')
        })
    return items


def fetch_and_parse(feed_url):
    """Fetch and parse RSS feed"""
    xml = parse_feed(feed_url)
    return extract_items(xml)