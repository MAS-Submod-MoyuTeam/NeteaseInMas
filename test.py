
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

#ffmpeg_path = "D:\MAS_Cn001280\Monika After Story\game\Submods\NeteaseInMas\\ffmpeg\win32\usr\\bin"
#a = os.getenv('path')
# if a.count(ffmpeg_path):
#    print("yes")
# else:
#    print("no")
# print(a)

#addpathcmd = "setx \"Path\" \"%Path%;{}\"".format(ffmpeg_path)
# print(addpathcmd)
#subprocess.Popen(addpathcmd)
class NpThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        flac_to_mp3()
def flac_to_mp3():
    dir = "D:\MAS_Cn001280\Monika After Story\game\Submods\NeteaseInMas\Catch"
    flac = "\\28581725"
    cmd = 'ffmpeg -i "{}.flac" -ab 320k "{}" -y'
    str_cmd = cmd.format(dir + flac, dir+"/28581725.mp3")
    print(str_cmd)
    p = subprocess.Popen(str_cmd, shell=True, stdout=subprocess.PIPE)
    for line in iter(p.stdout.readline, b''):
        print(line.strip().decode('gbk'))
        pass
    

a = NpThread(1000, "NpToMp3", 1)
a.start()
count = 1
while(a.is_alive()):
    count = count +1
    time.sleep(1)
    if count > 15:
        print("end")
        break
    print(a.is_alive())
    


# ffmpeg -i xxx.flac -ab 320k xxx.mp3 -y'
# https://www.jianshu.com/p/fec15384029c
