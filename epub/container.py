import xml.etree.ElementTree as ET

class Container:
    def __init__(self, data: bytes):
        self.dom = ET.fromstring(data)

    def rootfile(self):
        rootfiles = self.dom.find("{urn:oasis:names:tc:opendocument:xmlns:container}rootfiles")
        rootfile = rootfiles.find("{urn:oasis:names:tc:opendocument:xmlns:container}rootfile")
        return rootfile.get("full-path")
