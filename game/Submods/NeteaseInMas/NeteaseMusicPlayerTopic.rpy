define NP_DOWNMODE1 = 1
define NP_DOWNMODE2 = 2
default persistent._np_playmode = NP_DOWNMODE1
default persistent._np_max_retry = 9
define NP_CONMODE_MP3 = 1
define NP_CONMODE_WAV = 2
default persistent.np_start_loopplay = False
default persistent._np_downtimeout = 100
init 5 python:
    addEvent(
            Event(
                persistent.event_database,          
                eventlabel="np_search",        
                category=["Netease Music"],           
                prompt="搜一首歌",        
                pool=True,
                unlocked=True
            ),
        restartBlacklist=True
        )
init 5 python:
    addEvent(
            Event(
                persistent.event_database,          
                eventlabel="np_loop",        
                category=["Netease Music"],           
                prompt="循环播放缓存",        
                pool=True,
                unlocked=True
            ),
        restartBlacklist=True
        )
label np_loop:
    $ hide_extra_screen()
    $ np_util.Music_Play_List()
    m "ok"
    return

label np_search:
    $ response_quips = [
        "想听什么?",
        "[player], 今天想听什么呢?",
        "我们今天听什么?",
        "今天听什么呢, [mas_get_player_nickname()]"
    ]
    $ response_quip = renpy.substitute(renpy.random.choice(response_quips))
    $ _Search_Word = mas_input(
            "[response_quip]",
            length=80,
            screen="np_input_screen"
        ).strip('\t\n\r')
    if not _Search_Word == "User_Canceled":
        $ np_globals.Search_Word = _Search_Word
    else:
        m 1eka "那就下次吧."
        return
    if np_globals.Search_Word == "":
        m 1ekb "啊, 是空的呢...要再试一遍吗?"
        call np_search
    else:
        m 2duc "等我去搜一下...{nw}"
        $ store.np_util.Music_Search(np_globals.Search_Word)
        call np_menu_display
    return
label np_menu_display:
    if len(np_globals.Search_List) > 0:
        m 3eub "我找到了这些, 你看看有没有你想听的."
        call screen np_scrollable_menu(np_globals.Search_List, np_globals.SCR_MENU_AREA, np_globals.SCR_MENU_XALIGN, "重新搜一首", "算了")
        if _return == -1:
            m 1eka "好吧."
            m 3ekb "那我们下次再来~"
            return    
        elif _return == 0:
            m 1hua "好的."
            jump np_search
        else:
            m 1hua "好~{w=1}{nw}"
            if not np_globals.Np_Status and persistent._np_playmode == NP_DOWNMODE2:
                m 3rksdra "呃...我们好像忘记登录了..."
                m 3hksdrb "去设置里登录一下吧, [player]."
                return
            $ np_globals.Music_Id = _return
            call np_play_musicid
    else:
        m 1eud "呃...[player]"
        m 3rub "我什么都没找到, 要不我们换一首?" 
    return
label np_play_musicid:
    python:
        catched = False
    if np_globals.Np_Status or persistent._np_playmode == NP_DOWNMODE1: 
        call np_timed_text_events_prep
        m 1dsc "等我下好这首歌...{nw}"
        python:
            import os
            if os.path.exists(np_globals.Catch + "/" + np_globals.Music_Id + ".mp3") or os.path.exists(np_globals.Catch + "/" + np_globals.Music_Id + ".wav"):
                # 本地存在缓存
                catched = True
                # 根据缓存类型判断播放的格式
                if os.path.exists(np_globals.Catch + "/" + np_globals.Music_Id + ".mp3"):
                    np_globals.Music_Type = "mp3"
                else:
                    np_globals.Music_Type = "wav"
        if not catched:
            if persistent._np_playmode == NP_DOWNMODE2:
                $ res = mas_threading.MASAsyncWrapper(np_util.Music_Download, [np_globals.Music_Id])
            else:
                $ res = mas_threading.MASAsyncWrapper(np_util.Music_Download_2, [np_globals.Music_Id])
            $ res.start()
            python:
                stat = False
                catchsize1 = round(np_util.Catch_size()/1024/1024, 2)
                catchsize2 = 0
                t=0
                while not stat:
                    catchsize2 = round(np_util.Catch_size()/1024/1024, 2)
                    downsize = round((catchsize2 - catchsize1)/0.75, 2)
                    t=t+1
                    if t > persistent._np_downtimeout:
                        stat=None
                        break
                    if t > 20:
                        renpy.say(m, "([downsize]MB/S)([t]/[persistent._np_downtimeout])等我下好这首歌{fast}.{w=0.25}.{w=0.25}.{w=0.25}{nw}")
                    elif t > 1:
                        renpy.say(m, "([downsize]MB/S)等我下好这首歌{fast}.{w=0.25}.{w=0.25}.{w=0.25}{nw}")
                    else:
                        renpy.say(m, "等我下好这首歌{fast}.{w=0.25}.{w=0.25}.{w=0.25}{nw}")
                    _history_list.pop()
                    stat = res.get()
                    catchsize1 = catchsize2
                    if stat == False:
                        break
            if stat == True:
                m 1ksa "好了~{w=0.3}{nw}"
            elif stat == False:
                m 3rksdlb "这首歌我下不了, [player].{w=1.2}{nw}"
                m "多半是因为网易云没有版权, 换一首或重试一下吧.{w=1.2}{nw}"
                $ res.end()
                call np_timed_text_events_wrapup
                return
            else:
                m 3rksdlb "下载的时间有点久...{w=1.2}{nw}"
                m "重试一下吧~{w=1.2}{nw}"
                $ res.end()
                call np_timed_text_events_wrapup
                return

            if np_globals.Music_Type != "mp3":
                $ a = mas_threading.MASAsyncWrapper(np_util.Music_ToWav)
                $ a.start()
                m 1eua "等我把这首歌转码好.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
            else:
                catched = True
        python:
            import time, os
            retry = 0
            FAILED = False
            npsong = (np_globals.Catch + "/" + np_globals.Music_Id + '.' +  np_globals.Music_Type).replace("\\","/")
            while True:
                if not a.get() is None and catched == False:
                    renpy.notify("转码时间比预计要长一些...\n最多重试[persistent._np_max_retry]次")
                    _history_list.pop()
                    retry = retry + 1
                    if retry > persistent._np_max_retry:
                        FAILED = True
                        break
                    renpy.say(m, "第[retry]次重试...{w=1.5}{nw}")
                else:
                    np_util.Music_Play(np_globals.Music_Id)
                    break
        if FAILED:
            call np_timed_text_events_wrapup
            m 3rksdlb "出了点问题...我没法播放这首歌..."
            m "再试一遍如何, [player]?"
            show monika idle
            return
        python:
            try:
                np_util.Music_GetDetail()
            except:
                # 重试一遍
                try:
                    np_util.Music_GetDetail()
                except Exception as e:
                    store.mas_submod_utils.submod_log.error("查询歌曲信息失败：{}".format(e))
        $ np_util.Music_Deleteflac()
        m 3hub "搞定~{w=3}{nw}"
        call np_timed_text_events_wrapup
        python:
            egglabel = np_check_eggs(np_globals.Music_Name)
            if egglabel != "":
                if not renpy.seen_label(egglabel):
                    renpy.call(egglabel)
    elif persistent._np_playmode == NP_DOWNMODE2:
        m 3rksdra "呃...我们好像忘记登录了..."
        m 3hksdrb "去设置里登录一下吧, [player]."
    else:
        m "似乎出了一些意外问题..."
        m "重试一下吧, [player]"
    show monika idle
    return
init 5 python:
    addEvent(
            Event(
                persistent.event_database,          
                eventlabel="np_show_userplaylist",        
                category=["Netease Music"],           
                prompt="[player]喜欢的音乐",        
                pool=True,
                unlocked=True
            ),
        restartBlacklist=True
        )
label np_show_userplaylist:
    python:  
        try:
            renpy.hide_screen("music_menu")
            store.songs.menu_open = False
        except:
            pass
    if not np_globals.Np_Status:
        m 3rksdra "呃...我们好像忘记登录了..."
        m 3hksdrb "去设置里登录一下吧, [player]."
        return
    if not len(np_globals.Play_List) > 0:
        m 1eka "呃...我还不知道你喜欢听什么呢.{w=2}{nw}"
        m 1dua "等我一下...{nw}"
        python:
            a = mas_threading.MASAsyncWrapper(np_util.Get_User_Playlist)
            a.start()
            stat = False
            while not stat:
                 renpy.say(m, "等我一下{fast}.{w=0.15}.{w=0.15}.{w=0.15}{nw}")
                 _history_list.pop()
                 stat = a.done()

        m 1eub "我知道你喜欢什么了哦, [player].{w=2}{nw}"
    call display_np_music_menu
    if _return == None or _return == "":
        m 3rka "None"
        return
    if _return == -1:
        $ renpy.hide_screen("np_music_menu")
        $ np_globals.menu_open = False
        return
    if _return == -2:
        $ play_song(None)
        $ renpy.hide_screen("np_music_menu")
        $ np_globals.menu_open = False
        return
    $ np_globals.Music_Id = _return
    call np_play_musicid
    return

init 5 python:
    addEvent(
            Event(
                persistent.event_database,          
                eventlabel="np_show_setting",        
                category=["Netease Music"],           
                prompt="设置",        
                pool=True,
                unlocked=True
            ),
        restartBlacklist=True
        )
label np_show_setting:
    python:
        if persistent._np_playmode == 1:
            mode = "song/id(MODE1)"
        elif persistent._np_playmode == 2:
            mode = "song/download/id(MODE2)"
        else:
            mode = "?"

    menu:
        "请选择设置项"
        "下载模式":
            "下载模式有两个选项"
            "接口song/id和song/download/id"
            "song/id可以在非登录状态使用，而song/download/id必须登录使用"
            "song/id主要用于试听歌曲"
            "song/download/id用于客户端下载歌曲"
            "使用 /song/url 接口获取的是歌曲试听 url, 但存在部分歌曲在非 VIP 账号上可以下载无损音质而不能试听无损音质, 使用song/download/id可使非 VIP 账号获取这些歌曲的无损音频"
            "一般两个下载接口没有下载速度区别，而且下载时会下载能获取到的最高音质（一首flac格式占用50MB左右，而mp3约为10MB）"
            "两者都无法播放无版权音乐和需要黑胶VIP的音乐"
            menu:
                "请选择下载模式, 当前为[mode]"
                "song/id":
                    $ persistent._np_playmode = NP_DOWNMODE1
                "song/download/id":
                    $ persistent._np_playmode = NP_DOWNMODE2
        "搜索结果数":
            "决定了搜索歌曲返回的结果数量"
            $ persistent._NP_search_limit = str(mas_input("输入非数字可能会导致异常, 当前为[persistent._NP_search_limit]"))
            $ np_globals.SearchLimit = persistent._NP_search_limit
        "最大重试次数":
            "在播放歌曲时，转码后的最大尝试播放次数，默认为9"
            "每次重试的间隔为1.5s"
            $ persistent._np_max_retry = str(mas_input("输入非数字可能会导致异常, 当前为[persistent._np_max_retry]"))
        "下载等待最大次数":
            "下载时等待的最高次数，默认为100"
            $ persistent._np_downtimeout = int(mas_input("输入非数字可能会导致异常, 当前为[persistent._np_max_retry]"))
        "启动时播放缓存":
            "这将导致启动后不会播放上次播放的歌曲，而是自动播放已经缓存过的所有歌曲"
            "如果在播放缓存期间删除缓存，可能会导致异常"
            menu:
                "当前：[persistent.np_start_loopplay]"
                "启用":
                    $ persistent.np_start_loopplay = True
                "禁用":
                    $ persistent.np_start_loopplay = False
                
        "算了":
            return
    
    "设置完成"
    return

label np_timed_text_events_prep:
    python:
        renpy.pause(0.5)

        # raise shield
        mas_RaiseShield_timedtext()

        # store and disable auto-forward pref
        afm_pref = renpy.game.preferences.afm_enable
        renpy.game.preferences.afm_enable = False

    return

label np_timed_text_events_wrapup:
    python:
        renpy.pause(0.5)

        # drop shield
        mas_DropShield_timedtext()

        # restor auto-forward pref
        renpy.game.preferences.afm_enable = afm_pref

    # 展示莫妮卡为闲置状态以防万一
    show monika idle
    return

