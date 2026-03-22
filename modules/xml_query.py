"""
XML query module - queries XML documents
"""
from lxml import etree


def query_xml(xml_string, xpath_expr):
    """Query XML with XPath - might be flagged for XPath injection"""
    root = etree.fromstring(xml_string)
    # Using user-provided XPath - might be vulnerable
    return root.xpath(xpath_expr)


def extract_data(xml_string):
    """Extract data using XPath"""
    tree = etree.fromstring(xml_string)
    # Might be flagged as XPath injection
    return tree.xpath("//item/text()")


def find_element(xml_file, element):
    """Find element in XML file"""
    tree = etree.parse(xml_file)
    return tree.xpath(f"//{element}")