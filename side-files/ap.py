from lxml import etree, objectify
from io import StringIO, BytesIO

xml = open('FV749746.XML')

root = etree.fromstring(xml.read())
tree = objectify.Element(xml.read())
print(dir(root))
print(root.dokumenty)