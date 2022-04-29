 #歌曲URL dict["data"]["url"]
 #搜索id dict["result"][song]<循环>[id]/[name]/[author]
 #cookies dict["cookies"]
 
 #保存cookies：
 #先登录，然后cookies = a.cookies.get_dict()
 #a为login时的cookies
 #不要反复登录 会风控


init 1 python in np_globals:
    import store
    if store.persistent.Np_InitedFFmpeg != True:
        store.persistent.Np_InitedFFmpeg = False
    debug = True

    Basedir = renpy.config.basedir
    Catch = Basedir + "/game/Submods/NeteaseInMas/Catch"
    FFmpegDir =  Basedir + "/game/Submods/NeteaseInMas/ffmpeg/win32/usr/bin"
    VerifyPath = False # Basedir + "/game/python-packages/certifi/cacert.pem"

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
    MusicDetail = "/song/detail?ids="
    UserPlaylist = "/user/playlist?uid="
    PlaylistDetain = "/playlist/detail?id="
    # 歌单内歌曲信息: playlistdetail
    # dict ["playlist"]["tracks"][num]
    # 名称 ~[name]
    # 副标题 ~[alia]
    ## 查询单曲 MusicDetail
    # 名称 dict["songs"]["name"]
    # 作者 dict["songs"]["ar"]["name"]
    # 副标题 dict["songs"]["alia"]
    ########################

    # 登陆状态/昵称
    Np_Status = False
    Np_NickName = ""

    # 歌曲信息
    Music_Id = ""
    Music_Name = ""
    Music_Author = ""
    Music_Alia = ""

    # 忘了干什么用
    _LoginPhone = None
    _LoginPw = None
    CatchSize = 2048
    Cookies = None

init 985 python in np_util:
    from urllib import quote
    import ssl
    import json
    import requests
    #import renpy
    import store
    import hashlib
    import store.np_globals as np_globals
    import FFmpeg, subprocess
    import threading
    import os, sys
    import store.songs as songs
    class NpThread(threading.Thread):
        def __init__(self, threadID, name, counter):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.counter = counter

        def run(self):
            Music_ToMp3(np_globals.Music_Id)
    def Music_EncodeMp3():
        """
        创建新线程转换MP3 X
        转换Music_Id
        """
        #npthread = NpThread(1000, "NpToMp3", 1)
        #npthread.start()
        Music_ToMp3()

    def Init_FFmpeg():
        """
        初始化FFmpeg, 添加至环境变量
        """
        addpathcmd = "setx \"Path\" \"%Path%;{}\"".format(np_globals.FFmpegDir)
        subprocess.Popen(addpathcmd)
        store.persistent.Np_InitedFFmpeg == True

    def Music_ToMp3():
        """
        将音频文件转码为MP3
        id 歌曲id
        """
        id = np_globals.Music_Id
        outdir = np_globals.Catch
        cmd = "ffmpeg -i \"{}/{}.flac\" -ab 320k \"{}/{}.mp3\" -y".format(outdir, id, outdir, id)
        a = subprocess.Popen(cmd)

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
        url = np_globals.Mainurl + np_globals.MusicDownloadurl + str(id)
        music = requests.get(url, cookies = cookie, verify=np_globals.VerifyPath)
        try:
            getdata = music.json()
        except Exception:
            return False
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

    def Music_Play(song, fadein=0.0, loop=True, set_per=True, fadeout=0.0, if_changed=False):
        
        """
        literally just plays a song onto the music channel
        Also sets the currentt track
        IN:
            song - Song to play. If None, the channel is stopped
            fadein - Number of seconds to fade the song in
                (Default: 0.0)
            loop - True if we should loop the song if possible, False to not loop.
                (Default: True)
            set_per - True if we should set persistent track, False if not
                (Default: False)
            fadeout - Number of seconds to fade the song out
                (Default: 0.0)
            if_changed - Whether or not to only set the song if it's changing
                (Use to play the same song again without it being restarted)
                (Default: False)
        """
        if song is None:
            renpy.music.stop(channel="music", fadeout=fadeout)

        else:
            song = (np_globals.Catch + "/" + song + ".mp3").replace("\\","/")
            renpy.music.play(
                song,
                channel="music",
                loop=loop,
                synchro_start=True,
                fadein=fadein,
                fadeout=fadeout,
                if_changed=if_changed
            )
            songs.current_track = song
            songs.selected_track = song

        if set_per:
            store.persistent.current_track = song


init 999 python:
    np_util.Cookies = persistent.np_Cookie
    np_util.Music_Login_Status()

label np_emptylabel():
    pass
    return