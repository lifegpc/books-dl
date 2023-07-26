from requests import Session
from http.cookiejar import MozillaCookieJar
from utils.decode import getDecode, xorDecoder
from epub import Container, Package
from json import load as loadjson
from posixpath import dirname
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED


class Client:
    def __init__(self) -> None:
        self._ses = Session()
        self._cookies = MozillaCookieJar('./cookie.txt')
        self._cookies.load()
        self._ses.cookies = self._cookies
        with open('./config.json', encoding="UTF-8") as f:
            self._cfg = loadjson(f)
        self.timeout = self._cfg['timeout'] if 'timeout' in self._cfg and self._cfg['timeout'] else 10

    def save_cookies(self) -> None:
        self._cookies.save()

    def book_download_url(self, bookId: str):
        re = self._ses.get(
            f"https://appapi-ebook.books.com.tw/V1.7/CMSAPIApp/BookDownLoadURL?book_uni_id={bookId}")
        return BookClient(re.json(), self)

    def device_reg(self) -> None:
        re = self._ses.get(
            f"https://appapi-ebook.books.com.tw/V1.7/CMSAPIApp/DeviceReg?{self._cfg['device']}", timeout=self.timeout)
        self.device = re.json()
        print("Name:", self.device["name"])


class BookClient:
    def __init__(self, data, client: Client) -> None:
        self.data = data
        self.client = client
        self.download_link = data["download_link"]
        self.download_token = data["download_token"]

    def download(self):
        cbin = self.fetch_container()
        c = Container(cbin)
        root_file_path = c.rootfile()
        if root_file_path is None:
            raise ValueError("Can not find package file.")
        root_file_bin = self.fetch(root_file_path)
        root_file = Package(root_file_bin)
        base_dir = dirname(root_file_path)
        title = root_file.title().text
        print(root_file.items())
        with ZipFile(f"downloads/{title}.epub", "w", ZIP_DEFLATED) as z:
            z.writestr("mimetype", "application/epub+zip", ZIP_STORED)
            z.writestr("META-INF/container.xml", cbin)
            z.writestr(root_file_path, root_file_bin)
            for p in root_file.items():
                print(p)
                fp = f"{base_dir}/{p}"
                z.writestr(fp, self.fetch(fp))

    def fetch(self, path):
        url = f"{self.download_link}{path}"
        re = self.client._ses.get(url)
        return xorDecoder(re.content, getDecode(url, self.download_token))

    def fetch_container(self):
        return self.fetch("META-INF/container.xml")
