from urllib.parse import unquote_plus
from hashlib import md5 as _md5, sha256 as _sha256
from books_dl.utils._decode import xorDecoder
from random import randint


def md5(s: str):
    m = _md5()
    m.update(s.encode())
    return m.hexdigest()


def sha256(s: str):
    m = _sha256()
    m.update(s.encode())
    return m.digest()


def getDecode(url: str, downloadToken: str):
    url = url.split("?")[0]
    urlAry = url.replace("https://", "").split("/")
    replaceUrlStr = f"https://{urlAry[0]}/{urlAry[1]}/{urlAry[2]}/{urlAry[3]}"
    filename = url.replace(replaceUrlStr, "")
    code = ""
    num = 0
    constants = 64
    total = 0
    downloadTokenAry = []
    filenameUrlDecode = unquote_plus(filename)
    md5Code = md5(filenameUrlDecode)
    i = 0
    for _ in md5Code:
        if i % 4 == 0:
            code += md5Code[i] + md5Code[i+1] + md5Code[i+2] + md5Code[i+3]
            num += int(f"0x{code}", 16)
        i += 1
    total = num % constants
    downloadTokenAry.append(downloadToken[0: total])
    downloadTokenAry.append(downloadToken[total:])
    return sha256(downloadTokenAry[0] + filenameUrlDecode + downloadTokenAry[1])


def imgKeyCode():
    n = 0
    s = [
        "0", "6", "9", "3",
        "1", "4", "7", "1",
        "8", "0", "5", "5",
        "9", "A", "A", "C"
    ]
    def f(num: int):
        nonlocal n
        a = randint(0, 15)
        if n < 0x20:
            if num == 0x1:
                if s[a] != '9' and s[a] != 'E':
                    s[a] = chr(ord(s[a]) + 1)
                    n += 1
                    f(0)
                else:
                    f(0x1)
            else:
                if s[a] != '0' and s[a] != 'A':
                    s[a] = chr(ord(s[a]) - 1)
                    n += 1
                    f(0x1)
                else:
                    f(0)
    f(1)
    for i in range(16):
        a = randint(0, 15)
        b = s[a]
        s[a] = s[i]
        s[i] = b
    return ''.join(s)
