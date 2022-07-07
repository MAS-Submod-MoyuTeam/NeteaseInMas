# 兼容Extra+
init 2:
    label tools_extra:
        show monika staticpose at t21
        python:
           tools_menu = []
           tools_menu.append((_("View [m_name]'s Affection"), "affection"))
           tools_menu.append((_("[m_name], can you flip a coin?"), "coin"))
           tools_menu.append((_("[m_name], I want to make a backup"), "backup"))
           tools_menu.append((_("Create a gift for [m_name]"), "gift"))
           tools_menu.append((_("Github Repository"), "github"))
           tools_menu.append((_("Help"), "help"))
           tools_menu.append((_("Nevermind"),"nevermind"))

           playerchoice = renpy.display_menu(tools_menu, screen="talk_choice")

        if playerchoice == "affection":
            jump aff_log
        elif playerchoice == "coin":
            jump coinflipbeta
        elif playerchoice == "backup":
            jump mas_backup
        elif playerchoice == "gift":
            jump make_gift
        elif playerchoice == "github":
            jump github_submod
        elif playerchoice == "help":
            jump helpextra
        elif playerchoice == "nevermind":
            jump return_extra
    return
screen mas_extramenu_area():
    zorder 52

    key "e" action Jump("mas_extra_menu_close")
    key "E" action Jump("mas_extra_menu_close")

    frame:
        area (0, 0, 1280, 720)
        background Solid("#0000007F")

        # close button
        textbutton _("Close"):
            area (60, 596, 120, 35)
            style "hkb_button"
            action Jump("mas_extra_menu_close")

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
