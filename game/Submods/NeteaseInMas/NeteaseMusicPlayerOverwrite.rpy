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
                    xsize 175
                    ysize 35
                    style "hkb_button"
                    action Function(np_extra_musiclist)
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
        def np_extra_musiclist():
            renpy.call('np_show_userplaylist')
            renpy.call('mas_extra_menu_close_p1')
            renpy.jump('mas_extra_menu_close_p2')

label mas_extra_menu_close_p1:
    $ store.mas_extramenu.menu_visible = False
    hide screen mas_extramenu_area
    if store.mas_sprites.zoom_level != prev_zoom:
        call mas_extra_menu_zoom_callback

    # re-enable overlays
    if store.mas_globals.in_idle_mode:
        $ mas_coreToIdleShield()
    else:
        $ mas_DropShield_core()
    return

label mas_extra_menu_close_p2:
    show monika idle
    jump ch30_loop
    return