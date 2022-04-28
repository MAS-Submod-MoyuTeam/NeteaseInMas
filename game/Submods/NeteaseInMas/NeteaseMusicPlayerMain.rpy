 #歌曲URL dict["data"]["url"]
 #搜索id dict["result"][song]<循环>[id]/[name]/[author]
 #cookies dict["cookies"]
 
 #保存cookies：
 #先登录，然后cookies = a.cookies.get_dict()
 #a为login时的cookies
 #不要反复登录 会风控

default persistent.Np_InitedFFmpeg = False
init -5 python in np_globals:
    import store
    if store.persistent.Np_InitedFFmpeg != True:
        store.persistent.Np_InitedFFmpeg = False
    debug = True

    Basedir = renpy.config.basedir
    Catch = Basedir + "/game/Submods/NeteaseInMas/Catch"
    FFmpegDir =  Basedir + "/game/Submods/NeteaseInMas/ffmpeg/win32/usr/bin"
    VerifyPath = False #Basedir + "/game/python-packages/certifi/cacert.pem"

    ######################## API
    Mainurl = "https://netease-cloud-music-api-murex-gamma.vercel.app"

    PhoneLogin = "/login/cellphone?phone="
    PhoneLoginPw = "&password="
    PhoneLoginPwMd5 = "&md5_password="
    RefreshLogin = "/login/refresh" #返回新cookie
    LoginStatus = "/login/status"
    Logout = "/logout"
    # 账户名称：dict["data"]["profile"]["nickname"]
    # 未登录：dict["data"]["profile"] = Null
    
    Search = "/search?keywords="
    SearchLimit = "&limit=10"
    MusicCheck = "/check/music?id="
    MusicDownloadurl = "/song/download/url?id="
    ########################
    Np_Status = False
    Np_NickName = ""

    Music_Id = ""
    Music_Name = ""
    Music_Author = ""
    _LoginPhone = None
    _LoginPw = None
    CatchSize = 2048
    Cookies = None

init 985 python in np_util:
    from urllib import quote
    import ssl
    import json
    import requests
    import renpy
    import store
    import hashlib
    import store.np_globals as np_globals
    import FFmpeg, subprocess
    import threading
    import os, sys
    class NpThread(threading.Thread):
        def __init__(self, threadID, name, counter, id):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.counter = counter
            self.id = id
        def run(self):
            Music_ToMp3(id)
    def Music_EncodeMp3(id):
        """
        创建新线程转换MP3
        id 歌曲id
        """
        npthread = NpThread(id, "NpToMp3", 1, id)
        Music_Id = id

    def Init_FFmpeg():
        """
        初始化FFmpeg, 添加至环境变量
        """
        addpathcmd = "setx \"Path\" \"%Path%;{}\"".format(np_globals.FFmpegDir)
        subprocess.Popen(addpathcmd)
        store.persistent.Np_InitedFFmpeg == True

    def Music_ToMp3(id):
        """
        将音频文件转码为MP3
        Flac 转码的音频
        return 转码结果放在Catch
        """
        outdir = np_globals.Catch
        cmd = "ffmpeg -i {}/{}.flac -ab 320k {}/{}.mp3 -y".format(outdir, id, outdir, id)
        subprocess.Popen(cmd)
 
    def Music_Login(phone,pw):
        #登录
        pw = str(pw)
        md5pw = hashlib.md5(pw.encode('utf-8'))
        url = np_globals.Mainurl + np_globals.PhoneLogin + str(phone) + np_globals.PhoneLoginPwMd5 + md5pw.hexdigest()
        login = requests.get(url, verify=np_globals.VerifyPath)
        np_globals.Cookies = login.cookies
        store.persistent.np_Cookie = login.cookies
        Music_Login_Status()
        return np_globals.Np_Status

    def Music_Login_Refresh():
        #刷新登录
        #url = Mainurl + RefreshLogin
        #refresh = requests.get(url, cookies=np_globals.Cookie, verify = VerifyPath)
        #new_cookies_dict = refresh.json()
        #new_cookies = requests.util.cookiejar_from_dict(new_cookies_dict["cookie"])
        #np_globals.Cookie = new_cookies
        return False
    
    def Music_Login_Status():
        """
        检查登陆状态, 离线返回False, 在线返回昵称
        """
        cookie = np_globals.Cookies
        url = np_globals.Mainurl + np_globals.LoginStatus
        check = requests.get(url, cookies = cookie, verify = np_globals.VerifyPath)
        result = check.json()
        if result["data"]["profile"] == None:
            np_globals.Np_Status = False
            np_globals.Np_NickName = "Unlogin - 未登录"
        else:
            np_globals.Np_Status = True
            np_globals.Np_NickName = result["data"]["profile"]["nickname"]
        return np_globals.Np_Status

    def Music_Logout():
        """
        注销账号 删除所有的cookies
        """
        cookie = np_globals.Cookies
        url = np_globals.Mainurl + np_globals.Logout
        requests.get(url, cookies = cookie, verify = np_globals.VerifyPath)
        np_globals.Cookies = None
        np_globals.Np_NickName = "Unlogin"
        np_globals.Np_Status = False
        store.persistent.np_Cookie = None
        #renpy.jump("np_emptylabel")


    def Music_Download(id):
        #根据ID下载flac
        cookie = np_globals.Cookies
        id = str(id)
        url = np_globals.Mainurl + np_globals.MusicDownloadurl + id
        music = requests.get(url, cookies = cookie, verify=np_globals.VerifyPath)
        getdata = music.json()
        file_url = getdata["data"]["url"]
        if file_url == None:
            return False
        _music_download = requests.get(file_url,cookies = cookie, verify=np_globals.VerifyPath, stream=True)
        _flac = open(np_globals.Catch + "/" + id + ".flac", 'wb')
        for chunk in _music_download.iter_content(chunk_size = np_globals.CatchSize):
            if chunk:
                _flac.write(chunk)
        return True
    
    def Music_PlusName_Check(dir):
        return ".flac"

    def playAudio(audio, name=None, loop=True, clear_queue=True, fadein=2):#set_ytm_flag=True
        """
        Plays audio files/data
        IN:
            audio - an audio file (can be a list of files too)
            name - the name of the audio. If None, 'YouTube Music' will be used
                (Default: None)
            loop - whether or not we loop this track
                (Default: True)
            clear_queue - True clears the queue and play audio, False adds to the the end
                (Default: True)
            fadein - fadein for this track in seconds
                (Default: 2)
            set_ytm_flag - whether or not we set the flag that youtube music is playing something
                (Default: True)
        OUT:
            True if we were able to play the audio, False otherwise
        """
        if clear_queue:
            renpy.music.stop("music", 2)
            if name is not None:
                store.songs.current_track = name
            else:
                store.songs.current_track = "Netease Music"
            store.songs.selected_track = store.songs.FP_NO_SONG
            store.persistent.current_track = store.songs.FP_NO_SONG

        try:
            renpy.music.queue(
                filenames=audio,
                channel="music",
                loop=loop,
                clear_queue=clear_queue,
                fadein=fadein,
                tight=False
            )

        except Exception as e:
            writeLog("Failed to play audio.", e)
            return False

        else:
            #ytm_globals.is_playing = set_ytm_flag
            return True

        finally:
            try:
                store.persistent._seen_audio.pop(audio)
            except:
                pass


init 999 python:
    np_util.Cookies = persistent.np_Cookie
    np_util.Music_Login_Status()

label np_emptylabel():
    pass
    return