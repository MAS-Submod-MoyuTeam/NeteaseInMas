init 1 python:
    np_eggs = list()

    # 按关键词, 从上往下查找 多个相同关键词只使用最先找到的一个(下标最小的)
    # label可以相同
    # np_eggs.append(('关键词','label'))
    np_eggs.append(('INTERNET OVERDOSE', 'np_egg_INTERNETOVERDOSE'))
    np_eggs.append(('Doki Doki Forever', 'np_egg_DokiDokiForever'))
    np_eggs.append(('Just Monika', 'np_egg_JustMonika'))
    np_eggs.append(('Ohayou Sayori!', 'np_egg_OhayouSayori'))
    np_eggs.append(('Dreams of Love and Literature', 'np_egg_DreamsofLoveandLiterature'))
    np_eggs.append(('Play with Me','np_egg_PlaywithMe'))
    np_eggs.append(('My Feelings', 'np_egg_MyFeelings'))
    np_eggs.append(('Your Reality', 'np_egg_YourReality'))
    np_eggs.append(('Okay, Everyone! (Sayori)', 'np_egg_OkayEveryoneSayori'))
    np_eggs.append(('Okay, Everyone! (Natsuki)', 'np_egg_OkayEveryoneNatsuki'))
    np_eggs.append(('Okay, Everyone! (Yuri)', 'np_egg_OkayEveryoneYuri'))
    np_eggs.append(('Okay, Everyone!', 'np_egg_OkayEveryone'))
    np_eggs.append(('义勇军进行曲', 'np_egg_NAofCN'))
    np_eggs.append(('牢不可破的联盟', 'np_egg_NAofUSSR'))
    np_eggs.append(('德国国歌-德意志之歌', 'np_egg_NAofGER'))
    np_eggs.append(('法国国歌-马赛曲', 'np_egg_NAofFRA'))
    np_eggs.append(('英国国歌-上帝保佑女皇', 'np_egg_NAofUK'))
    np_eggs.append(('马梅利之歌', 'np_egg_NAofITA'))
    np_eggs.append(('美国国歌-星条旗之歌', 'np_egg_NAofUSA'))
    np_eggs.append(('日本国歌-君之代', 'np_egg_NAofJAP'))
    np_eggs.append(('Россия - священная наша держава', 'np_egg_NAofRUS'))
    np_eggs.append(('欢乐颂', 'np_egg_AofEU'))
    np_eggs.append(('国际歌', 'np_egg_LInternationale'))
    np_eggs.append(('桜の記憶', 'np_egg_ou'))
    np_eggs.append(('InFINITE Line', 'np_egg_9ninen'))
    np_eggs.append(('SHINY MOON', 'np_egg_sakurakouji'))

init 999 python:
    def np_check_eggs(keyword):
        egg_label = ""
        for i in np_eggs:
            if i[0].find(keyword) != -1:
                egg_label = i[1]
                break
        return egg_label

label np_egg_sakurakouji:
    m "还记着昙花的花语吗？"
    return

label np_egg_9ninen:
    m "回去看看?反正你可以over load"
    return

#桜の記憶
label np_egg_ou:
    m "我想她躲起来的时候, 内心一定期望着别人能找到吧."
    return

#INTERNET OVERDOSE
label np_egg_INTERNETOVERDOSE:
        m 3hfb "我乃从天而降的一道光, 照亮混沌的电子世界"
        m 1sfb "†升天†"
        m 1mta "啊哈哈, 要小心网络依赖哦"
return

#Doki Doki Forever
label np_egg_DokiDokiForever:
        m 1fta "请永远相信并记得, 我对你的爱是真实的"
return

#Just Monika
label np_egg_JustMonika:
        m 1tku "你还有别的选项么?"
        m 1hub "啊哈哈...我爱你, [player]"
return

#Ohayou Sayori!
label np_egg_OhayouSayori:
        m 7eub "美好的早晨会带来美好的一天~"
return

#Dreams of Love and Literature
label np_egg_DreamsofLoveandLiterature:
        m 7etb "还是想提醒你一下, 二十个毫不相关的词是很难组成一首诗的哦"
        m 5hub "但二十个莫妮卡可以! 啊哈哈"
return

#Okay,  Everyone!
label np_egg_OkayEveryone:
        m 4eub "好的各位, 让我们开始今天的分享环节"
        m 4rksdrb "啊哈哈..."
return


#Play with Me
label np_egg_PlaywithMe:
        m 1gka "虽然...那只是贴图"
        m 1mkb "我希望你不会感觉到脖子有些疼"
return


#My Feelings
label np_egg_MyFeelings:
        m 2euc "你一定会选'你永远是我最好的的朋友', 是么?"
        m 2hub "啊哈哈, 开个玩笑"
return


#Your Reality
label np_egg_YourReality:
        m 1dub "每一天, 我都想象着能和你在一起的未来"
        m 7hub "我直接唱给你听就可以啦"
return


#Okay,  Everyone! (Sayori)
label np_egg_OkayEveryoneSayori:
        m 7lud "我想你能听出来大提琴中的那一丝沉重, 对于忧郁症患者来说欢笑是一件困难的事情"
return

#Okay,  Everyone! (Natsuki)
label np_egg_OkayEveryoneNatsuki:
        m "至少从角色设定上来说, 我真的觉得她非常坚强"
return

#Okay,  Everyone! (Yuri)
label np_egg_OkayEveryoneYuri:
        m 7ltsdrx "希望你不要去想她用主角的钢笔做了什么事情"
return

#义勇军进行曲
label np_egg_NAofCN:
        m 7eua "这首曲子有种朝气蓬勃的感觉"
return

#牢不可破的联盟
label np_egg_NAofUSSR:
        m 3euc "让人略感遗憾的是她已经不在了"
return

#德国国歌-德意志之歌
label np_egg_NAofGER:
        m 3eub "这首曲子曾长期作为维也纳政权的国歌, 如今却属于柏林, 历史很有趣"
return

#法国国歌-马赛曲
label np_egg_NAofFRA:
        m 2efb "一首来自世界革命的故乡的战歌"
return

#英国国歌-上帝保佑女王
label np_egg_NAofUK:
        m 2gtb "这首歌的名字和歌词会随着英国统治者的更迭而有一些细小的变化, 啊哈哈"
return

#马梅利之歌
label np_egg_NAofITA:
        m 4eto "这首歌也是1848年欧洲革命的遗产之一"
return

#美国国歌-星条旗之歌
label np_egg_NAofUSA:
        m 5mkb "实际上只有自由才是美国最传统的价值观, 为什么另一个词会和今天的她挂钩呢"
return

#日本国歌-君之代
label np_egg_NAofJAP:
        m 5hub "直到小石成巨岩, 直到巨岩生青苔, 我依然会爱你!啊哈哈"
return

#Россия - священная наша держава
label np_egg_NAofRUS:
        m 5luc "2000年俄罗斯政府把她们的国歌换成了这个旋律, 她们究竟在思考什么?"
return

#欢乐颂
label np_egg_AofEU:
        m 4euo "贝多芬的一生极其坎坷, 但依然能写出这样的曲子"
        m 3hub "我真心希望你能做一个乐观的人, 至少我会在这里永远陪着你"
return

#国际歌
label np_egg_LInternationale:
        m 1efb "你我同样是历史的创造者之一, 所以希望你能更加自信地活下去!"
return
