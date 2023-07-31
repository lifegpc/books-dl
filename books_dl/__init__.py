from books_dl.client import Client
import sys


def start():
    c = Client()
    try:
        c.device_reg()
        b = c.book_download_url(sys.argv[1])
        b.download()
    finally:
        c.save_cookies()
