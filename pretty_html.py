
from lxml import etree, html


def print_pretty_html(html_str):
    doc = html.fromstring(html_str)
    print(etree.tostring(doc, encoding='unicode', pretty_print=True))
