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
