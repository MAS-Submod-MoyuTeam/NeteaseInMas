init 5 python:
    addEvent(
            Event(
                persistent.event_database,          
                eventlabel="np_search",        
                category=["Netease Music"],           
                prompt="搜一首歌",        
                pool=True,
                unlocked=True
            )
        )
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
        m "那就下次吧."
        return
    if np_globals.Search_Word == "":
        m "是空的欸...再试一遍?"
        call np_search
    else:
        m "等我去搜一下...{nw}"
        #$ store.np_threading.Music_Search
        $ store.np_util.Music_Search(np_globals.Search_Word)
        call np_menu_display
    return
label np_menu_display:
    if len(np_globals.Search_List) > 0:
        m "我找到了这些, 你看看有没有你想听的."
        call screen np_scrollable_menu(np_globals.Search_List, np_globals.SCR_MENU_AREA, np_globals.SCR_MENU_XALIGN, "重新搜一首", "算了")
        if _return == -1:
            m "好吧."
            m "那我们下次再来~"
            return    
        elif _return == 0:
            m "好的."
            jump np_search
        else:
            m "好~{w=1}{nw}"
            $ np_globals.Music_Id = _return
            call np_play_musicid
    else:
        m "呃...[player]"
        m "我什么都没找到, 要不我们换一首?" 
    return
label np_play_musicid:
    python:
        catched = False
    if np_globals.Np_Status: 
        call mas_timed_text_events_prep
        m "等我下好这个歌...{nw}"
        python:
            import os
            if os.path.exists(np_globals.Catch + "/" + np_globals.Music_Id + ".mp3"):
                catched = True
        if not catched:
            $ np_util.Music_Download(np_globals.Music_Id)
            m "好了~{nw}"
            python:
                if np_globals.Music_Type == "mp3":
                    speed = 4500.0
                else:
                    speed = 3250.0
                wtime = np_globals.Music_Size / 1024 / speed
                if wtime > 20:
                    wtime = 20
                elif wtime < 8:
                    wtime = 8
            
            if np_globals.debug:
                m "预计时间:[wtime]{nw}"
            $ np_util.Music_EncodeMp3()
            m "接下来...等音乐转码完就好了...{w=[wtime]}{nw}"
            call mas_timed_text_events_wrapup
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
                        retry = retry + 1
                        platable = False
                        time.sleep(1.5)
                        if retry > 7:
                            FAILED = True
                            break
                        renpy.say(m, "第[retry]次重试...")
            if FAILED:
                m "出了点问题...我没法播放这首歌..."
                return
        $ np_util.Music_GetDetail()
        m "搞定{w=3}{nw}"
        python:
            egglabel = np_check_eggs(np_globals.Music_Name)
            if egglabel != "":
                if not renpy.seen_label(egglabel):
                    renpy.call(egglabel)
    else:
        m "呃...我们好像忘记登录了..."
        m "去设置里登录一下吧, [player]."
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
            )
        )
label np_show_userplaylist:
    python:
        store.songs.menu_open = False
        try:
            renpy.hide_screen("music_menu")
        except:
            pass
    if not np_globals.Np_Status:
        m "呃...我们好像忘记登录了..."
        m "去设置里登录一下吧, [player]."
        return
    if not len(np_globals.Play_List) > 0:
        m "呃...我还不知道你喜欢听什么呢."
        m "等我一下...{nw}"
        $ np_util.Get_User_Playlist()
        m "我知道你喜欢什么了哦, [player]."
    #m "call display_np_music_menu{nw}"
    call display_np_music_menu
    #m "设置Music_Id{nw}"
    if _return == None or _return == "":
        m "None"
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
    #m "call np_play_musicid{nw}"
    call np_play_musicid
    return
