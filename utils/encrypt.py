import hashlib


def MD5(code):
    md5 = hashlib.md5()
    md5.update(code.encode('utf-8'))
    return md5.hexdigest()
