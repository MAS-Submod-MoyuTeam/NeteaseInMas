define NP_DOWNMODE1 = 1
define NP_DOWNMODE2 = 2
default persistent._np_playmode = NP_DOWNMODE1
default persistent._np_max_retry = 9
define NP_CONMODE_MP3 = 1
define NP_CONMODE_WAV = 2
define persistent._np_conmode = NP_CONMODE_WAV
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
                $ res = np_util.Music_Download(np_globals.Music_Id)
            else:
                $ res = np_util.Music_Download_2(np_globals.Music_Id)
            if res:
                m 1ksa "好了~{w=0.3}{nw}"
            else:
                m 3rksdlb "这首歌我下不了, [player].{w=1.2}{nw}"
                m "多半是因为网易云没有版权, 换一首吧.{w=1.2}{nw}"
                call np_timed_text_events_wrapup
                return
            python:
                if np_globals.Music_Type == "mp3":
                    speed = 4500.0
                elif np_globals.Music_Type == 'wav':
                    speed = 30000
                else:
                    speed = 4500
                wtime = np_globals.Music_Size / 1024 / speed
                if wtime > 20:
                    wtime = 20
                elif wtime < 4:
                    wtime = 4
            
            if np_globals.debug:
                m 1esa "预计时间:[wtime]{nw}"
            if np_globals.Music_Type != "mp3":
                $ np_util.Music_ToWav()
                m 1eua "接下来...等音乐转码完就好了...{w=[wtime]}{nw}"
            
        python:
            import time
            playable = False
            retry = 0
            FAILED = False
            while not playable:
                try:
                    np_util.Music_Play(np_globals.Music_Id)
                    playable = True
                except:
                    renpy.notify("转码时间比预计要长一些...\n最多重试[persistent._np_max_retry]次")
                    retry = retry + 1
                    time.sleep(1.5)
                    if retry > persistent._np_max_retry:
                        FAILED = True
                        break
                    renpy.say(m, "第[retry]次重试...{nw}")
        if FAILED:
            call np_timed_text_events_wrapup
            m 3rksdlb "出了点问题...我没法播放这首歌..."
            m "再试一遍如何, [player]?"
            return
        $ np_util.Music_GetDetail()
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
        $ np_util.Get_User_Playlist()
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
            "song/id对于部分歌曲(需要VIP)可能只能播放试听片段"
            "song/id的加载速度更快"
            "song/download/id的音质比song/id更好"
            "如果你能登录，请优先使用song/download/id, song/id在登录/非登录状态可能有两种类型，可能更容易出bug"
            "两者都无法播放无版权音乐和需要黑胶VIP的音乐"
            menu:
                "请选择播放模式, 当前为[mode]"
                "song/id":
                    $ persistent._np_playmode = NP_DOWNMODE1
                "song/download/id":
                    $ persistent._np_playmode = NP_DOWNMODE2
        #"转码格式": - 导致了太多bug，强制为.wav
        #    "当下载的音乐格式不支持(flac)时, 会调用ffmpeg进行转码, 通常出现于song/download/id"
        #    "转码为MP3存储占用较低, 通常来说flac转为mp3会导致音质损失，而且速度相比于WAV极慢"
        #    "转码为WAV不会有音质损失, 存储占用较高，但是几乎瞬间转码完成"
        #    "如果下载原格式为MP3, 则不会进行转码"
        #    menu:
        #        "请选择转码模式, 当前为[persistent._np_conmode]"
        #        "mp3":
        #            $ persistent._np_conmode = NP_CONMODE_MP3
        #        "wav":
        #            $ persistent._np_conmode = NP_CONMODE_WAV
        "搜索结果数":
            "决定了搜索歌曲返回的结果数量"
            $ persistent._NP_search_limit = str(mas_input("输入非数字可能会导致异常, 当前为[persistent._NP_search_limit]"))
            $ np_globals.SearchLimit = persistent._NP_search_limit
        "最大重试次数":
            "在播放歌曲时，转码后的最大尝试播放次数，默认为9"
            "每次重试的间隔为1.5s"
            $ persistent._np_max_retry = str(mas_input("输入非数字可能会导致异常, 当前为[persistent._np_max_retry]"))
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

