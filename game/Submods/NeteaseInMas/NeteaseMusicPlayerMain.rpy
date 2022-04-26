 #歌曲URL dict["data"]["url"]
 #搜索id dict["result"][song]<循环>[id]/[name]/[author]
 #cookies dict["cookies"]
 
 #保存cookies：
 #先登录，然后cookies = a.cookies.get_dicts()
 #a为login时的cookies
 #不要反复登录 会风控


init python:
    from urllib import urlopen
    from urllib import quote
    from urllib import urlretrieve
    import ssl
    import json
    import requests

    #关闭证书验证
    import ssl
    unverified = ssl._create_unverified_context()
    Basedir = renpy.config.basedir
    Catch = Basedir + "game/Submods/NeteaseInMas/Catch/"

    Mainurl = "https://netease-cloud-music-api-murex-gamma.vercel.app"
    PhoneLogin = "/login/cellphone?phone="
    PhoneLoginPw = "&password="
    REFRESH_LOGIN = "/login/refresh" #返回新cookie

    Search = "/search?keywords="
    Search_Limit = "&limit=10"
    Music_Check = "/check/music?id="
    Music_Downloadurl = "/song/download/url?id="

    Music_Id = ""


    def Music_Login():
        url = "https://netease-cloud-music-api-murex-gamma.vercel.app/login/cellphone?phone=15753515952&password=LOVEcxs2002"
        urlopen(url, context=unverified)

    def Music_Getid():
        return 0

    def Music_Download(id):
        id = str(id)
        url = Mainurl + Music_Downloadurl + id
        music = urlopen(url, context=unverified)
        getdata = json.loads(music.read())
        file_url = getdata["data"]["url"]
        if file_url == None:
            raise Exception("None")
        catch_location = Catch
        Music_Login()
        _music_download = urlopen(file_url, context=unverified)
        _music_data = _music_download.read()
        _flac = open(catch_location + id + ".flac", 'wb')
        _flac.write(_music_data)

    Music_Download(1860841248)

    