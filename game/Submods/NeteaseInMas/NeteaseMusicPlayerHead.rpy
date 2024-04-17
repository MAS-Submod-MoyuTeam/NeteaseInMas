init -990 python:
    store.mas_submod_utils.Submod(
        author="P",
        name="Netease Music",
        description="在MAS里播放来自网易云的音乐.\n强烈建议使用{a=https://github.com/Legendkiller21/MAS-Submods-Paste}{i}{u}Paste{/u}{/i}{/a}子模组来进行复制粘贴操作。",
        version='1.8.0',
        settings_pane="np_setting_pane"
    )
init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Netease Music",
            user_name="MAS-Submod-MoyuTeam",
            repository_name="NeteaseInMas",
            update_dir="",
            attachment_id=None
        )

init -5 python:
    _np_LoginPhone = ""
    _np_LoginPw = ""
    _np_LoginCaptcha = ""
    def np_login_ok():
        result = True
        if _np_LoginPhone == "" or (_np_LoginPw == "" and _np_LoginCaptcha == ""):
            renpy.show_screen("np_message", message = "手机号/密码为空")
        else:    
            np_globals._LoginPhone = _np_LoginPhone
            np_globals._LoginPw =  _np_LoginPw
            np_globals._LoginCaptcha =  _np_LoginCaptcha
            if np_globals._LoginCaptcha == "":
                np_globals._LoginCaptcha = None
            result = np_util.Music_Login(np_globals._LoginPhone, np_globals._LoginPw, np_globals._LoginCaptcha)
        if not result:
            renpy.show_screen("np_message", message = "登录失败! 请检查账号密码是否正确!")
        renpy.hide_screen("np_login")
    
    def np_login_ok_e():
        result = True
        if _np_LoginPhone == "" or (_np_LoginPw == ""):
            renpy.show_screen("np_message", message = "邮箱/密码为空")
        else:    
            np_globals._LoginPhone = _np_LoginPhone
            np_globals._LoginPw =  _np_LoginPw
            np_globals._LoginCaptcha =  _np_LoginCaptcha
            if np_globals._LoginCaptcha == "":
                np_globals._LoginCaptcha = None
            result = np_util.Music_Login_e(np_globals._LoginPhone, np_globals._LoginPw, np_globals._LoginCaptcha)
        if not result:
            renpy.show_screen("np_message", message = "登录失败! 请检查账号密码是否正确!")
        renpy.hide_screen("np_login")

    def np_save_cookies():
        np_util.Save_Cookies(np_globals.Cookies)
    def np_refresh_cookies():
        np_util.Music_Login_Refresh()
    def np_get_phonecaptcha():
        np_globals._LoginPhone = _np_LoginPhone
        np_util.Music_Get_Captcha(np_globals._LoginPhone)

    def np_logout_method():
        np_util.Music_Logout()
        renpy.hide_screen("np_logout")
        
    def np_initFFmpeg():
        np_util.Init_FFmpeg()
        renpy.show_screen("np_message", message = "需要重启{b}电脑{/b}完成初始化")
    
    def np_force_refresh():
        a = np_util.Music_Login_Status()
        if a:
            renpy.show_screen("np_message", message = "在线!")
        else:
            renpy.show_screen("np_message", message = "离线!")

    def np_del_catch():
        np_util.Music_DeleteCatch()

    def np_get_ml():
        np_util.Get_User_Playlist()
        renpy.show_screen("np_message", message = "ok")

    def np_get_out_ip():
        np_util.Get_OutIp()
        renpy.show_screen("np_message", message = "ok")

    np_buttontip_login = "登录网易云音乐"
    np_buttontip_forcerefresh = "强制检测登录状态"
    np_buttontip_logout = "登出网易云音乐"
    np_buttontip_playermusiclist = "获取登录用户的'我喜欢'歌单"
    np_buttontip_refreshcookie = "用于刷新Cookies的有效时间(可能并不好用)"
    np_buttontip_whygetoutip = "重新获取本机的外部IP，用于刷新因为加速器导致定位ip在国外导致风控问题。"

screen np_setting_pane():
    python:
        np_screen_tt = store.renpy.get_screen("submods", "screens").scope["tooltip"]
        np_catchsize = round(np_util.Catch_size()/1024/1024, 2)
    $ warn_message = "Netease Music不会将您的密码上传至任何第三者, 且密码上传时先在本地使用MD5加密. 下载时要确保从正确的渠道下载，因为别人发的版本可能存在后门:)\n官方Github存储库：{a=https://github.com/MAS-Submod-MoyuTeam/NeteaseInMas}点我{/a}"
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
        text "- 正在播放: [np_globals.Music_Name] | [np_globals.Music_Alia] | [np_globals.Music_Author]"

        if np_globals.version is not None:
            text ("API版本：" + store.np_globals.version):
                xalign 1.0 yalign 0.0
                xoffset -10
                style "main_menu_version"
        else:
            text "API状态异常, 请检查连接性, 填写是否正确.":
                xalign 1.0 yalign 0.0
                xoffset -10
                style "main_menu_version"
        #> !已登录 ? 登陆账号 : 注销账号

        if not np_globals.Np_Status:
            textbutton "> 扫码登陆 <当前暂不支持, 请前往设置手动设置歌单id>"
                #action Show("np_login")
                #hovered SetField(np_screen_tt, "value", np_buttontip_login)
                #unhovered SetField(np_screen_tt, "value", np_screen_tt.default)
            #textbutton "> 强制刷新登录":
            #    action Function(np_force_refresh)
            #    hovered SetField(np_screen_tt, "value", np_buttontip_forcerefresh)
            #    unhovered SetField(np_screen_tt, "value", np_screen_tt.default)
        else:
            #textbutton "> 注销账号":
            #    action Show("np_logout")
            #    hovered SetField(np_screen_tt, "value", np_buttontip_logout)
            #    unhovered SetField(np_screen_tt, "value", np_screen_tt.default)
            textbutton "> 获取'我喜欢的音乐'":
                hovered SetField(np_screen_tt, "value", np_buttontip_playermusiclist)
                unhovered SetField(np_screen_tt, "value", np_screen_tt.default)
                action Function(np_get_ml)
            #textbutton "> 手动保存Cookies":
            #    action Function(np_save_cookies)
            #textbutton "> 手动刷新Cookies":
            #    hovered SetField(np_screen_tt, "value", np_buttontip_refreshcookie)
            #    unhovered SetField(np_screen_tt, "value", np_screen_tt.default)
            #    action Function(np_refresh_cookies)
        
        textbutton "> 安全性问题说明":
            action Show("np_message", message = warn_message)

        textbutton "> 清理歌曲缓存 - [np_catchsize]MB":
            action Function(np_del_catch)

        textbutton "> 重新获取本机IP":
            hovered SetField(np_screen_tt, "value", np_buttontip_whygetoutip)
            unhovered SetField(np_screen_tt, "value", np_screen_tt.default)
            action Function(np_get_out_ip)

        if np_globals.debug:
            textbutton "> debug":
                action Show("np_debug")
        #textbutton "> 请务必点我初始化服务!":
        #    action Function(np_initFFmpeg)

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
                text "提示：如果手机验证码不为空，那么将无视密码的输入"
                text "请注意关闭加速器/梯子，否则可能无法登录"

            hbox:
                textbutton "<点击输入手机号/163邮箱>":
                    action Show("np_login_input",message = "请输入手机号/163邮箱",returnto = "_np_LoginPhone")
            hbox:
                textbutton "<点击输入密码>":
                    action Show("np_login_input",message = "请输入密码",returnto = "_np_LoginPw")
            hbox:
                textbutton "<点击输入手机验证码>":
                    action Show("np_login_input",message = "请输入手机验证码",returnto = "_np_LoginCaptcha")
                label "     "
                textbutton "<获取验证码>":
                    action Function(np_get_phonecaptcha)
            hbox:
                text ""
            hbox:
                textbutton "手机登录":
                    action Function(np_login_ok)
                textbutton "邮箱登录":
                    action Function(np_login_ok_e)
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

screen np_scrollable_menu(items, display_area, scroll_align, nvm_retry, nvm_quit):
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
                    for id, name, author, alias, showname in items:
                        textbutton showname:
                            xsize display_area[2]
                            action Return(id)

            textbutton _(nvm_retry) action Return(0) xsize display_area[2]
            textbutton _(nvm_quit) action Return(-1) xsize display_area[2]


        bar:
            style "classroom_vscrollbar"
            value YScrollValue("viewport")
            xalign scroll_align

screen np_input_screen(prompt):
    default np_input = store.np_screen_util.NpInputValue()

    style_prefix "input"

    window:
        hbox:
            style_prefix "quick"
            xfill True
            xmaximum 0#(None if not has_history else 232)
            xalign 0.5
            yalign 0.995

            textbutton _("算了"):
                selected False
                action Return("User_Canceled")

#            有一点点想实现搜索历史的想法，不过摸了
#            if has_history:
#                if renpy.get_screen("ytm_history_submenu") is None:
#                    textbutton _("Show previous tracks"):
#                        selected False
#                        action ShowTransient("ytm_history_submenu")
#
#                else:
#                    textbutton _("Hide previous tracks"):
#                        selected False
#                        action Hide("ytm_history_submenu")
#
        vbox:
            align (0.5, 0.5)
            spacing 30

            text prompt style "input_prompt"
            input:
                id "input"
                value np_input


# Music menu
#
# IN:
#   music_list - current page of music
#   page_num - current page number
#   more_pages - true if there are more pages left
#
screen np_music_menu(music_list, page_num=0, more_pages=False):
    modal True

    $ import store.songs as songs

    zorder 200

    style_prefix "music_menu"

    frame:
        style "music_menu_outer_frame"

        hbox:

            frame:
                style "music_menu_navigation_frame"

            frame:
                style "music_menu_content_frame"

                transclude

        # this part copied from navigation menu
        vbox:
            style_prefix "music_menu"

            xpos gui.navigation_xpos
    #        yalign 0.4
            spacing gui.navigation_spacing

            # wonderful loop so we can dynamically add songs
            for id, name, artist, alias, showname in music_list:
                textbutton _(showname) action Return(id)

    vbox:

        yalign 1.0

        hbox:

            # dynamic prevous text, so we can keep button size alignments
            if page_num > 0:
                textbutton _("<<<< Prev"):
                    style "music_menu_prev_button"
                    action Return(page_num - 1)

            else:
                textbutton _(""):
                    style "music_menu_prev_button"
                    xsize 126
                    sensitive False

#                if more_pages:
#                    textbutton _(" | "):
#                        xsize 50
#                        text_font "gui/font/Halogen.ttf"
#                        text_align 0.5
#                        sensitive False

            if more_pages:
                textbutton _("Next >>>>"):
                    style "music_menu_return_button"
                    action Return(page_num + 1)

        textbutton _(songs.NO_SONG):
            style "music_menu_return_button"
            action Return(-2)

        textbutton _("Return"):
            style "music_menu_return_button"
            action Return(-1)

    label "我喜欢的音乐"

# sets locks and calls hte appropriate screen
label display_np_music_menu:
    # set var so we can block multiple music menus
    python:
        import store.np_globals as np_globals
        import store.songs as songs
        songs.menu_open = False
        np_globals.menu_open = True
        song_selected = False
        curr_page = np_globals.curr_page
        try:
            renpy.hide_screen("music_menu")
        except:
            pass

    # loop until we've selected a song
    while not song_selected:
        $ subpllist = np_globals.Play_List[curr_page*10 :curr_page*10 + 10]
        # setup pages
        if subpllist is None:
            # this should never happen. Immediately quit with None
            return songs.NO_SONG

        # otherwise, continue formatting args
        python:
            max_page = len(np_globals.Play_List) // 10
            if curr_page + 1 > max_page:
                more_pages = False
            else:
                more_pages = True

        call screen np_music_menu(subpllist, page_num=curr_page, more_pages=more_pages)

        python:
            str1 = str("sdw12dwa")
            if _return == -1 or _return == -2:
                song_selected = True
            elif not type(_return) == type(str1):
                song_selected = False
                curr_page = _return
            else:
                song_selected = True
                
    $ np_globals.menu_open = False
    return _return

