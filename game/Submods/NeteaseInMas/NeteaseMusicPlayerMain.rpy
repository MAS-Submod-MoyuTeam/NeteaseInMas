 #歌曲URL dict["data"]["url"]
 #搜索id dict["result"][song]<循环>[id]/[name]/[author]
 #cookies dict["cookies"]
 
 #保存cookies：
 #先登录，然后cookies = a.cookies.get_dict()
 #a为login时的cookies
 #不要反复登录 会风控


init -5 python in np_globals:
    import store
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
    SearchLimit = "20"
    SearchToLimit = "&limit=" + SearchLimit
    MusicCheck = "/check/music?id="
    MusicDownloadurl = "/song/download/url?id="
    MusicDetail = "/song/detail?ids="
    UserPlaylist = "/user/playlist?uid="
    PlaylistDetail = "/playlist/detail?id="
    # 歌单内歌曲信息: playlistdetail
    # dict ["playlist"]["tracks"][num]
    # 名称 ~[name]
    # 副标题 ~[alia]
    # 作者 ~[ar][name]
    
    ## 查询单曲 MusicDetail
    # 名称 dict["songs"]["name"]
    # 作者 dict["songs"]["ar"]["name"]
    # 副标题 dict["songs"]["alia"]
    ########################

    # 登陆状态/昵称
    Np_Status = False
    # 是否使用过
    Np_Playing = False
    Np_NickName = ""
    Np_UserId = ""

    # 歌曲信息
    Music_Id = ""
    Music_Name = ""
    Music_Author = ""
    Music_Alia = ""
    Music_Size = 0
    Music_Type = ""

    Search_Word = ""
    #搜索结果 -> id, name, artist, alias(如果有), showname
    Search_List = list()
    #用户收藏歌单
    Play_List = list()
    # 其它用处
    _LoginPhone = None
    _LoginPw = None
    CatchSize = 12000
    Cookies = None

    GlobalSubP = None

    # Music menu菜单
    menu_open = False
    curr_page = 0

    #UI位置
    SCR_MENU_AREA = (835, 40, 440, 528)
    SCR_MENU_XALIGN = -0.05

init python in np_util:
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
    import urllib2
    

    def Get_User_Playlist():
        """
        获取用户歌单
        """
        cookie = np_globals.Cookies
        msclist = list()

        id = str(np_globals.Np_UserId)
        url = np_globals.Mainurl + np_globals.UserPlaylist + id
        plidr = requests.get(url, cookies = np_globals.Cookies, verify = np_globals.VerifyPath)
        plidj = plidr.json()
        plid = str(plidj["playlist"][0]["id"])
        url2 = np_globals.Mainurl + np_globals.PlaylistDetail + plid
        getmusiclist = requests.get(url2, cookies = cookie , verify = np_globals.VerifyPath)
        mlist = getmusiclist.json()
        for song in mlist['playlist']["tracks"]:
            id = str(song["id"])
            name = song["name"]
            artist = song["ar"][0]["name"]
            try:
                alias = str(song["alia"][0])
            except:
                alias = ""
            if alias == "":
                showname = name + " - " + artist
            else:
                showname = name + " - " + alias + " - " + artist
            showname = showname.replace('[','')
            showname = showname.replace(']','')
            showname = showname.replace('{','')
            showname = showname.replace('}','')
            msclist.append([id, name, artist, alias, showname])

        np_globals.Play_List = msclist


    def Catch_size(path = np_globals.Catch):
        """
        网上的代码 检测占用空间
        """
        total_size=0
        path=os.path.abspath(path)
        file_list=os.listdir(path)
        for i in file_list:
            i_path = os.path.join(path, i)
            if os.path.isfile(i_path):
                total_size += os.path.getsize(i_path)
            else:
                try:
                    file_size(i_path)
                except RecursionError:
                    raise Exception('递归操作时超出最大界限')
        return total_size

    def Music_Search(keyword):
        """
        搜索歌曲
        keyword 关键词 
        修改global的Search_List
        搜索结果 -> id, name, artist, alias(如果有, 无为空字符串), showname
        返回 结果list
        """
        res = list()
        keyword = urllib2.quote(keyword.encode('utf-8'))
        url = np_globals.Mainurl + np_globals.Search + keyword + np_globals.SearchToLimit
        search = requests.get(url, verify = np_globals.VerifyPath)
        result = search.json()
        for song in result["result"]["songs"]:
            id = str(song["id"])
            name = song["name"]
            artist = song["artists"][0]["name"]
            try:
                alias = song["alias"][0]
            except:
                alias = ""
            if alias == "":
                showname = name + " - " + artist
            else:
                showname = name + " - " + alias + " - " + artist
            showname = showname.replace('[','')
            showname = showname.replace(']','')
            showname = showname.replace('{','')
            showname = showname.replace('}','')
            res.append([id, name, artist, alias, showname])
        np_globals.Search_List = res
        return res

    def Music_GetDetail(id = np_globals.Music_Id):
        """
        获取歌曲的详细信息
        id 获取的歌曲，默认为Music_Id
        """
        if id == None or id == "":
            id = str(np_globals.Music_Id)
        url = np_globals.Mainurl + np_globals.MusicDetail + id
        debug_GetUrl = url
        info = requests.post(url, verify = np_globals.VerifyPath)
        debug_GetData = info
        infodata = info.json()
        np_globals.Music_Name = infodata["songs"][0]["name"]
        np_globals.Music_Author = infodata["songs"][0]["ar"][0]["name"]
        try:
            np_globals.Music_Alia = infodata["songs"][0]["alia"][0]
        except:
            np_globals.Music_Alia = ""
    
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
        url = np_globals.Mainurl + np_globals.RefreshLogin
        refresh = requests.get(url, cookies=np_globals.Cookies, verify = np_globals.VerifyPath)
        new_cookies = refresh.cookies
        np_globals.Cookies = new_cookies
        store.persistent.np_Cookie = new_cookies
    
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
            np_globals.Np_UserId = ""
        else:
            np_globals.Np_Status = True
            np_globals.Np_NickName = result["data"]["profile"]["nickname"]
            np_globals.Np_UserId = result["data"]["profile"]["userId"]
        return np_globals.Np_Status

    def Music_Logout():
        """
        注销账号 删除所有的cookies
        """
        cookie = np_globals.Cookies
        url = np_globals.Mainurl + np_globals.Logout
        requests.get(url, cookies = cookie, verify = np_globals.VerifyPath)
        np_globals.Cookies = None
        np_globals.Np_NickName = "Unlogin-未登录"
        np_globals.Np_Status = False
        store.persistent.np_Cookie = None
        #renpy.jump("np_emptylabel")


    def Music_Download(id):
        #根据ID下载flac
        id = str(id)
        cookie = np_globals.Cookies
        url = np_globals.Mainurl + np_globals.MusicDownloadurl + id
        music = requests.get(url, cookies = cookie, verify=np_globals.VerifyPath)
        try:
            getdata = music.json()
        except Exception:
            return False
        file_url = getdata["data"]["url"]
        np_globals.Music_Size = getdata['data']['size']
        np_globals.Music_Type = getdata['data']['type']
        if file_url == None:
            return False
        _music_download = requests.get(file_url,cookies = cookie, verify=np_globals.VerifyPath, stream=True)
        _flac = open(np_globals.Catch + "/" + id + ".flac", 'wb')
        for chunk in _music_download.iter_content(chunk_size = np_globals.CatchSize):
            if chunk:
                _flac.write(chunk)
        return True
    
    def Music_Check():
        """
        检测歌曲是否可用
        返回bool
        """
        url = np_globals.Mainurl + np_globals.MusicCheck + np_globals.Music_Id
        res = requests.get(url, verify = np_globals.VerifyPath)
        r = res.json()
        return r['success']

    def Music_Deleteflac():
        dirs = os.listdir(np_globals.Catch)
        for file_name in dirs:
            if file_name.find('flac') != -1:
                file = np_globals.Catch + "/" + file_name
                os.remove(file)

    def Music_DeleteCatch():
        dirs = os.listdir(np_globals.Catch)
        for file_name in dirs:
            if True:
                file = np_globals.Catch + "/" + file_name
                os.remove(file)

    def Music_Play(song, fadein=1.2, loop=True, set_per=True, fadeout=1.2, if_changed=False):
        Music_Deleteflac()
        song = str(song)
        
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
        np_globals.Np_Playing = True

init python in np_screen_util:
    import store

    class NpInputValue(store.InputValue):
        """
        Our subclass of InputValue for internal use
        Allows us to manipulate the user input
        For more info read renpy docs (haha yeah...docs...renpy...)
        """
        def __init__(self):
            self.default = True
            self.input_value = ""
            self.editable = True
            self.returnable = True
    
        def get_text(self):
            return self.input_value
    
        def set_text(self, s):
            if not isinstance(s, basestring):
                s = unicode(s)
            self.input_value = s

    #def toggleChildScreenAnimation(new_value):
    #"""
    #This allows us to hide the sub-menu w/o animation
    #when we need it to just disappear immediately
    #IN:
    #    new_value - a bool to switch the setting
    #"""
    #_screen = renpy.get_screen("ytm_history_submenu")
    #if _screen:
    #    _settings = _screen.scope.get("settings", None)
    #    if _settings:
    #        _settings["animate"] = new_value

    def setParentInputValue(new_input):
        """
        A wrapper which allows us to do the magic in local env
        IN:
            new_input - a new value for input
        """
        _screen = renpy.get_screen("np_input_screen")
        if _screen:
            np_input = _screen.scope.get("np_input", None)
            if np_input:
                np.set_text(new_input)

init 999 python:
    np_globals.Cookies = persistent.np_Cookie
    np_util.Music_Login_Status()

label np_emptylabel():
    pass
    return