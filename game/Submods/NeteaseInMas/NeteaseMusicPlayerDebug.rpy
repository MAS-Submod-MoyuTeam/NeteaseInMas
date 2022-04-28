init -5 python:
    def np_debug_check():
        res = np_util.Music_Login_Status()
        str1 = ""
        if res == False:
            str1 = "Fail"
        else:
            str1 = "Login"
        renpy.show_screen("np_message", message = str1)
    def np_fastlogin():
        np_util.Music_Login(15753515952, "LOVEcxs2002")
        renpy.show_screen("np_message", message = "ok")
    def np_fastlogin_fail():
        np_util.Music_Login("31423423", "-1234")
        renpy.show_screen("np_message", message = "ok")
    def np_download_music(id):
        pass
        



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
                text "Nickname:[np_globals.Np_NickName]"

            hbox:
                textbutton "立刻检查登陆状态":
                    action Function(np_debug_check)
                textbutton "快速登录sp":
                    action Function(np_fastlogin)
                textbutton "快速登录 - 异常情况":
                    action Function(np_fastlogin_fail)
                textbutton "初始化FFmpeg环境变量":
                    action Function(np_initFFmpeg)
                textbutton "下载指定id歌曲":
                    action Show("np_login_input")
            hbox:
                textbutton "关闭":
                    action Hide("np_debug")



                    