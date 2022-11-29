 #歌曲URL dict["data"]["url"]
 #搜索id dict["result"][song]<循环>[id]/[name]/[author]
 #cookies dict["cookies"]
 
 #保存cookies：
 #先登录，然后cookies = a.cookies.get_dict()
 #a为login时的cookies
 #不要反复登录 会风控

init -100:
    default persistent._NP_API_key_able = False
    default persistent._NP_search_limit = "50"
    default persistent.np_restart_song = None

init -5 python in np_globals:
    import store
    import os
    if os.path.exists(renpy.config.basedir + "/game/Submods/NeteaseInMas/debug.np"):
        debug=True
    else:
        debug=False

    Basedir = renpy.config.basedir
    Catch = Basedir + "/game/Submods/NeteaseInMas/Catch"
    FFmpegDir =  Basedir + "/game/Submods/NeteaseInMas/ffmpeg/win32/usr/bin"
    FFmpegexe = FFmpegDir + "/ffmpeg"
    VerifyPath = True
    CookiesPath = Basedir + "/game/Submods/NeteaseInMas/Cookies/cookies.json"

    ######################## API
    
    Mainurl = None#"http://neteaseapi.0721play.icu"

    ### API get
    Version = "/inner/version"

    PhoneLogin = "/login/cellphone?phone="
    PhoneLoginPw = "&password="
    PhoneLoginPwMd5 = "&md5_password="
    PhoneCaptcha="&captcha="

    PhoneSendCaptcha="/captcha/sent?phone="

    EmailLogin = "/login?email="

    realIP="&realIP="

    Amonymous="/register/anonimous"
    RefreshLogin = "/login/refresh" #返回新cookie
    LoginStatus = "/login/status"
    Logout = "/logout"
    # 账户名称：dict["data"]["profile"]["nickname"]
    # 未登录：dict["data"]["profile"] = Null
    
    Search = "/search?keywords="
    SearchLimit = str(store.persistent._NP_search_limit)
    SearchToLimit = "&limit=" + SearchLimit
    MusicCheck = "/check/music?id="
    MusicDownloadurl = "/song/download/url?id="
    MusicDownloadurl2 = "/song/url?id="
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
    _LoginCaptcha = None
    # 下载缓存区大小
    CatchSize = 120000
    Cookies = None
    Header={'Connection':'close'}
    # 上次获取验证码时间
    GetCaptchaTime=0

    # ip
    Outip=""
    # 返回结果
    ReqCode = 0
    # Music menu菜单
    menu_open = False
    curr_page = 0

    #UI位置
    SCR_MENU_AREA = (835, 40, 440, 528)
    SCR_MENU_XALIGN = -0.05
    # api版本
    version = None

init 5 python in np_globals:
    def change_api(api):
        global Mainurl
        if api == "":
            Mainurl = "http://neteaseapi.0721play.icu"
        elif api[-1] == "/":
            Mainurl = api[:-1]
        else:
            Mainurl = api
        try:
            if store.np_util.Check_API_Available():
                return True, Mainurl
            else:
                Mainurl = "http://neteaseapi.0721play.icu"
                store.np_util.Check_API_Available()
                return False, "粘贴的API链接错误！将使用默认值！查看submod_log获取详细信息"
        except Exception as e:
            Mainurl = "http://neteaseapi.0721play.icu"
            store.mas_submod_utils.submod_log.error(e)
            return False, "粘贴的API链接错误！将使用默认值！查看submod_log获取详细信息"
        #return True, Mainurl
    store.mas_registerAPIKey(
        "netease_apiurl",
        "网易云音乐 - APIurl",
        on_change=change_api
    )
    if store.mas_getAPIKey("netease_apiurl") != "":
        Mainurl = store.mas_getAPIKey("netease_apiurl")
    else:
        Mainurl = "http://neteaseapi.0721play.icu"

init python in np_util:
    import json
    import requests
    import requests.utils as requtils
    import ssl
    #import renpy
    import store
    import hashlib
    import store.np_globals as np_globals
    import subprocess
    import threading
    import os, sys
    import store.songs as songs
    import urllib2
    import time
    from store.mas_submod_utils import submod_log

    
    def Save_Cookies(cookies):
        """
        保存Cookies
        IN:
            要保存的RequestsCookieJar
        """
        cookiesDict = requtils.dict_from_cookiejar(cookies)
        with open(np_globals.CookiesPath, 'w') as cookie:
            json.dump(cookiesDict, cookie)

    def Save_Cookies_From_Dict(cookies):
        """
        保存Cookies, 但是字典形式
        IN:
            要保存的字典
        """
        with open(np_globals.CookiesPath, 'w') as cookie:
            json.dump(cookies, cookie)
    
    def Load_Cookies():
        """
        从CookiesPath读取Cookies，保存至np_globals.Cookies
        """
        try:
            with open(np_globals.CookiesPath, 'r') as cookie:
                cookiesDict = json.load(cookie)
            np_globals.Cookies = requtils.cookiejar_from_dict(cookiesDict)
        except Exception as e:
            np_globals.Cookies = None
            submod_log.error("加载Cookies发生错误：{}".format(e))
    
    def Remove_Cookies():
        """
        删除Cookies文件
        """
        try:
            os.remove(np_globals.CookiesPath)
        except:
            pass

    def Check_API_Available():
        """
        检测API可用性
        return:
            True/False
        """
        try:
            API = requests.get(np_globals.Mainurl + np_globals.Version, verify = np_globals.VerifyPath, headers=np_globals.Header)
            API = API.json()
            store.np_globals.version = API['data']['version']
            return True
        except Exception as e:
            store.mas_submod_utils.submod_log.error(e)
            store.np_globals.version = None
            return False
    def Check_FFmpeg_init():
        a = os.getenv('Path')
        if a.find(np_globals.FFmpegDir) == -1:
            store.persistent.Np_InitedFFmpeg = False
        else:
            store.persistent.Np_InitedFFmpeg = True

    def Get_User_Playlist():
        """
        获取用户歌单
        """
        cookie = np_globals.Cookies
        msclist = list()

        id = str(np_globals.Np_UserId)
        url = np_globals.Mainurl + np_globals.UserPlaylist + id
        plidr = requests.get(url, cookies = np_globals.Cookies, verify = np_globals.VerifyPath, headers=np_globals.Header)
        plidj = plidr.json()
        plid = str(plidj["playlist"][0]["id"])
        url2 = np_globals.Mainurl + np_globals.PlaylistDetail + plid
        getmusiclist = requests.get(url2, cookies = cookie , verify = np_globals.VerifyPath, headers=np_globals.Header)
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
        search = requests.get(url, verify = np_globals.VerifyPath, headers=np_globals.Header)
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
        info = requests.get(url, verify = np_globals.VerifyPath, headers=np_globals.Header)
        infodata = info.json()
        np_globals.Music_Name = infodata["songs"][0]["name"]
        np_globals.Music_Author = infodata["songs"][0]["ar"][0]["name"]
        try:
            np_globals.Music_Alia = infodata["songs"][0]["alia"][0]
        except:
            np_globals.Music_Alia = ""
    

    def Music_ToWav():
        """
        将音频文件转码为WAV
        id 歌曲id
        """
        id = np_globals.Music_Id
        outdir = np_globals.Catch
        cmd = "\"{}\" -i \"{}/{}.flac\" -ab 990k \"{}/{}.wav\" -y".format(np_globals.FFmpegexe, outdir, id, outdir, id)
        st=subprocess.STARTUPINFO()
        st.dwFlags=subprocess.STARTF_USESHOWWINDOW
        st.wShowWindow=subprocess.SW_HIDE
        a = subprocess.Popen(cmd, startupinfo=st)
        return a.communicate()


    def Get_OutIp():
        np_globals.Outip=requests.get('http://ifconfig.me/ip', headers=np_globals.Header).text.strip()
        return np_globals.Outip

    def Music_Login(phone,pw,verifycode=None):
        #登录
        import time
        pw = str(pw)
        md5pw = hashlib.md5(pw.encode('utf-8'))
        url = np_globals.Mainurl + np_globals.PhoneLogin + str(phone)
        if not pw == "":
            url = url + np_globals.PhoneLoginPwMd5 + md5pw.hexdigest()
        if verifycode != None:
            url= url + np_globals.PhoneCaptcha + str(verifycode)
        url=url + "&timestamp={}".format(int(round(time.time()*1000)))+np_globals.realIP+np_globals.Outip
        login = requests.get(url, verify=np_globals.VerifyPath, headers=np_globals.Header)
        loginjson = login.json()
        try:
            failmessage = loginjson['message']
        except:
            failmessage = None
        if login.status_code != 200:
            submod_log.debug("url:{}".format(url))
            submod_log.debug("respond:{}".format(str(loginjson)))
            renpy.notify("登录错误代码 - {}\n请考虑更换API/等待API风控结束/使用短信验证码/更新API/重启\n查看submod_log可以查看详细信息\n以下为服务器返回错误信息：\n===================\n\"{}\"".format(login.status_code, failmessage))
        np_globals.Cookies = login.cookies
        Save_Cookies(login.cookies)
        Music_Login_Status()
        return np_globals.Np_Status

    def Music_Login_e(phone,pw,verifycode=None):
        #登录
        import time
        pw = str(pw)
        md5pw = hashlib.md5(pw.encode('utf-8'))
        url = np_globals.Mainurl + np_globals.EmailLogin + str(phone)
        if not pw == "":
            url = url + np_globals.PhoneLoginPwMd5 + md5pw.hexdigest()
        if verifycode != None:
            pass
            #url= url + np_globals.PhoneCaptcha + str(verifycode)
        url=url + "&timestamp={}".format(int(round(time.time()*1000)))+np_globals.realIP+np_globals.Outip
        login = requests.get(url, verify=np_globals.VerifyPath, headers=np_globals.Header)
        loginjson = login.json()
        try:
            failmessage = loginjson['message']
        except:
            failmessage = None
        if login.status_code != 200:
            renpy.notify("登录错误代码 - {}\n请考虑更换API/等待API风控结束/使用短信验证码/更新API/重启\n查看submod_log可以查看详细信息\n以下为服务器返回错误信息：\n===================\n\"{}\"".format(login.status_code, failmessage))
            submod_log.debug("url:{}".format(url))
            submod_log.debug("respond:{}".format(str(loginjson)))
        np_globals.Cookies = login.cookies
        Save_Cookies(np_globals.Cookies)
        Music_Login_Status()
        return np_globals.Np_Status
 
    def Music_Login_Refresh():
        #刷新登录
        url = np_globals.Mainurl + np_globals.RefreshLogin
        refresh = requests.get(url, cookies=np_globals.Cookies, verify = np_globals.VerifyPath, headers=np_globals.Header)
        new_cookies = refresh.cookies
        np_globals.Cookies.update(new_cookies)
        Save_Cookies(np_globals.Cookies)
        
    def Music_Get_Captcha(phone):
        """
        获取验证码

        return:
            是否成功
        """
        # 如果发送时间间隔<60，阻止发送
        if (time.time() - np_globals.GetCaptchaTime) < 60:
            renpy.notify("发送失败：发送太频繁，请等待{}s后重试".format(60 - (time.time() - np_globals.GetCaptchaTime)))
            return False
        url=np_globals.Mainurl + np_globals.PhoneSendCaptcha + str(phone) + "&timestamp={}".format(int(round(time.time()*1000)))
        send=requests.get(url, verify=np_globals.VerifyPath, headers=np_globals.Header)
        np_globals.ReqCod = send.status_code
        if send.status_code == 200:
            np_globals.GetCaptchaTime=time.time()
            sendjson=send.json()
            try:
                sendjson['message']
                try:
                    renpy.notify("发送失败：{}".format(sendjson['message']))
                except:
                    renpy.notify("发送失败：{}".format(sendjson['code']))
                return False
            except:
                return renpy.notify("发送成功，请注意查收")
                
        else:
            renpy.notify('发送失败，请检查网络连接')

    def Music_Login_Status():
        """
        检查登陆状态, 离线返回False, 在线返回昵称
        """
        import time
        cookie = np_globals.Cookies
        url = np_globals.Mainurl + np_globals.LoginStatus + "?&timestamp={}".format(int(time.time()*1000))
        check = requests.get(url, cookies = cookie, verify = np_globals.VerifyPath, headers=np_globals.Header)
        np_globals.ReqCode = check.status_code
        result = check.json()
        try:
            profile = result["data"]["profile"]
        except:
            np_globals.Np_Status = False
            np_globals.Np_NickName = "Unlogin - 未登录"
            np_globals.Np_UserId = ""
            return np_globals.Np_Status
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
        requests.get(url, cookies = cookie, verify = np_globals.VerifyPath, headers=np_globals.Header)
        np_globals.Cookies = None
        np_globals.Np_NickName = "Unlogin - 未登录"
        np_globals.Np_Status = False
        store.persistent.np_Cookie = None
        Remove_Cookies()
        #renpy.jump("np_emptylabel")


    def Music_Download(id):
        #根据ID下载flac
        id = str(id)
        cookie = np_globals.Cookies
        url = np_globals.Mainurl + np_globals.MusicDownloadurl + id
        music = requests.get(url, cookies = cookie, verify=np_globals.VerifyPath, headers=np_globals.Header)
        try:
            getdata = music.json()
        except Exception:
            return False
        file_url = getdata["data"]["url"]
        np_globals.Music_Size = getdata['data']['size']
        np_globals.Music_Type = getdata['data']['type']
        if file_url is None:
            return False
        _music_download = requests.get(file_url,cookies = cookie, verify=np_globals.VerifyPath, stream=True, headers=np_globals.Header)
        _flac = open(np_globals.Catch + "/" + id + "." + np_globals.Music_Type, 'wb')
        for chunk in _music_download.iter_content(chunk_size = np_globals.CatchSize):
            if chunk:
                _flac.write(chunk)
        _flac.close()
        return True

    def Music_Download_2(id):
        #根据ID下载flac - song/id
        id = str(id)
        cookie = np_globals.Cookies
        url = np_globals.Mainurl + np_globals.MusicDownloadurl2 + id
        music = requests.get(url, cookies = cookie, verify=np_globals.VerifyPath, headers=np_globals.Header)
        try:
            getdata = music.json()
        except Exception:
            return False
        file_url = getdata["data"][0]["url"]
        np_globals.Music_Size = getdata['data'][0]['size']
        np_globals.Music_Type = getdata['data'][0]['type']
        if file_url == None:
            return False
        _music_download = requests.get(file_url,cookies = cookie, verify=np_globals.VerifyPath, stream=True, headers=np_globals.Header)
        _flac = open(np_globals.Catch + "/" + id + "." + np_globals.Music_Type, 'wb')
        for chunk in _music_download.iter_content(chunk_size = np_globals.CatchSize):
            if chunk:
                _flac.write(chunk)
        _flac.close()
        return True

    def Music_Deleteflac():
        """
        删除无法播放的flac文件
        """ 
        dirs = os.listdir(np_globals.Catch)
        for file_name in dirs:
            if file_name.find('flac') != -1:
                file = np_globals.Catch + "/" + file_name
                try:
                    os.remove(file)
                except Exception as e:
                    submod_log.error("清除flac: {}".format(e))
                    continue
    def Music_DeleteCatch():
        """
        清理缓存文件夹，如果失败就跳过
        """
        dirs = os.listdir(np_globals.Catch)
        for file_name in dirs:
            if True:
                file = np_globals.Catch + "/" + file_name
                try:
                    os.remove(file)
                except Exception as e:
                    submod_log.error(e)
                    continue
    
    def Music_GetCatchSaveList():
        """
        列出缓存文件列表
        """
        dirs = os.listdir(np_globals.Catch)
        catched = []
        for file_name in dirs:
            for types in ["mp3", "wav"]:
                if file_name.find(types) != -1:
                    catched.append((np_globals.Catch + "/" +file_name).replace("\\","/"))
        return catched
    
    def Music_Play_List(song=Music_GetCatchSaveList(), fadein=1.2, loop=True, set_per=False, fadeout=1.2, if_changed=False):
        Music_Deleteflac()
        """
        播放已缓存列表
        IN:
            song - Music_GetCatchSaveList() 获取缓存列表
            fadein - 过度渐入时间
                (Default: 0.0)
            loop - 是否循环播放
                (Default: True)
            set_per - 是否保存至persistent 无实际意义
                (Default: False)
            fadeout - 过度渐出时间
                (Default: 0.0)
            if_changed - Whether or not to only set the song if it's changing
                (Use to play the same song again without it being restarted)
                (Default: False)
        """
        if song is None or song == []:
            renpy.music.stop(channel="music", fadeout=fadeout)
        else:
            renpy.music.play(
                song,
                channel="music",
                loop=loop,
                synchro_start=True,
                fadein=fadein,
                fadeout=fadeout,
                if_changed=if_changed
            )
        np_globals.Np_Playing = True
        np_globals.Music_Name = "<正在播放缓存列表>"
        np_globals.Music_Alia = ""
        np_globals.Music_Author = ""
        np_globals.Music_Id = ""
        store.persistent.np_restart_song = None

    def Music_Play(song, fadein=1.2, loop=True, set_per=True, fadeout=1.2, if_changed=False):
        song = str(song)
        
        """
        播放某一首歌 同时设置为启动音乐
        IN:
            song - 要播放的id. 如为None则停止
            fadein - 过度渐入时间
                (Default: 1.2)
            loop - 是否循环播放
                (Default: True)
            set_per - 是否保存至persistent 决定是否启动播放
                (Default: True)
            fadeout - 过度渐出时间
                (Default: 1.2)
            if_changed - Whether or not to only set the song if it's changing
                (Use to play the same song again without it being restarted)
                (Default: False)
        """
        if song is None:
            renpy.music.stop(channel="music", fadeout=fadeout)
            if set_per:
                store.persistent.current_track = None
        else:
            if set_per:
                store.persistent.np_restart_song = song
            if np_globals.Music_Type != "mp3":
                mtype = ".wav"
            else:
                mtype = ".mp3"
            song = (np_globals.Catch + "/" + song + mtype).replace("\\","/")
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
            store.persistent.current_track = None
            store.persistent.np_restart_song_type = np_globals.Music_Type
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
    # 初始化cookies
    if persistent.np_Cookie is not None:
        persistent.np_Cookie = None
    np_util.Load_Cookies()

    # 检查API连通性
    try:
        if np_util.Check_API_Available():
            np_util.Music_Login_Status()
            persistent._NP_API_key_able = True
            np_util.Get_OutIp()
        else:
            persistent._NP_API_key_able = False
    except Exception as e:
        # 尝试两次
        try:
            if np_util.Check_API_Available():
                np_util.Music_Login_Status()
                persistent._NP_API_key_able = True
                np_util.Get_OutIp()
            else:
                persistent._NP_API_key_able = False
        except Exception as e:
            persistent._NP_API_key_able = False
            store.mas_submod_utils.submod_log.info("初始化连接时发生异常：{}".format(e))

init -900 python:
    # 创建缓存和cookies文件夹
    try:
        os.mkdir(renpy.config.basedir + "/game/Submods/NeteaseInMas/Catch")
    except:
        pass
    try:
        os.mkdir(renpy.config.basedir + "/game/Submods/NeteaseInMas/Cookies")
    except:
        pass
    
    # 签名fix
    import os
    os.environ['REQUESTS_CA_BUNDLE'] = renpy.config.basedir + "/game/python-packages/certifi/cacert.pem"
    

label np_emptylabel():
    pass
    return
 
init 950 python:
    # 自启动播放判断
    def np_start_play():
        # 使用了MAS默认菜单播放音乐，清除np保存的歌曲以防止错误
        if store.persistent.current_track is not None:
            store.persistent.np_restart_song = None
            store.persistent.np_restart_song_type = None
        
        # 如果设置了播放缓存
        if store.persistent.np_start_loopplay:
            try:
                store.np_util.Music_Play_List(song=store.np_util.Music_GetCatchSaveList(), fadein=1.2, loop=True, set_per=False, fadeout=1.2, if_changed=False)
            except Exception as e:
                store.mas_submod_utils.submod_log.error("播放缓存失败：{}".format(e))
            return
        
        # 只当np_restart_song不为空且current_track为空时启动播放
        if store.persistent.np_restart_song is not None and store.persistent.current_track is None:
            np_globals.Music_Type = store.persistent.np_restart_song_type
            try:
                np_util.Music_Play(store.persistent.np_restart_song)
            except Exception as e:
                store.mas_submod_utils.submod_log.error("播放文件失败：{}".format(e))

    # 在preloop label注册来实现自启播放
    store.mas_submod_utils.registerFunction('ch30_preloop', np_start_play)