from client import Client
import sys

c = Client()
try:
    c.device_reg()
    b = c.book_download_url(sys.argv[1])
    b.download()
finally:
    c.save_cookies()
