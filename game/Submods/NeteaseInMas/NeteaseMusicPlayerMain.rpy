 #歌曲URL dict["data"]["url"]
 #搜索id dict["result"][song]<循环>[id]/[name]/[author]
 #cookies dict["cookies"]
 
 #保存cookies：
 #先登录，然后cookies = a.cookies.get_dict()
 #a为login时的cookies
 #不要反复登录 会风控

init -5 python in np_globals:

    debug = True

    Basedir = renpy.config.basedir
    Catch = Basedir + "/game/Submods/NeteaseInMas/Catch"
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
    Music_Id = ""
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
    
 
    def Music_Login(phone,pw):
        #登录
        pw = str(pw)
        md5pw = hashlib.md5(pw.encode('utf-8'))
        url = np_globals.Mainurl + np_globals.PhoneLogin + str(phone) + np_globals.PhoneLoginPwMd5 + md5pw.hexdigest()
        login = requests.get(url, verify=np_globals.VerifyPath)
        np_globals.Cookies = login.cookies
        store.persistent.np_Cookie = login.cookies

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
            return False
        else:
            return result["data"]["profile"]["nickname"]

    def Music_Logout():
        """
        注销账号 删除所有的cookies
        """
        cookie = np_globals.Cookies
        url = np_globals.Mainurl + np_globals.logout
        requests.get(url, cookie = cookie, verify = np_globals.VerifyPath)
        np_globals.Cookies = None
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




label np_emptylabel():
    pass
    return