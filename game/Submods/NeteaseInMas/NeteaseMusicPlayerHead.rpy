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
        description="在MAS里播放来自网易云的音乐.\n强烈建议使用{a=https://github.com/Legendkiller21/MAS-Submods-Paste}{i}{u}Paste{/u}{/i}{/a}子模组来进行复制粘贴操作。",
        version='1.1.0',
        settings_pane="np_setting_pane"
    )

init -5 python:
    _np_LoginPhone = ""
    _np_LoginPw = ""
    def np_login_ok():
        result = True
        if _np_LoginPhone == "" or _np_LoginPw == "":
            renpy.show_screen("np_message", message = "手机号/密码为空")
        else:    
            np_globals._LoginPhone = _np_LoginPhone
            np_globals._LoginPw =  _np_LoginPw
            result = np_util.Music_Login(np_globals._LoginPhone, np_globals._LoginPw)
        if not result:
            renpy.show_screen("np_message", message = "登录失败! \n1.首先检查账号密码是否正确.\n2.若密码正确, 等待2分钟后, 强制刷新登录(不是登录)即可.")
        renpy.hide_screen("np_login")
    
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
            

screen np_setting_pane():
    python:
        np_catchsize = np_util.Catch_size()/1000000
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
        text "- 正在播放: [np_globals.Music_Name] | [np_globals.Music_Alia] | [np_globals.Music_Author]"

        #> !已登录 ? 登陆账号 : 注销账号

        
        if not np_globals.Np_Status:
            textbutton "> 登录账号":
                action Show("np_login")
            textbutton "> 强制刷新登录":
                action Function(np_force_refresh)
        else:
            textbutton "> 注销账号":
                action Show("np_logout")
            textbutton "> 获取'我喜欢的音乐'":
                action Function(np_get_ml)
        
        textbutton "> 安全性问题说明":
            action Show("np_message", message = warn_message)

        if not np_globals.Np_Playing:
            textbutton "> 清理歌曲缓存 - [np_catchsize]MB":
                action Function(np_del_catch)
        else:
            textbutton "> 清理歌曲缓存 - [np_catchsize]MB (请在开始使用前清理缓存)"


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
                text "登录后, 可能会显示登陆失败, 如果账户密码正确只需要等待2分钟再刷新即可."
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


