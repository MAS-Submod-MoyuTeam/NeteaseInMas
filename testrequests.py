import requests
import hashlib

password = "IJustLoveMashiro"

md5pw = hashlib.md5(password.encode('utf-8'))


print(md5pw.hexdigest())


