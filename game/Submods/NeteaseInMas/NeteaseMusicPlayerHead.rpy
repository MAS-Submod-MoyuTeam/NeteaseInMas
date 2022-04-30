#    todo:
#        界面:
#            - 登录
#            - 刷新登录缓存 X - 无法实现
#            - 正在播放
#            - 清除下载歌曲
init -990 python:
    store.mas_submod_utils.Submod(
        author="P",
        name="Netease Music",
        description="在MAS里播放来自网易云的音乐.",
        version='0.0.1',
        settings_pane="np_setting_pane"
    )

init -5 python:
    _np_LoginPhone = ""
    _np_LoginPw = ""
    def np_login_ok():
        result = True
        if _np_LoginPhone == "" or _np_LoginPw == "":
            renpy.show_screen("np_message", message = "你忘了一个吧?")
        else:    
            np_globals._LoginPhone = _np_LoginPhone
            np_globals._LoginPw =  _np_LoginPw
            result = np_util.Music_Login(np_globals._LoginPhone, np_globals._LoginPw)
        if not result:
            renpy.show_screen("np_message", message = "登录失败! 是不是账号密码填错了?")
        renpy.hide_screen("np_login")
    
    def np_logout_method():
        np_util.Music_Logout()
        renpy.hide_screen("np_logout")
        
    def np_initFFmpeg():
        np_util.Init_FFmpeg()
        renpy.show_screen("np_message", message = "需要重启{b}电脑{/b}完成初始化")

screen np_setting_pane():
    $ warn_message = "Netease Music不会将您的密码上传至除我(P)以外的第三者, 且密码上传时使用MD5加密.但请注意, 登录时关闭了证书验证(因为开启就验证失败), 所以仍然有一定的可能性导致被盗号.\n如果真的被盗号, 通常是因为你下了别人发的版本/你的PC上有病毒,MD5没那么好破"
#    """
#    Submod菜单:
#        计划格式:
#            > !已登录 ? 登陆账号 : 注销账号
#            > - 当前登录: <用户名>
#            > - 正在播放: <歌曲>
#            > 安全性问题说明
#            > 清理歌曲缓存
#            > debug
#    """
    vbox:
        xmaximum 800
        xfill True
        style_prefix "check"

        text "- 当前登录: [np_globals.Np_NickName]"
        text "- 正在播放: [np_globals.Music_Name] | [np_globals.Music_Author]"

        #> !已登录 ? 登陆账号 : 注销账号

        
        if not np_globals.Np_Status:
            textbutton "> 登录账号":
                action Show("np_login")
        else:
            textbutton "> 注销账号":
                action Show("np_logout")
        
        textbutton "> 安全性问题说明":
            action Show("np_message", message = warn_message)


        textbutton "> 清理歌曲缓存"

        if np_globals.debug:
            textbutton "> debug":
                action Show("np_debug")
        if persistent.Np_InitedFFmpeg:
            textbutton "///{b}第一次使用,请点我初始化服务{/b}///":
                action Function(np_initFFmpeg)

screen np_login():
    modal True
    zorder 215

    style_prefix "confirm"

    frame:
        vbox:
            xfill False
            yfill False
            spacing 5
            hbox:
                text "登录系统不是很稳定, 可能需要等待几分钟后再检查. 切勿短时间内反复登录, 可能会导致风控."
            hbox:
                text "登陆后, 界面不会实时更新, 您可以切换至其他窗口（如：设置）再切换回来即可更新状态."
            hbox:
                text "尽量避免在其他位置登录您的网易云账号:)\n"

            hbox:
                textbutton "<点击输入手机号>":
                    action Show("np_login_input",message = "请输入手机号",returnto = "_np_LoginPhone")
            hbox:
                textbutton "<点击输入密码>":
                    action Show("np_login_input",message = "请输入密码",returnto = "_np_LoginPw")
            hbox:
                text ""
            hbox:
                textbutton "登录":
                    action Function(np_login_ok)
                textbutton "关闭":
                    action Hide("np_login")



screen np_login_input(message, returnto, ok_action = Hide("np_login_input")):
    #登录输入账户窗口, 也用来用作通用的输入窗口
    ## Ensure other screens do not get input while this screen is displayed.s
    modal True
    zorder 225

    style_prefix "confirm"

    frame:
        vbox:
            ymaximum 300
            xmaximum 800
            xfill True
            yfill False
            spacing 5

            label _(message):
                style "confirm_prompt"
                xalign 0.5
            hbox:
                input default "" value VariableInputValue(returnto) length 64

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action ok_action

screen np_logout():
    ## Ensure other screens do not get input while this screen is displayed.
    modal True
    zorder 225

    style_prefix "confirm"

    frame:
        vbox:
            ymaximum 300
            xmaximum 800
            xfill True
            yfill False
            spacing 5

            hbox:
                text "你确定要注销账号吗?"
            hbox:
                textbutton "确定":
                    action Function(np_logout_method)
                textbutton "取消":
                    action Hide("np_logout")

                

screen np_message(message = "Non Message", ok_action = Hide("np_message")):
    #np通用消息信息
    ## Ensure other screens do not get input while this screen is displayed.
    modal True
    zorder 225

    style_prefix "confirm"

    frame:
        vbox:
            ymaximum 300
            xmaximum 800
            xfill True
            yfill False
            spacing 5

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            #input default "" value VariableInputValue("savefile") length 25

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action ok_action

screen scrollable_menu(items, display_area, scroll_align, nvm_text, remove=None):
    style_prefix "scrollable_menu"

    fixed:
        area display_area

        vbox:
            ypos 0
            yanchor 0

            viewport:
                id "viewport"
                yfill False
                mousewheel True

                vbox:
                    for i_caption, i_label in items:
                        textbutton i_caption:
                            if renpy.has_label(i_label) and not seen_event(i_label):
                                style "scrollable_menu_new_button"

                            elif not renpy.has_label(i_label):
                                style "scrollable_menu_special_button"

                            action Return(i_label)

            null height 20

            if remove:
                # in case we want the option to hide this menu
                textbutton _(remove[0]) action Return(remove[1])

            textbutton _(nvm_text) action Return(False)

        bar:
            style "classroom_vscrollbar"
            value YScrollValue("viewport")
            xalign scroll_align



