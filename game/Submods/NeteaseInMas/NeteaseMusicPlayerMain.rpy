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
    default persistent._np_force_playlist = None
    default np_search_input_value = ""

init -5 python in np_globals:
    import store
    import os
    if os.path.exists(renpy.config.basedir + "/game/Submods/NeteaseInMas/debug.np"):
        debug=True
    else:
        debug=False

    Basedir = renpy.config.basedir
    Catch = Basedir + "/game/Submods/NeteaseInMas/Catch"
    FFmpegDir =  Basedir + "/game/Submods/NeteaseInMas/ffmpeg"
    FFmpegexe = FFmpegDir + "/ffmpeg"
    VerifyPath = True
    CookiesPath = Basedir + "/game/Submods/NeteaseInMas/Cookies/cookies.json"
    QRImageDir = Basedir + "/game/Submods/NeteaseInMas/"
    QRImagePath = Basedir + "/game/Submods/NeteaseInMas/QR.png"
    QRImageDirforScreen = "Submods/NeteaseInMas/"

    QRFileName = "QR.png"
    ######################## API
    
    Mainurl = "https://neteaseapi.0721play.icu"

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
    MusicMatchUrl = "/song/url/match?id="
    MusicDetail = "/song/detail?ids="
    UserPlaylist = "/user/playlist?uid="
    UserCloud = "/user/cloud?limit=1000"
    PlaylistDetail = "/playlist/detail?id="
    GetQRKey = "/login/qr/key"
    QRCreate = "/login/qr/create?key="
    QRCheck = "/login/qr/check?key="



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
    _QRLogin = False

    # 下载缓存区大小
    CatchSize = 120000
    Cookies = None
    CookiesQR = ""
    _QRCookie = None # 临时
    Header={'Connection':'close'}
    AudioHeader = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://music.163.com/',
        'Connection': 'close',
    }
    # 上次获取验证码时间
    GetCaptchaTime=0
    QRData = None
    QRLastQueryCode = 0
    # ip
    Outip=""
    # 返回结果
    ReqCode = 0
    # Music menu菜单
    menu_open = False
    curr_page = 0
    # 两种列表的独立缓存
    playlist_cache = []      # 我喜欢的音乐
    cloud_cache = []         # 云盘音乐
    current_list_type = ""   # 当前显示类型
    menu_title = "音乐"       # 音乐菜单左上角标题
    search_filter = ""

    #UI位置
    SCR_MENU_AREA = (835, 40, 440, 528)
    SCR_MENU_XALIGN = -0.05
    # api版本
    version = None

init 5 python in np_globals:
    def change_api(api):
        global Mainurl
        if api == "":
            Mainurl = "https://neteaseapi.0721play.icu"
        elif api[-1] == "/":
            Mainurl = api[:-1]
        else:
            Mainurl = api
        try:
            if store.np_util.Check_API_Available():
                return True, Mainurl
            else:
                Mainurl = "https://neteaseapi.0721play.icu"
                store.np_util.Check_API_Available()
                return False, "粘贴的API链接错误！将使用默认值！查看submod_log获取详细信息"
        except Exception as e:
            Mainurl = "https://neteaseapi.0721play.icu"
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
        Mainurl = "https://neteaseapi.0721play.icu"

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
    #import urllib2
    # 兼容 Python 2 / Python 3
    try:
        # Python 3 (Ren'Py 8)
        from urllib.parse import quote
        from urllib.request import urlopen, Request
        from urllib.error import HTTPError
    except ImportError:
        # Python 2 (Ren'Py 7)
        from urllib import quote
        from urllib2 import urlopen, Request, HTTPError
    import time
    from store.mas_submod_utils import submod_log
     
    #Android追加路径
    import os
        
        if renpy.android:
            Netease_dir = "/storage/emulated/0/MAS/game/Submods/NeteaseInMas/Catch/"
            #external_dir = "/storage/emulated/0/Download/netease/cloudmusic/Music/"
    
            if os.path.isdir(Netease_dir) and Netease_dir not in renpy.config.searchpath:
                #追加到renpy的路径
                renpy.config.searchpath.append(Netease_dir)

    def randompngname():
        return str(int(time.time()))+'.png'

    def Save_Cookies(cookies):
        """
        保存Cookies
        IN:
            要保存的RequestsCookieJar
        """
        return Save_Cookies_From_Dict(cookies)
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
        return Load_Cookies_to_QR()
        try:
            with open(np_globals.CookiesPath, 'r') as cookie:
                cookiesDict = json.load(cookie)
            np_globals.Cookies = requtils.cookiejar_from_dict(cookiesDict)
        except Exception as e:
            np_globals.Cookies = None
            submod_log.error("加载Cookies发生错误：{}".format(e))
    
    def Load_Cookies_to_QR():
        """
        从CookiesPath读取Cookies，保存至np_globals.CookiesQR
        """
        try:
            with open(np_globals.CookiesPath, 'r') as cookie:
                cookiesDict = json.load(cookie)
            np_globals.CookiesQR = cookiesDict
            np_globals._QRLogin = True
        except Exception as e:
            np_globals.CookiesQR = None
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
        if not store.persistent._np_force_playlist:
            id = str(np_globals.Np_UserId)
            url = np_globals.Mainurl + np_globals.UserPlaylist + id
            if np_globals._QRLogin:
                plidr = requests.post(url,json={'cookie': np_globals.CookiesQR}, verify = np_globals.VerifyPath, headers=np_globals.Header)
            else:
                plidr = requests.get(url, cookies = np_globals.Cookies, verify = np_globals.VerifyPath, headers=np_globals.Header)
            plidj = plidr.json()
            plid = str(plidj["playlist"][0]["id"])
            url2 = np_globals.Mainurl + np_globals.PlaylistDetail + plid
        else:
            url2 = np_globals.Mainurl + np_globals.PlaylistDetail + str(store.persistent._np_force_playlist)
        if np_globals._QRLogin:
            getmusiclist = requests.post(url2, json={'cookie': np_globals.CookiesQR}, verify=np_globals.VerifyPath, headers=np_globals.Header)
        else:
            getmusiclist = requests.get(url2, cookies = cookie , verify = np_globals.VerifyPath, headers=np_globals.Header)
        mlist = getmusiclist.json()
        for song in mlist.get('playlist', {}).get("tracks", []):
            id = str(song.get("id", ""))

            # 空值保护
            name = song.get("name") or "未知歌曲"

            ar_list = song.get("ar") or []
            if ar_list and ar_list[0].get("name"):
                artist = ar_list[0]["name"]
            else:
                artist = "未知歌手"

            try:
                alias = str(song["alia"][0]) if song.get("alia") else ""
            except:
                alias = ""

            if alias == "":
                showname = name + " - " + artist
            else:
                showname = name + " - " + alias + " - " + artist

            showname = showname.replace('[','').replace(']','').replace('{','').replace('}','')
            msclist.append([id, name, artist, alias, showname])

        np_globals.playlist_cache = list(msclist)
        np_globals.Play_List = list(msclist)
        np_globals.current_list_type = "playlist"
        np_globals.menu_title = "我喜欢的音乐"

    def Get_User_Cloud():
        """
        获取用户云盘的所有歌曲（分页拉取）
        """
        cookie = np_globals.Cookies
        msclist = list()

        offset = 0
        limit = 100          # 每页拉取数量
        max_pages = 50       # 最多拉取 50 页，防止死循环
        page = 0

        while page < max_pages:
            url = np_globals.Mainurl + "/user/cloud?limit={}&offset={}".format(limit, offset)
            #submod_log.info("[NP-DEBUG] 拉取云盘 offset={} limit={}".format(offset, limit))

            if np_globals._QRLogin:
                cloudr = requests.post(url, json={'cookie': np_globals.CookiesQR}, verify=np_globals.VerifyPath, headers=np_globals.Header)
            else:
                cloudr = requests.get(url, cookies=cookie, verify=np_globals.VerifyPath, headers=np_globals.Header)

            try:
                cloudj = cloudr.json()
            except Exception as e:
                submod_log.error("[NP-DEBUG] 云盘返回非 JSON: {}".format(e))
                break

            data_list = cloudj.get("data", [])
            if isinstance(data_list, dict):
                data_list = data_list.get("songs", [])

            if not data_list:
                #submod_log.info("[NP-DEBUG] 云盘第 {} 页返回空，结束".format(page))
                break

            for song in data_list:
                simple = song.get("simpleSong")
                if simple:
                    sid = str(simple.get("id", ""))
                    name = simple.get("name") or "未知歌曲"
                    ar = simple.get("ar") or []
                    artist = ar[0]["name"] if ar and ar[0].get("name") else "未知歌手"
                else:
                    sid = str(song.get("songId") or song.get("id") or "")
                    name = song.get("songName") or song.get("name") or "未知歌曲"
                    artist = song.get("artist") or "未知歌手"

                if not sid:
                    continue

                alias = ""
                showname = name + " - " + artist
                showname = showname.replace('[','').replace(']','').replace('{','').replace('}','')
                msclist.append([sid, name, artist, alias, showname])

            #submod_log.info("[NP-DEBUG] 云盘第 {} 页获取 {} 首，累计 {} 首".format(page, len(data_list), len(msclist)))

            # 判断是否还有下一页
            has_more = cloudj.get("hasMore", False)
            if not has_more:
                #submod_log.info("[NP-DEBUG] hasMore=False，结束分页")
                break

            # 返回数量少于 limit 也认为结束
            if len(data_list) < limit:
                #submod_log.info("[NP-DEBUG] 返回数量少于 limit，结束分页")
                break

            offset += limit
            page += 1

        np_globals.cloud_cache = list(msclist)
        np_globals.Play_List = list(msclist)
        np_globals.current_list_type = "cloud"
        np_globals.menu_title = "云盘音乐"
        #submod_log.info("[NP-DEBUG] 云盘歌曲最终总数 = {}".format(len(msclist)))


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
        keyword = quote(keyword.encode('utf-8'))
        url = np_globals.Mainurl + np_globals.Search + keyword + np_globals.SearchToLimit
        search = requests.get(url, verify = np_globals.VerifyPath, headers=np_globals.Header)
        result = search.json()
        for song in result["result"]["songs"]:
            id = str(song["id"])
            name = song["name"]
            artist = song["artists"][0]["name"]
            # 灰色歌曲标记
            fee = song.get("fee", 0)
            privilege = song.get("privilege", {}) or {}
            st = privilege.get("st", 0) or 0
            if fee in (1, 4) or st < 0:
                name = "[灰] " + name
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

    def Music_Search_Artist(keyword):
        """
        搜索歌手，返回歌手列表
        return: [[artist_id, artist_name], ...]
        """
        res = list()
        kw = quote(keyword.encode('utf-8'))
        url = np_globals.Mainurl + "/search?keywords=" + kw + "&type=100&limit=30"
        try:
            r = requests.get(url, verify=np_globals.VerifyPath,
                             headers=np_globals.Header, timeout=15)
            j = r.json()
            for a in (j.get("result", {}) or {}).get("artists", []) or []:
                res.append([str(a.get("id", "")), a.get("name") or "未知歌手"])
        except Exception as e:
            submod_log.error("Music_Search_Artist 异常：{}".format(e))
        return res


    def Music_Get_Artist_All_Songs(artist_id):
        """
        拉取某歌手的全部歌曲（含灰歌），不设上限，直到 API 返回空
        return: [[id, name, artist, alias, showname], ...]
        """
        res = list()
        offset = 0
        limit = 100
        page = 0

        while True:
            url = "{}/artist/songs?id={}&limit={}&offset={}&order=hot".format(
                np_globals.Mainurl, str(artist_id), limit, offset
            )
            try:
                r = requests.get(url, verify=np_globals.VerifyPath,
                                 headers=np_globals.Header, timeout=30)
                j = r.json()
            except Exception as e:
                submod_log.error("Music_Get_Artist_All_Songs 异常：{}".format(e))
                break

            songs = j.get("songs", []) or []
            if not songs:
                break

            for song in songs:
                sid = str(song.get("id", ""))
                if not sid:
                    continue
                name = song.get("name") or "未知歌曲"

                ar_list = song.get("ar") or song.get("artists") or []
                if ar_list and ar_list[0].get("name"):
                    artist = "/".join([x.get("name", "") for x in ar_list if x.get("name")]) or "未知歌手"
                else:
                    artist = "未知歌手"

                # 灰色标记（和 Music_Search 保持一致）
                fee = song.get("fee", 0)
                privilege = song.get("privilege", {}) or {}
                st = privilege.get("st", 0) or 0
                if fee in (1, 4) or st < 0:
                    name = "[灰] " + name

                try:
                    alias = str(song["alia"][0]) if song.get("alia") else ""
                except:
                    alias = ""

                if alias == "":
                    showname = name + " - " + artist
                else:
                    showname = name + " - " + alias + " - " + artist
                showname = (showname.replace('[','').replace(']','')
                                     .replace('{','').replace('}',''))

                res.append([sid, name, artist, alias, showname])

            # 返回数量少于 limit 说明到底了
            if len(songs) < limit:
                break

            offset += limit
            page += 1
            #submod_log.info("Music_Get_Artist_All_Songs 已拉取 {} 首...".format(len(res)))

        #submod_log.info("歌手 {} 共拉取 {} 首歌曲".format(artist_id, len(res)))
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
    

    def Music_ToMp3():
        """
        将音频文件转码为MP3
        id 歌曲id
        """
        import os, subprocess
    
        id = str(np_globals.Music_Id)
        outdir = np_globals.Catch
        in_type = str(np_globals.Music_Type).lower()
        
        # 如果已经是 mp3，无需转码
        if in_type == 'mp3':
            return True
            
        in_path = "{}/{}.{}".format(outdir, id, in_type)
        out_path = "{}/{}.mp3".format(outdir, id)
        
        # 根据平台获取 ffmpeg 路径并执行
        try:
            if renpy.android:
                from jnius import autoclass
                activity = autoclass("org.renpy.android.PythonSDLActivity").mActivity
                ffmpeg_exe = os.path.join(activity.getApplicationInfo().nativeLibraryDir, "libmas_ffmpeg.so")
                
                if not os.path.exists(ffmpeg_exe):
                    submod_log.error("[NP-DEBUG] 找不到 ffmpeg: {}".format(ffmpeg_exe))
                    return False
                    
                # 安卓端用列表形式，不弹黑框（安卓本来也没黑框）
                cmd = [ffmpeg_exe, "-i", in_path, "-c:a", "libmp3lame", "-b:a", "320k", out_path, "-y"]
                a = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
            else:
                # PC 端使用字符串拼接
                ffmpeg_exe = np_globals.FFmpegexe
                if not os.path.exists(ffmpeg_exe):
                    submod_log.error("[NP-DEBUG] 找不到 ffmpeg: {}".format(ffmpeg_exe))
                    return False
                    
                # 使用引号防止路径中有空格
                cmd = "\"{}\" -i \"{}\" -c:a libmp3lame -b:a 320k \"{}\" -y".format(ffmpeg_exe, in_path, out_path)
                
                # Windows 隐藏黑框的经典写法
                st = subprocess.STARTUPINFO()
                st.dwFlags = subprocess.STARTF_USESHOWWINDOW
                st.wShowWindow = subprocess.SW_HIDE
                
                # 加上 PIPE 捕获输出
                a = subprocess.Popen(cmd, startupinfo=st, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            stdout, stderr = a.communicate()
            
            if a.returncode == 0 and os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                #submod_log.info("[NP-DEBUG] 转码 MP3 成功")
                np_globals.Music_Type = "mp3"
                return True
            else:
                err_msg = stderr.decode('utf-8', errors='ignore')
                submod_log.error("[NP-DEBUG] 转码失败: {}".format(err_msg))
                return False
                
        except Exception as e:
            submod_log.error("[NP-DEBUG] 执行异常: {}".format(e))
            return False
    

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

    def Music_Get_QRBase64():
        """
        获取二维码base64编码

        return:
            (key, base64编码)
        """

        #获取图片base64编码
        keyurl = np_globals.Mainurl + np_globals.GetQRKey + "?timestamp={}".format(int(round(time.time()*1000)))+np_globals.realIP+np_globals.Outip
        keyreq = requests.get(keyurl, verify = np_globals.VerifyPath, headers=np_globals.Header)
        keyjson = keyreq.json()
        if not keyjson['code'] == 200:
            raise Exception("获取二维码key失败 {}".format(keyjson))
        np_globals._QRCookie = keyreq.cookies
        key = keyjson['data']["unikey"]
        imgurl = np_globals.Mainurl + np_globals.QRCreate + key + "&qrimg=true" + "&timestamp={}".format(int(round(time.time()*1000)))+np_globals.realIP+np_globals.Outip
        imgreq = requests.get(imgurl, verify = np_globals.VerifyPath, headers=np_globals.Header, cookies=np_globals._QRCookie)
        imgjson = imgreq.json()
        imgbase64 = imgjson['data']['qrimg']

        return (key, imgbase64)
    def Save_Image(b64, filename):
        # 去除前缀
        import base64
        if b64.startswith('data:image/png;base64,'):
            b64 = b64[len('data:image/png;base64,'):]

        # 解码 Base64 数据
        image_data = base64.b64decode(b64)

        # 将解码的数据写入 PNG 文件
        with open(filename, "wb") as file:
            file.write(image_data)

    def Music_Check_Status(key):
        checkurl = np_globals.Mainurl + np_globals.QRCheck + key + "&timestamp={}".format(int(round(time.time()*1000)))+np_globals.realIP+np_globals.Outip+"&noCookie=true"
        checkreq = requests.get(checkurl, verify = np_globals.VerifyPath, headers=np_globals.Header, cookies=np_globals._QRCookie)
        checkjson = checkreq.json()
        status = checkjson['code']
        np_globals.QRLastQueryCode = status
        if status == 803:
            np_globals._QRLogin = True
            res = Music_Login_Status_QR(checkjson['cookie'])
            if res:
                np_globals.CookiesQR = checkjson['cookie']
                Save_Cookies(np_globals.CookiesQR)
                store.persistent._np_force_playlist = None   # 扫码登录成功后清除强制歌单
            return status
        else:
            return status


    def Music_Login_Status_QR(cookie):
        """
        检查登陆状态, 离线返回False, 在线返回昵称
        """
        data = {
            'cookie': cookie
        }
        import time
        cookie = np_globals.Cookies
        url = np_globals.Mainurl + np_globals.LoginStatus + "?&timestamp={}".format(int(time.time()*1000))
        check = requests.post(url, verify = np_globals.VerifyPath, headers=np_globals.Header, json=data)
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

 
    def Music_Login_Refresh():
        #刷新登录
        url = np_globals.Mainurl + np_globals.RefreshLogin
        refresh = requests.get(url, cookies=np_globals.Cookies, verify = np_globals.VerifyPath, headers=np_globals.Header)
        new_cookies = refresh.cookies
        np_globals.Cookies = new_cookies
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

    def Music_Login_Status(key = None):
        """
        检查登陆状态, 离线返回False, 在线返回昵称
        """
        if np_globals._QRLogin:
            return Music_Login_Status_QR(np_globals.CookiesQR)
        if store.persistent._np_force_playlist:
            np_globals.Np_Status = True
            np_globals.Np_NickName = "歌单id: " + str(store.persistent._np_force_playlist)
            np_globals.Np_UserId = ""
            return np_globals.Np_Status 
            
        import time
        cookie = np_globals.Cookies
        url = np_globals.Mainurl + np_globals.LoginStatus + "?&timestamp={}".format(int(time.time()*1000))
        if np_globals._QRLogin:
            check = requests.post(url, json={'cookie': np_globals.CookiesQR}, verify=np_globals.VerifyPath, headers=np_globals.Header)
        else:
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
        if np_globals._QRLogin:
            requests.post(
                url,
                json={'cookie': np_globals.CookiesQR},
                verify=np_globals.VerifyPath,
                headers=np_globals.Header
            )
        else:
            requests.get(url, cookies = cookie, verify=np_globals.VerifyPath, headers=np_globals.Header)
        np_globals.Cookies = None
        np_globals.Np_NickName = "Unlogin - 未登录"
        np_globals.Np_Status = False
        store.persistent.np_Cookie = None
        np_globals.QRLastQueryCode = 0
        np_globals.QRData = None
        np_globals._QRLogin = False
        Remove_Cookies()
        #renpy.jump("np_emptylabel")

    def _Get_Download_Header(url):
        """
        根据下载链接的域名，返回合适的请求头（防盗链）。
        """
        u = (url or "").lower()
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

        # 默认
        referer = "https://music.163.com/"

        if "kuwo.cn" in u:
            referer = "https://www.kuwo.cn/"
        elif "kugou.com" in u or "kglink" in u:
            referer = "https://www.kugou.com/"
        elif "migu" in u:
            referer = "https://music.migu.cn/"
        elif "bilibili" in u or "bilivideo" in u or "hdslb.com" in u:
            referer = "https://www.bilibili.com/"
        elif "qq.com" in u or "y.qq.com" in u or "qqmusic" in u:
            referer = "https://y.qq.com/"
        elif "126.net" in u:
            referer = "https://music.163.com/"

        return {
            "User-Agent": ua,
            "Referer": referer,
            "Connection": "close",
        }

    def _Get_Song_Url(id):
        """
        获取歌曲下载 URL。
        依次尝试，跳过试听片段：
          1. /song/download/url
          2. /song/url
          3. /song/url/match （解灰，需开关开启）
        返回 (url, size, type) 或 (None, 0, "")
        """
        id = str(id)
        cookie = np_globals.Cookies
        HEADERS = np_globals.Header
        VERIFY = np_globals.VerifyPath
        br = str(store.persistent._np_download_br)

        def _is_trial(data, url):
            """判断返回的是不是试听片段"""
            if data and data.get("freeTrialInfo") is not None:
                #submod_log.info("[NP-DEBUG] 试听检测：freeTrialInfo 不为空")
                return True
            if url:
                u = url.lower()
                # 网易云试听片段 URL 特征
                if "jd-musicrep-ts" in u or "-ts/" in u or "/ts/" in u or "trial" in u:
                    #submod_log.info("[NP-DEBUG] 试听检测：URL 含试听关键字")
                    return True
            if data:
                size = data.get("size", 0)
                if size and size < 1024 * 1024:
                    #submod_log.info("[NP-DEBUG] 试听检测：size={} < 1MB".format(size))
                    return True
                t = data.get("time", 0)
                if t and t < 60000:
                    #submod_log.info("[NP-DEBUG] 试听检测：time={} < 60s".format(t))
                    return True
            return False
            
        # ---- 1. song/url ----
        url2 = np_globals.Mainurl + np_globals.MusicDownloadurl2 + id + "&br=" + br
        try:
            if np_globals._QRLogin:
                r2 = requests.post(url2, json={'cookie': np_globals.CookiesQR}, verify=VERIFY, headers=HEADERS, timeout=15)
            else:
                r2 = requests.get(url2, cookies=cookie, verify=VERIFY, headers=HEADERS, timeout=15)
            j2 = r2.json()
            d2 = (j2.get("data") or [{}])[0]
            u2 = d2.get("url")
            #submod_log.info("[NP-DEBUG] song/url 返回：url={}, size={}, time={}, freeTrialInfo={}".format(
            #    (u2[:60] + "...") if u2 else None,
            #    d2.get("size"),
            #    d2.get("time"),
            #    d2.get("freeTrialInfo")
            #))
            if u2 and not _is_trial(d2, u2):
                return u2, d2.get('size', 0), str(d2.get('type', 'mp3')).lower()
            elif u2:
                #submod_log.info("[NP-DEBUG] song/url 判定为试听，跳过")
                pass
        except Exception as e:
            submod_log.error("[NP-DEBUG] song/url 异常：{}".format(e))

        # ---- 2. song/download/url ----
        url1 = np_globals.Mainurl + np_globals.MusicDownloadurl + id + "&br=" + br
        try:
            if np_globals._QRLogin:
                r = requests.post(url1, json={'cookie': np_globals.CookiesQR}, verify=VERIFY, headers=HEADERS, timeout=15)
            else:
                r = requests.get(url1, cookies=cookie, verify=VERIFY, headers=HEADERS, timeout=15)
            j = r.json()
            d = j.get("data", {}) or {}
            u = d.get("url")
            #submod_log.info("[NP-DEBUG] song/download/url 返回：url={}, size={}, time={}, freeTrialInfo={}".format(
            #    (u[:60] + "...") if u else None,
            #    d.get("size"),
            #    d.get("time"),
            #    d.get("freeTrialInfo")
            #))
            if u and not _is_trial(d, u):
                return u, d.get('size', 0), str(d.get('type', 'mp3')).lower()
            elif u:
                #submod_log.info("[NP-DEBUG] song/download/url 判定为试听，跳过")
                pass
        except Exception as e:
            #submod_log.info("[NP-DEBUG] song/download/url 异常：{}".format(e))
            submod_log.error("[NP-DEBUG] song/download/url 异常：{}".format(e))


        # ---- 3. 解灰（仅在开关开启时） ----
        if not store.persistent._np_unblock_enable:
            #submod_log.info("[NP-DEBUG] 解灰未开启，放弃 id={}".format(id))
            return None, 0, ""

        # 音源列表：用户指定了就用指定的，否则按顺序轮流尝试
        if store.persistent._np_unblock_source:
            _sources = [store.persistent._np_unblock_source]
        else:
            _sources = ["", "kuwo", "kugou", "qq", "migu", "bilibili"]

        for _src in _sources:
            match_url = np_globals.Mainurl + np_globals.MusicMatchUrl + id
            if _src:
                match_url = match_url + "&source=" + _src
            #submod_log.info("[NP-DEBUG] 尝试解灰 id={} source='{}'".format(id, _src if _src else "auto"))
            try:
                if np_globals._QRLogin:
                    mr = requests.post(match_url, json={'cookie': np_globals.CookiesQR},
                                       verify=VERIFY, headers=HEADERS, timeout=45)
                else:
                    mr = requests.get(match_url, cookies=cookie,
                                      verify=VERIFY, headers=HEADERS, timeout=45)
                mj = mr.json()
                #submod_log.info("[NP-DEBUG] 解灰返回：{}".format(str(mj)[:200]))

                mu = None
                data_field = mj.get("data")
                if isinstance(data_field, dict):
                    mu = data_field.get("url")
                elif isinstance(data_field, list) and data_field:
                    mu = data_field[0].get("url")
                elif isinstance(data_field, basestring) and data_field:
                    mu = data_field
                elif mj.get("url"):
                    mu = mj["url"]

                if mu:
                    lower = mu.lower()
                    if ".flac" in lower:
                        mtype = "flac"
                    elif ".m4a" in lower:
                        mtype = "m4a"
                    elif ".mp3" in lower:
                        mtype = "mp3"
                    else:
                        mtype = "mp3"
                    #submod_log.info("[NP-DEBUG] 解灰成功(source={})，格式={}，url 前100：{}".format(
                    #    _src if _src else "auto", mtype, mu[:100]))
                    return mu, 0, mtype
                else:
                    #submod_log.info("[NP-DEBUG] source={} 未返回 url，换下一个".format(_src if _src else "auto"))
                    pass
            except Exception as e:
                submod_log.error("[NP-DEBUG] source={} 解灰异常：{}".format(_src if _src else "auto", e))
                # 超时/异常都继续试下一个源
                continue

        submod_log.error("[NP-DEBUG] 所有音源都没找到 id={}".format(id))
        return None, 0, ""

    def _Download_Music_Core(id, debug_tag):
        id = str(id)
        file_url, size, mtype = _Get_Song_Url(id)
        if not file_url:
            submod_log.error("[NP-DEBUG] {} 未获取到可用 URL id={}".format(debug_tag, id))
            return False
    
        np_globals.Music_Size = size
        np_globals.Music_Type = str(mtype).lower().strip()
        _dl_header = _Get_Download_Header(file_url)
    
        try:
            _music_download = requests.get(
                file_url, verify=np_globals.VerifyPath, stream=True,
                headers=_dl_header, timeout=60
            )
            _music_download.raise_for_status() # 检查 HTTP 状态，防死链
        except Exception as e:
            submod_log.error("[NP-DEBUG] {} 请求异常：{}".format(debug_tag, e))
            return False
    
        path = np_globals.Catch + "/" + id + "." + np_globals.Music_Type
        _total = 0
        try:
            with open(path, 'wb') as _file: # 使用 with 防止文件被占用
                for chunk in _music_download.iter_content(chunk_size=np_globals.CatchSize):
                    if chunk:
                        _file.write(chunk)
                        _total += len(chunk)
        except Exception as e:
            submod_log.error("[NP-DEBUG] {} 写入异常：{}".format(debug_tag, e))
            try: os.remove(path)
            except: pass
            return False
        finally:
            _music_download.close() # 确保关闭网络流
    
        if _total == 0:
            submod_log.error("[NP-DEBUG] {} 下载为空 id={} status={}".format(debug_tag, id, _music_download.status_code))
            try: os.remove(path)
            except: pass
            return False
    
        return True
    
    def Music_Download(id):
        return _Download_Music_Core(id, "Music_Download")
    
    def Music_Download_2(id):
        return _Download_Music_Core(id, "Music_Download_2")
        
    def Music_Deleteflac():
        """
        清理flac文件
        """ 
        import time
        try:
            dirs = os.listdir(np_globals.Catch)
            for file_name in dirs:
                if file_name.endswith('.flac'):
                    file_path = np_globals.Catch + "/" + file_name
                    success = False
                    for i in range(5):
                        try:
                            os.remove(file_path)
                            success = True
                            #submod_log.info("[NP-DEBUG] 成功清理文件: {}".format(file_name))
                            break
                        except Exception as e:
                            time.sleep(0.5)
                    if not success:
                        submod_log.error("[NP-DEBUG] 清理失败，可能文件被占用: {}".format(file_name))
        except Exception as e:
            submod_log.error("[NP-DEBUG] 清理 flac 出错: {}".format(e))
                    
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
        Android追加路径
        """
        # import os
        
        # if renpy.android:
        #     Netease_dir = "/storage/emulated/0/MAS/game/Submods/NeteaseInMas/Catch/"
        #     #external_dir = "/storage/emulated/0/Download/netease/cloudmusic/Music/"
    
        #     if os.path.isdir(Netease_dir) and Netease_dir not in renpy.config.searchpath:
        #         #追加到renpy的路径
        #         renpy.config.searchpath.append(Netease_dir)

        dirs = os.listdir(np_globals.Catch)
        catched = []
        for file_name in dirs:
            for types in ["mp3", "wav"]:
                if file_name.find(types) != -1:
                    if not renpy.android:
                        catched.append((np_globals.Catch + "/" +file_name).replace("\\","/"))
                    else:
                        catched.append(file_name)
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
        if song is None:
            song = Music_GetCatchSaveList()     # 每次调用都重新扫描缓存目录
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

    def Music_Play_Random(fadein=1.2, loop=True, fadeout=1.2, if_changed=False):
        """
        随机播放已缓存的音乐列表
        IN:
            fadein - 过度渐入时间 (Default: 1.2)
            loop - 是否循环播放 (Default: True)
            fadeout - 过度渐出时间 (Default: 1.2)
            if_changed - 仅在歌曲改变时才切换 (Default: False)
        """
        import random
        Music_Deleteflac()
        songs_list = Music_GetCatchSaveList()
        if songs_list:
            random.shuffle(songs_list)
        Music_Play_List(
            song=songs_list,
            fadein=fadein,
            loop=loop,
            set_per=False,
            fadeout=fadeout,
            if_changed=if_changed
        )

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
            if renpy.android:
                song = (song + mtype)
            else:
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
    import sys

    if sys.version_info[0] >= 3:
        basestring = str
        unicode = str

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
            store.mas_submod_utils.submod_log.error("初始化连接时发生异常：{}".format(e))

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

        # 优先：随机播放缓存
        if store.persistent.np_start_randomplay:
            try:
                store.np_util.Music_Play_Random(fadein=1.2, loop=True, fadeout=1.2, if_changed=False)
            except Exception as e:
                store.mas_submod_utils.submod_log.error("随机播放缓存失败：{}".format(e))
            return

        # 其次：循环播放缓存
        if store.persistent.np_start_loopplay:
            try:
                store.np_util.Music_Play_List(song=store.np_util.Music_GetCatchSaveList(), fadein=1.2, loop=True, set_per=False, fadeout=1.2, if_changed=False)
            except Exception as e:
                store.mas_submod_utils.submod_log.error("播放缓存失败：{}".format(e))
            return

        # 最后：上次单曲
        if store.persistent.np_restart_song is not None and store.persistent.current_track is None:
            np_globals.Music_Type = store.persistent.np_restart_song_type
            try:
                np_util.Music_Play(store.persistent.np_restart_song)
            except Exception as e:
                store.mas_submod_utils.submod_log.error("播放文件失败：{}".format(e))

    # 在preloop label注册来实现自启播放
    store.mas_submod_utils.registerFunction('ch30_preloop', np_start_play)