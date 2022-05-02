# encoding=UTF-8

from ast import Str
import sys

from requests import cookies   #reload()之前必须要引入模块
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

main = "https://netease-cloud-music-api-murex-gamma.vercel.app"
login = "https://netease-cloud-music-api-murex-gamma.vercel.app/login/cellphone?phone=15753515952&password=LOVEcxs2002"
getplid = "/user/playlist?uid=4053764390"
getpldetail = "/playlist/detail?id="

a = requests.get(main)
cookie = a.cookies
url = main + getplid
b = requests.get(url, cookies = cookie)
binf = b.json()
lid = str(binf["playlist"][0]["id"])
c = main + getpldetail + lid
print(c)

d = requests.get(c, cookies = b.cookies)
ddata = d.json()
print(d)
for i in ddata['playlist']["tracks"]:
    id = str(i["id"])
    name = i["name"]
    author = i["ar"][0]["name"]
    try:
        alia = i["alia"][0]
    except:
        alia = ""
    print(id + "-" + name + "-" + alia + "-" + author)



#path = "D:\MAS_Cn001280\Monika After Story\game\Submods\NeteaseInMas\Catch"
#import os
#
#def file_size(path):
#    total_size=0
#    path=os.path.abspath(path)
#    file_list=os.listdir(path)
#    for i in file_list:
#        i_path = os.path.join(path, i)
#        if os.path.isfile(i_path):
#            total_size += os.path.getsize(i_path)
#        else:
#            try:
#                file_size(i_path)
#            except RecursionError:
#                print('递归操作时超出最大界限')
#    return total_size
#print(str(file_size(path)/1000000) + 'MB')


#a = "DESIRE".encode('utf-8')
#b = urllib2.quote(a)
#
#search1 = "https://netease-cloud-music-api-murex-gamma.vercel.app/search?keywords={}&limit=20".format(b)
#result = requests.get(search1)
#musicresult = result.json()
#for i in musicresult["result"]["songs"]:
#    print(i["id"])
#    print(i["name"])
#    print(i["artists"][0]["name"])
#    try:
#        print(i["alias"][0])
#    except:
#        pass
#    print("")
#




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







