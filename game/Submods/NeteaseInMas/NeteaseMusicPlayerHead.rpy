init -990 python:
    store.mas_submod_utils.Submod(
        author="P",
        name="Netease Music",
        description="在MAS里播放来自网易云的音乐.\n强烈建议使用{a=https://github.com/Legendkiller21/MAS-Submods-Paste}{i}{u}Paste{/u}{/i}{/a}子模组来进行复制粘贴操作。",
        version='1.9.2',
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

    def np_force_refresh_playlist():
        np_globals.playlist_cache = []
        renpy.show_screen("np_message", message = "已清空歌单缓存，下次进入会重新加载")

    def np_force_refresh_cloud():
        np_globals.cloud_cache = []
        renpy.show_screen("np_message", message = "已清空云盘缓存，下次进入会重新加载")

    def np_toggle_unblock():
        persistent._np_unblock_enable = not persistent._np_unblock_enable
        if persistent._np_unblock_enable:
            renpy.show_screen("np_message", message = "已开启解灰\n灰色歌曲会尝试从其他平台获取音源")
        else:
            renpy.show_screen("np_message", message = "已关闭解灰")

    def np_randomplay():
        hide_extra_screen()
        renpy.call('np_random')
        renpy.jump('mas_extra_menu_close_p2')
        

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
            textbutton "> 扫码登陆":
                action Show("np_qrlogin")
                hovered SetField(np_screen_tt, "value", np_buttontip_login)
                unhovered SetField(np_screen_tt, "value", np_screen_tt.default)
            #textbutton "> 强制刷新登录":
            #    action Function(np_force_refresh)
            #    hovered SetField(np_screen_tt, "value", np_buttontip_forcerefresh)
            #    unhovered SetField(np_screen_tt, "value", np_screen_tt.default)
        else:
            textbutton "> 注销账号":
                action Show("np_logout")
                hovered SetField(np_screen_tt, "value", np_buttontip_logout)
                unhovered SetField(np_screen_tt, "value", np_screen_tt.default)
            textbutton "> 刷新我喜欢的音乐":
                action Function(np_force_refresh_playlist)
            textbutton "> 刷新云盘音乐":
                action Function(np_force_refresh_cloud)
            # textbutton "> 获取'我喜欢的音乐'":
            #     hovered SetField(np_screen_tt, "value", np_buttontip_playermusiclist)
            #     unhovered SetField(np_screen_tt, "value", np_screen_tt.default)
            #     action Function(np_get_ml)
            #textbutton "> 手动保存Cookies":
            #    action Function(np_save_cookies)
            #textbutton "> 手动刷新Cookies":
            #    hovered SetField(np_screen_tt, "value", np_buttontip_refreshcookie)
            #    unhovered SetField(np_screen_tt, "value", np_screen_tt.default)
            #    action Function(np_refresh_cookies)
        
        if persistent._np_unblock_enable:
            textbutton "> 灰色歌曲解灰：已开启":
                action Function(np_toggle_unblock)
            python:
                _src_display = persistent._np_unblock_source if persistent._np_unblock_source else "自动"
            textbutton "> 解灰音源：[_src_display]":
                action Show("np_unblock_source_menu")
        else:
            textbutton "> 灰色歌曲解灰：已关闭":
                action Function(np_toggle_unblock)
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

screen np_qrlogin():
    python:
        def _np_qrlogin_genimg():
            import time
            if (np_globals.QRLastQueryCode > 800):
                if (time.time() - np_globals.GetCaptchaTime) < 60:
                    renpy.notify("发送失败：发送太频繁，请等待{}s后重试".format(60 - (time.time() - np_globals.GetCaptchaTime)))
                    return False
            np_globals.QRData = np_util.Music_Get_QRBase64()
            np_globals.QRFileName = np_util.randompngname()
            np_util.Save_Image(np_globals.QRData[1], np_globals.QRImageDir + np_globals.QRFileName)
            np_globals.GetCaptchaTime = time.time()
        
        def _np_check_code():
            if not os.path.exists(np_globals.QRImageDir + np_globals.QRFileName) or np_globals.QRData == None:
                return 
            elif np_globals.QRLastQueryCode == 803:
                np_force_refresh()
                return
            else:
                np_util.Music_Check_Status(np_globals.QRData[0])
        
        def del_qrimage():
            try:
                import os
                os.remove(np_globals.QRImageDir + np_globals.QRFileName)
                np_globals.QRData = None
                np_globals.QRLastQueryCode = 0
            except Exception as e:
                pass

        def whattime():
            import time
            return time.time()


    modal True
    zorder 215

    style_prefix "confirm"
    
    frame:
        vbox:
            xfill False
            yfill False
            spacing 5

            timer 2.0 repeat (np_globals.QRLastQueryCode != 803) action Function(_np_check_code, _update_screens=True)

            hbox:
                if np_globals.QRData != None:
                    python:
                        import base64
                        qr_img = None
                        try:
                            # 提取 base64 数据部分（去掉前缀）
                            b64_str = np_globals.QRData[1]
                            if ',' in b64_str:
                                b64_str = b64_str.split(',')[1]
                            # 解码为二进制数据
                            img_data = base64.b64decode(b64_str)
                            # 直接生成 Ren'Py 图像对象，不读磁盘文件
                            qr_img = im.Data(img_data, np_globals.QRFileName)
                        except Exception as e:
                            pass
            
                    if qr_img is not None:
                        imagebutton:
                            insensitive qr_img
                            idle qr_img
                            hover qr_img
                            selected_idle qr_img
                            selected_hover qr_img
                    else:
                        text "等待生成二维码..."
                else:
                    text "等待生成二维码..."
            

            hbox:
                text "二维码状态: "
                if np_globals.QRLastQueryCode == 800:
                    text "已过期, 请重新生成"
                elif np_globals.QRLastQueryCode == 801:
                    text "请打开手机网易云音乐APP扫描二维码登陆"
                elif np_globals.QRLastQueryCode == 802:
                    text "请在手机网易云音乐APP中确认登陆"
                elif np_globals.QRLastQueryCode == 803:
                    text "授权登录成功"
                elif np_globals.QRLastQueryCode == 0:
                    text "请先生成二维码"
            hbox:
                text "{size=-10}很难扫？很难扫就对了, 我也很难扫, 网易云不会做扫码我来做"
            if config.debug:
                hbox:
                    text "QRLastQueryCode" + str(np_globals.QRLastQueryCode)
                hbox:
                    text str(whattime())
                hbox:
                    text str(np_globals.QRData)[:75]
                hbox:
                    text str(np_globals._QRCookie).replace("[", "")[:75]

            hbox:
                textbutton "关闭":
                    action [
                        Function(del_qrimage),
                        Hide("np_qrlogin")
                        ]
                
                if not os.path.exists(np_globals.QRImageDir + np_globals.QRFileName):
                    textbutton "生成二维码":
                        action Function(_np_qrlogin_genimg, _update_screens=True)
                else:
                    textbutton "生成二维码(请重新打开此页面)"

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
screen np_music_menu(music_list, page_num=0, more_pages=False, search_text="", search_active=False):
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

    vbox:
        xpos 200
        ypos 650
        spacing 8
        if search_active:
            text "搜索: [search_text]" size 18
            xoffset 20
            yoffset -30
            textbutton _("清除搜索"):
                action Return("__CLEAR_SEARCH__")
                # xoffset 20
                # yoffset -30
        else:
            textbutton _("搜索当前列表"):
                action Return("__SEARCH__")

    label "[np_globals.menu_title]"

# sets locks and calls hte appropriate screen
label display_np_music_menu:
    # set var so we can block multiple music menus
    python:
        import store.np_globals as np_globals
        import store.songs as songs
        songs.menu_open = False
        np_globals.menu_open = True
        song_selected = False
        curr_page = 0
        try:
            renpy.hide_screen("music_menu")
        except:
            pass

    # loop until we've selected a song
    while not song_selected:
        # 本地过滤，不发网络请求
        python:
            if np_globals.search_filter:
                _sl = np_globals.search_filter.lower()
                display_list = [s for s in np_globals.Play_List if _sl in s[4].lower()]
            else:
                display_list = list(np_globals.Play_List)

            # 搜索无结果的处理
            _empty_search = (len(display_list) == 0 and np_globals.search_filter)
            if _empty_search:
                np_globals.search_filter = ""
                display_list = list(np_globals.Play_List)

            # 列表为空，直接退出
            _list_empty = (len(display_list) == 0)

        if _empty_search:
            m 1eka "没有找到匹配的歌曲呢..."
        elif _list_empty:
            m 1eka "列表里没有歌呢..."
            $ song_selected = True

        if not _list_empty:
            python:
                max_page = (len(display_list) - 1) // 10
                if curr_page > max_page:
                    curr_page = 0
                subpllist = display_list[curr_page*10 : curr_page*10 + 10]
                more_pages = curr_page < max_page

            call screen np_music_menu(subpllist, page_num=curr_page, more_pages=more_pages, search_text=np_globals.search_filter, search_active=bool(np_globals.search_filter))

            if _return == "__SEARCH__":
                $ _sw = renpy.call_screen("np_music_search_input")
                if _sw:
                    $ np_globals.search_filter = _sw
                    $ curr_page = 0
            elif _return == "__CLEAR_SEARCH__":
                $ np_globals.search_filter = ""
                $ curr_page = 0
            elif _return == -1 or _return == -2:
                $ song_selected = True
            elif not isinstance(_return, str):
                $ curr_page = _return
            else:
                $ song_selected = True

    $ np_globals.menu_open = False
    $ np_globals.search_filter = ""
    return _return

#当前列表搜索输入
screen np_music_search_input():
    modal True
    zorder 250

    style_prefix "confirm"


    frame:
        align (0.5, 0.5)
        xsize 800
        xfill False
        yfill False

        vbox:
            xalign 0.5
            spacing 20

            label "搜索当前列表":
                style "confirm_prompt"
                xalign 0.5

            input:
                id "input"
                value VariableInputValue("np_search_input_value")
                length 80
                xalign 0.5
                xsize 600

            hbox:
                xalign 0.5
                spacing 60

                textbutton _("搜索"):
                    action Return(np_search_input_value)
                textbutton _("清空"):
                    action SetVariable("np_search_input_value", "")
                textbutton _("取消"):
                    action Return("")

# 灰色歌曲解灰音源选择
screen np_unblock_source_menu():
    modal True
    zorder 225

    style_prefix "confirm"

    frame:
        align (0.5, 0.5)
        xfill False
        yfill False

        vbox:
            spacing 5

            label "选择解灰音源":
                style "confirm_prompt"
                xalign 0.5

            textbutton "自动（推荐）":
                action [SetField(persistent, "_np_unblock_source", ""), Hide("np_unblock_source_menu")]
            textbutton "酷我 (kuwo)":
                action [SetField(persistent, "_np_unblock_source", "kuwo"), Hide("np_unblock_source_menu")]
            textbutton "酷狗 (kugou)":
                action [SetField(persistent, "_np_unblock_source", "kugou"), Hide("np_unblock_source_menu")]
            textbutton "咪咕 (migu)":
                action [SetField(persistent, "_np_unblock_source", "migu"), Hide("np_unblock_source_menu")]
            textbutton "QQ音乐 (qq)":
                action [SetField(persistent, "_np_unblock_source", "qq"), Hide("np_unblock_source_menu")]
            textbutton "B站 (bilibili)":
                action [SetField(persistent, "_np_unblock_source", "bilibili"), Hide("np_unblock_source_menu")]
            textbutton "网易云原生 (netease)":
                action [SetField(persistent, "_np_unblock_source", "netease"), Hide("np_unblock_source_menu")]

            textbutton "关闭":
                action Hide("np_unblock_source_menu")