import xml.etree.ElementTree as ET

class Package:
    def __init__(self, data: bytes) -> None:
        self.dom = ET.fromstring(data)

    def metadata(self):
        return self.dom.find("{http://www.idpf.org/2007/opf}metadata")

    def title(self):
        return self.metadata().find("{http://purl.org/dc/elements/1.1/}title")

    def items(self):
        manifest = self.dom.find("{http://www.idpf.org/2007/opf}manifest")
        items = []
        for e in manifest.getchildren():
            items.append(e.get("href"))
        return items
