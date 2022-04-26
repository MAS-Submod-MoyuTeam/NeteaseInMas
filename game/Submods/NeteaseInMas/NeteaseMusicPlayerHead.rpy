init -990 python:
    store.mas_submod_utils.Submod(
        author="P",
        name="Netease Music",
        description="在MAS里播放游戏音乐.",
        version='0.0.1',
        settings_pane="nm_setting_pane"
    )
"""
todo:
    界面:
        - 登录
        - 刷新登录缓存
        - 正在播放
        - 清除下载歌曲
"""
screen nm_setting_pane():