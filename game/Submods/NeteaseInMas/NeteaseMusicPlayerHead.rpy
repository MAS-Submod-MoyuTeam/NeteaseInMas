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
        description="在MAS里播放游戏音乐.",
        version='0.0.1',
        settings_pane="np_setting_pane"
    )


screen np_setting_pane():
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

        text "- 当前登录:<check>"
        text "- 正在播放:<music>"
        text ""

        #> !已登录 ? 登陆账号 : 注销账号
        if np_util.Music_Login_Status() == False:
            textbutton "> 登录账号":
                ypos 1
                selected False
                action Show("np_login")
        else:
            textbutton "> 注销账号":
                ypos 1
                selected False
                action Show("np_logout")
        
        textbutton "> 安全性问题说明"

        textbutton "> 清理歌曲缓存"

        if np_globals.debug:
            textbutton "> debug" 

screen np_login():
    pass

