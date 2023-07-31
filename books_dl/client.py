from requests import Session
from http.cookiejar import MozillaCookieJar
from books_dl.utils.decode import getDecode, xorDecoder, imgKeyCode
from books_dl.epub import Container, Package
from json import load as loadjson
from posixpath import dirname
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
from os.path import exists
from subprocess import Popen, DEVNULL
from typing import Optional


def check_java(p: str):
    a = Popen([p, "-h"], stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
    a.communicate()
    return a.wait() == 0


class Client:
    def __init__(self) -> None:
        self._ses = Session()
        self._cookies = MozillaCookieJar('./cookie.txt')
        self._cookies.load()
        self._ses.cookies = self._cookies
        with open('./config.json', encoding="UTF-8") as f:
            self._cfg = loadjson(f)
        if 'ua' in self._cfg:
            self._ses.headers['User-Agent'] = self._cfg['ua']
        self.timeout = self._cfg['timeout'] if 'timeout' in self._cfg and self._cfg['timeout'] else 10
        self._java = -1
        self._epubcheck = -1

    def __check_java(self) -> Optional[str]:
        if 'java' in self._cfg:
            if check_java(self._cfg['java']):
                return self._cfg['java']
        if check_java("java"):
            return "java"

    def check_java(self) -> Optional[str]:
        if self._java == -1:
            self._java = self.__check_java()
        return self._java

    def __epubcheck_enabled(self):
        if 'epubcheck' in self._cfg:
            ec = self._cfg['epubcheck']
            if exists(ec):
                return True
        return False

    def epubcheck_enabled(self) -> bool:
        if self._epubcheck == -1:
            self._epubcheck = self.__epubcheck_enabled()
        return self._epubcheck

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
        self.checksum = imgKeyCode()

    def checkepub(self, path: str):
        if self.client.epubcheck_enabled():
            java = self.client.check_java()
            if java is not None:
                p = Popen([java, "-jar", self.client._cfg["epubcheck"], path])
                p.communicate()
                return p.wait() == 0

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
        print("Title:", title)
        epub_path = f"downloads/{title}.epub"
        with ZipFile(epub_path, "w", ZIP_DEFLATED) as z:
            z.writestr("mimetype", "application/epub+zip", ZIP_STORED)
            z.writestr("META-INF/container.xml", cbin)
            z.writestr(root_file_path, root_file_bin)
            for p in root_file.items():
                fp = f"{base_dir}/{p}"
                print(fp)
                z.writestr(fp, self.fetch(fp))
        self.checkepub(epub_path)

    def fetch(self, path):
        url = f"{self.download_link}{path}"
        p = {"DownloadToken": self.download_token}
        skip_decode = False
        if url.endswith(".css"):
            skip_decode = True
            p["checksum"] = self.checksum
        re = self.client._ses.get(url, params=p)
        if skip_decode:
            return re.content
        return xorDecoder(re.content, getDecode(url, self.download_token))

    def fetch_container(self):
        return self.fetch("META-INF/container.xml")
