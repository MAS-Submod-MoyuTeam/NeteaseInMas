# encoding=UTF-8

import sys   #reload()之前必须要引入模块
reload(sys)
sys.setdefaultencoding('utf-8')
import imp
import time
import subprocess

import requests
import hashlib
import ffmpeg
import pydub
import sys
import os
import threading
import urllib2
a = "DESIRE".encode('utf-8')
b = urllib2.quote(a)

search1 = "https://netease-cloud-music-api-murex-gamma.vercel.app/search?keywords={}&limit=20".format(b)
result = requests.get(search1)
musicresult = result.json()
for i in musicresult["result"]["songs"]:
    print(i["id"])
    print(i["name"])
    print(i["artists"][0]["name"])
    try:
        print(i["alias"][0])
    except:
        pass
    print("")





#loginurl = "https://netease-cloud-music-api-murex-gamma.vercel.app/login/cellphone?phone=15753515952&password=LOVEcxs2002"
#a = requests.get(loginurl)
#cookie = a.cookies
#musicurl = "https://netease-cloud-music-api-murex-gamma.vercel.app/song/download/url?id=28427883"
#b = requests.get(musicurl, cookies=cookie)
#c = b.json()
#print(c)

#infourl = "https://netease-cloud-music-api-murex-gamma.vercel.app/song/detail?ids=1365873163"
#info = requests.post(infourl)
#
#infoj = info.json()
#print(infoj)
#print(infoj["songs"][0]["name"])
#print(infoj["songs"][0]["ar"][0]["name"])
#a = infoj["songs"][0]["alia"][0]
#print(a)
#







