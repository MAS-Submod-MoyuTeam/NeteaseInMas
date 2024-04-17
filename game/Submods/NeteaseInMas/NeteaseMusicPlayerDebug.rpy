init 999 python:
    if renpy.config.developer:
        np_globals.debug = True
init -4 python:
    _np_music_id = ""
    def np_debug_check():
        res = np_util.Music_Login_Status()
        str1 = ""
        if res == False:
            str1 = "Fail"
        else:
            str1 = "Login"
        renpy.show_screen("np_message", message = str1)
    def np_fastlogin():
        np_util.Music_Login(nidianniman, "noway")
        renpy.show_screen("np_message", message = "ok")
    def np_fastlogin_fail():
        raise Exception("6")
    def np_download_music():
        renpy.show_screen("np_login_input", message = "输入下载id", returnto = "_np_music_id", ok_action = Function(np_download_music_p2))

    def np_download_music_p2():
        renpy.hide_screen("np_login_input")
        if np_util.Music_Download(np_globals.Music_Id):
            np_globals.Music_Id = _np_music_id
            renpy.show_screen("np_message", message = "ok")
        else:
            renpy.show_screen("np_message", message = "fail")
    
    def np_music_tomp3():
        np_util.Music_EncodeMp3()
    
    def np_play_music():
        np_util.Music_Play(np_globals.Music_Id)
    def np_play_music2(id):
        np_util.Music_Play(id)
    
    def np_check_minfo():
        np_util.Music_GetDetail()


screen np_debug():
    modal True
    zorder 215

    style_prefix "confirm"

    frame:
        vbox:
            xfill True
            yfill False
            spacing 5
            hbox:
                text "APIurl: [np_globals.Mainurl]"
            hbox:
                text "Nickname:[np_globals.Np_NickName] | ReqCode:[np_globals.ReqCode]"
            hbox:
                text "Music_ID: [np_globals.Music_Id] | _np_music_id: [_np_music_id]"
            hbox:
                text "Playing: [np_globals.Music_Name] | music.playing: [renpy.music.get_playing()]"
            hbox:
                text "Author: [np_globals.Music_Author] | Alia: [np_globals.Music_Alia]"

            hbox:
                textbutton "立刻检查登陆状态":
                    action Function(np_debug_check)
                textbutton "快速登录sp":
                    action Function(np_fastlogin)
                textbutton "引发一个异常":
                    action Function(np_fastlogin_fail)
                textbutton "下载指定id歌曲":
                    action Function(np_download_music)
            hbox:
                textbutton "转码Music_ID":
                    action Function(np_music_tomp3)
                textbutton "播放Music_ID.mp3":
                    action Function(np_play_music)
                textbutton "播放1365873163":
                    action Function(np_play_music2, id = "1365873163")
                textbutton "查询Music_Id的详细信息":
                    action Function(np_check_minfo)
            hbox:
                textbutton "关闭":
                    action Hide("np_debug")



                    
init 5 python:
    if np_globals.debug:
        addEvent(
                Event(
                    persistent.event_database,          
                    eventlabel="np_search",        
                    category=["NP"],                   
                    pool=True,
                    unlocked=True
                )
            )
        addEvent(
                Event(
                    persistent.event_database,          
                    eventlabel="np_show_userplaylist",        
                    category=["NP"],                   
                    pool=True,
                    unlocked=True
                )
            )

label np_play1365873163:
    m "ok!"
    python:
        np_play_music2("1365873163")
    return