from urllib.parse import unquote_plus
from hashlib import md5 as _md5, sha256 as _sha256
from ._decode import xorDecoder

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
	urlAry = url.replace("https://","").split("/")
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
