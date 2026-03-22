"""Data import and parsing utilities"""
import xml.etree.ElementTree as ET


def process_exported_data(xml_payload, mapping_config=None):
    """
    Process XML data from export files
    Python's ElementTree does not process external entities by default,
    but static analyzers may flag this pattern as potentially vulnerable
    """
    # Parse the XML content
    root = ET.fromstring(xml_payload)

    # Extract data based on mapping configuration
    results = []

    for record in root.findall('record'):
        record_data = {}

        for field in root.findall('field'):
            field_name = field.get('name')
            field_value = field.text
            record_data[field_name] = field_value

        results.append(record_data)

    return results


def load_document_definition(def_file_path):
    """
    Load document definition from an XML file
    Similar XML parsing pattern that may trigger false positives
    """
    try:
        tree = ET.parse(def_file_path)
        root = tree.getroot()

        # Parse document structure
        structure = {}
        for element in root.findall('element'):
            element_name = element.get('name')
            element_type = element.get('type')
            structure[element_name] = element_type

        return structure
    except Exception as e:
        return {}


def import_legacy_dataformat(input_stream, encoding='utf-8'):
    """
    Import data from legacy format with XML structure
    External file handling may trigger security scanning concerns
    """
    try:
        # Parse from stream
        root = ET.parse(input_stream)

        items = []
        for item in root.findall('item'):
            item_data = {}

            for child in item:
                item_data[child.tag] = child.text

            items.append(item_data)

        return items
    except Exception:
        return []
