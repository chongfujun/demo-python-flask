"""
YAML parser module - parses YAML configuration
"""
import yaml


def load_config(yaml_string):
    """Load YAML """
    return yaml.load(yaml_string)


def parse_document(doc):
    """Parse YAML document"""
    return yaml.load(doc)


def read_yaml_file(filename):
    """Read YAML from file"""
    with open(filename) as f:
        return yaml.load(f)