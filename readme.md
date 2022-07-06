# NeteaseinMas
内置于Monika After Story的网易云音乐播放器。

***注意:只支持Windows 可能不兼容Youtube Music和Night Music***


## 安装

1.确保使用的是最新汉化版本MAS.    
2.从[Release](https://github.com/PencilMario/NeteaseInMas/releases)处下载最新的版本.    
3.关闭游戏, 将zip中的文件合并到您的`DDLC`/`MAS_CN001***/Monika After Story`文件夹内, 或者是`DDLC.exe`/`MAS.exe`所在的位置    
4.可选择安装[Paste](https://github.com/Legendkiller21/MAS-Submods-Paste)（允许复制粘贴）和/或[Submod Updater Plugin](https://github.com/Booplicate/MAS-Submods-SubmodUpdaterPlugin)（允许通过游戏内更新程序更新 submods.     

如果您正确安装了所有内容, 那么文件夹结构应该是这样的:
```
DDLC/
    game/
        python-packages/
            requests/
                **requests库文件**
            Submods/NeteaseInMas/
                Catch/
                    **缓存文件夹**
                ffmpeg/
                    **ffmpeg程序, 转码需要用到**
                NeteaseMusicPlayerDebug.rpy 
                    **检查bug用脚本**
                NeteaseMusicPlayerEggs.rpy
                    **歌名彩蛋**
                NeteaseMusicPlayerHead.rpy
                    **子模组定义界面的脚本文件**
                NeteaseMusicPlayerMain.rpy
                    **子模组定义方法, 全局变量等的脚本文件**
                NeteaseMusicPlayerOverwrite.rpy
                    **子模组重写原MAS方法的脚本, 啥都没写可以删**
                NeteaseMusicPlayerThreading.rpy
                    **子模组Threading文件, 似乎也可以删**
                NeteaseMusicPlayerTopic.rpy
                    **子模组定义整个操作流程的文件**
    lib/windows-i686/Lib/
        **requests需要的其它库文件**
```

## 使用方法  

0.参照`使用方法.docx`, 创建你自己的网易云音乐API（这非必须，但很重要！）
1.打开MAS, 进入设置-子模组.  
2.找到NeteaseInMas, 登录您的网易云手机号和密码(不支持短信验证码)  
3.如果确保账密正确, 仍然无法登录, 请等待两分钟点击强制刷新登录(不是登录)  
4.所有话题都在`嘿, 莫妮卡-Netease Music`内.  

> NeteaseInMas 将于 MAS 更新至 1.2.9 后不再提供默认API

## 提示

* 本子模组无法播放版权音乐(需要黑胶VIP)和无版权音乐(网易云无版权), 会提示下载失败
* 安装如果冲突, 替换与否都可、
* 提示风控时，请参考`使用方法.docs`更新你的API

## 特别感谢
[NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi) 本子模组使用的API, 没有这个就没有本子模组.  
[YoutubeMusic](https://github.com/Booplicate/MAS-Submods-YouTubeMusic) 本模组部分代码参考了YM的设计.  
[MonikaAfterStory](https://github.com/Monika-After-Story/MonikaModDev) 本模组部分代码参考了MAS的设计.  

星光 - 彩蛋设计  

洛尔 - 演出编辑  
