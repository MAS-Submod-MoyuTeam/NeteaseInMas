define np_paused = False
init 100:
    screen mas_extramenu_area():
        zorder 52

        key "e" action Jump("mas_extra_menu_close")
        key "E" action Jump("mas_extra_menu_close")
        
        frame:
            area (0, 0, 1280, 720)
            background Solid("#0000007F")
            textbutton _("Close"):
                area (60, 596, 120, 35)
                style "hkb_button"
                action Jump("mas_extra_menu_close")

        frame:
            area (295, 450, 180, 255)
            style "mas_extra_menu_frame"
            vbox:
                spacing 2
                label "网易云":
                    text_style "mas_extra_menu_label_text"
                    xalign 0.5
                textbutton _("我喜欢的音乐"):
                    xsize 170
                    ysize 35
                    style "hkb_button"
                    action Function(np_extra_musiclist)


                textbutton _("循环播放缓存"):
                    xsize 170
                    ysize 35
                    style "hkb_button"
                    action Function(np_loopplay)

                textbutton _("随机播放缓存"):
                    xsize 170
                    ysize 35
                    style "hkb_button"
                    action Function(np_randomplay)
                    
                textbutton _("搜索"):
                    xsize 170
                    ysize 35
                    style "hkb_button"
                    action Function(np_search_topic)
                hbox:
                    textbutton _("播放"):
                        xsize 77
                        ysize 35
                        style "hkb_button"
                        action Function(np_resume)
                    label "":
                        xsize 14
                        ysize 35
                    textbutton _("暂停"):
                        xsize 77
                        ysize 35
                        style "hkb_button"
                        action Function(np_pause)

                    
            # zoom control
        frame:
            area (195, 450, 80, 255)
            style "mas_extra_menu_frame"
            vbox:
                spacing 2
                label "Zoom":
                    text_style "mas_extra_menu_label_text"
                    xalign 0.5
                # resets the zoom value back to default
                textbutton _("Reset"):
                    style "mas_adjustable_button"
                    selected False
                    xsize 72
                    ysize 35
                    xalign 0.3
                    action SetField(store.mas_sprites, "zoom_level", store.mas_sprites.default_zoom_level)
                # actual slider for adjusting zoom
                bar value FieldValue(store.mas_sprites, "zoom_level", store.mas_sprites.max_zoom):
                    style "mas_adjust_vbar"
                    xalign 0.5
                $ store.mas_sprites.adjust_zoom()

    python:
        def hide_extra_screen():
            store.mas_extramenu.menu_visible = False
            try:
                renpy.hide_screen("mas_extramenu_area")
            except:
                pass

            # prev_zoom 只在 extra menu 打开时被定义；
            # 如果直接调用本函数（比如从事件菜单触发），会 NameError，所以做兜底
            try:
                if store.mas_sprites.zoom_level != prev_zoom:
                    renpy.call("mas_extra_menu_zoom_callback")
            except NameError:
                pass
            except Exception as e:
                store.mas_submod_utils.submod_log.error(
                    "hide_extra_screen zoom_callback 异常：{}".format(e)
                )

            # 同样把 shield 相关也包一下，防止非 idle 状态下调用出错
            try:
                if store.mas_globals.in_idle_mode:
                    mas_coreToIdleShield()
                else:
                    mas_DropShield_core()
            except Exception as e:
                store.mas_submod_utils.submod_log.error(
                    "hide_extra_screen shield 异常：{}".format(e)
                )
        def np_extra_musiclist():
            hide_extra_screen()
            renpy.call('np_show_userplaylist')
            renpy.jump('mas_extra_menu_close_p2')

        def np_search_topic():
            hide_extra_screen()
            renpy.call("np_search")
            renpy.jump('mas_extra_menu_close_p2')

        def np_loopplay():
            hide_extra_screen()
            renpy.call('np_loop')
            renpy.jump('mas_extra_menu_close_p2')

        def np_pause():
            renpy.music.set_pause(True)
            np_paused=True
        def np_resume():
            renpy.music.set_pause(False)
            np_paused=False

label mas_extra_menu_close_p2:
    show monika idle
    jump ch30_loop
    return