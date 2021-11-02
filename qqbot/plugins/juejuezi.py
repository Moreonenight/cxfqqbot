# https://github.com/kingcos/JueJueZiGenerator MIT License

import sys
sys.path.insert(0, r"C:\Users\Administrator\Desktop\qqbot\qqbot\plugins")
from blacklist import check_blacklist
import random
import nonebot
from nonebot import on_command, CommandSession

__plugin_name__ = '绝绝子'
__plugin_usage__ = r"""
绝绝子

使用方法：绝绝子 [动词] [名词]
示例：绝绝子 喝 咖啡；绝绝子 吃 薯条
""".strip()

materialDict = {
    "emotions": {
        "emoji": [
            "😊",
            "🌟",
            "🧩",
            "✨",
            "☀️",
            "🌹",
            "🌸",
            "🌼",
            "🥝",
            "🥤",
            "🍑",
            "🍹",
            "🥑",
            "🙋‍♀️",
            "🎀",
            "❤️",
            "🧡",
            "💛",
            "💚",
            "💙",
            "💜",
            "🖤",
            "🤍",
            "🤎",
            "💕",
            "💞",
            "💓",
            "💗",
            "💖",
            "💝"
        ],
        "xiaohongshu": [
            "[微笑R]",
            "[害羞R]",
            "[失望R]",
            "[汗颜R]",
            "[哇R]",
            "[喝奶茶R]",
            "[自拍R]",
            "[偷笑R]",
            "[飞吻R]",
            "[石化R]",
            "[笑哭R]",
            "[赞R]",
            "[暗中观察R]",
            "[买爆R]",
            "[大笑R]",
            "[色色R]",
            "[生气R]",
            "[哭惹R]",
            "[萌萌哒R]",
            "[斜眼R]",
            "[可怜R]",
            "[鄙视R]",
            "[皱眉R]",
            "[抓狂R]",
            "[派对R]",
            "[吧唧R]",
            "[惊恐R]",
            "[抠鼻R]",
            "[再见R]",
            "[叹气R]",
            "[睡觉R]",
            "[得意R]",
            "[吃瓜R]",
            "[扶墙R]",
            "[黑薯问号R]",
            "[黄金薯R]",
            "[吐舌头H]",
            "[扯脸H]",
            "[doge]"
        ],
        "weibo": []
    },
    "symbols": [
        "！",
        "？",
        "～",
        "❓",
        "❔",
        "‼️",
        "⁉️",
        "❗️",
        "❕"
    ],
    "auxiliaryWords": [
        "鸭",
        "呜",
        "啦",
        "呐",
        "呀",
        "咩",
        "呢",
        "哈",
        "嘿",
        "哒",
        "害",
        "啊"
    ],
    "dividers": [
        " ",
        "，"
    ],
    "beginning": [
        "今日份who营业啦",
        "who下班啦",
        "投递日常",
        "今天的who也营业啦",
        "今日份甜甜碎片已加载完毕",
        "忙里偷闲的生活碎片",
        "和someone逛吃的一天",
        "分享開心",
        "分享今日份開心",
        "营业一下"
    ],
    "who": [
        "打工人",
        "仙女",
        "普信男",
        "Java男",
        "普信女",
        "小可爱",
        "本公主"
    ],
    "someone": [
        "小狗勾",
        "小姐姐",
        "集美",
        "集美们",
        "闺蜜",
        "闺蜜👭",
        "姐妹",
        "姐妹们",
        "姐妹👭",
        "好姐妹",
        "好姐妹👭",
        "小姐妹",
        "小姐妹👭"
    ],
    "todosth": [
        "今天去dosth",
        "今天去dosth了",
        "今天去dosth啦",
        "今天去dosth鸭",
        "今天去dosth噜",
        "今天又又又dosth啦",
        "今天又又又dosth鸭",
        "又去dosth啦",
        "又是dosth的一天啦",
        "今天又是dosth的一天啦",
        "宝～我今天dosth了",
        "宝！我今天dosth了",
        "还是去dosth了",
        "无聊去dosth",
        "今天去体验了dosth"
    ],
    "another": [
        "买 小蛋糕",
        "买 小布丁",
        "喝 奶茶",
        "穿 JK",
        "吃 迷hotel",
        "喝 咖啡",
        "买 蜜雪冰城",
        "买 喜茶",
        "喝 谬可"
    ],
    "ending": [
        "也是在逃公主的一天",
        "好想谈一场双向奔赴的恋爱",
        "星星月亮和我都要睡啦",
        "散会",
        "我是一面镜子 所以 晚安 我碎啦",
        "岁月漫长 那就一起拯救地球与乐趣吧"
    ],
    "collections": [
        "路上还看见一个普信男",
        "路边捡到了一分钱",
        "不小心踩了狗屎",
        "路上还看见一个Java男"
    ],
    "attribute": [
        "绝绝子",
        "无语子",
        "真下头",
        "yyds",
        "奈斯",
        "有被惊艳到",
        "🉑️",
        "太可了",
        "太🉑️了",
        "真的绝",
        "太牛了",
        "太🐮了",
        "好dosth到跺脚",
        "好dosth到爆",
        "好dosth到跺jiojio",
        "太爱了"
    ],
    "fashion": [
        "救命🆘",
        "噎死莫拉",
        "不管啦",
        "就是玩儿",
        "无语子",
        "我真的哭死",
        "冲鸭",
        "笑死",
        "那我走",
        "我都惊了",
        "大无语事件",
        "就很烦",
        "心态炸裂",
        "搞快点",
        "不是吧",
        "不是8⃣️",
        "全都给我冲",
        "啥也不是"
    ],
    "default": [
        "豁 奶茶",
        "撸 代码",
        "刷 微博",
        "买 基金",
        "摸 鱼",
        "玩 绝绝子生成器"
    ]
}


def randomWord(words, nullable=False, divider=''):
    maxRange = len(words)
    if nullable:
        maxRange += maxRange / 3
    index = int(random.random() * maxRange)
    if index >= len(words):
        return ''
    else:
        return words[index] + divider


def randomWords(words, count):
    if len(words) < count:
        return words
    return random.sample(words, count)


def randomRepeat(word, times=-1):
    if times > 0:
        result = ""
        result += times * word
        return result
    index = int(random.random() * 3)
    if index == 2:
        return randomRepeat(word, 3)
    if index == 0:
        return randomRepeat(word, 1)
    return ''


def generateBeginning(divider):
    beginning = randomWord(materialDict["beginning"])
    if 'who' in beginning:
        beginning = beginning.replace('who', randomWord(materialDict["who"]))
    if 'someone' in beginning:
        beginning = beginning.replace(
            'someone', randomWord(materialDict["someone"]))
    emotion = randomWord(materialDict["emotions"]["emoji"], True)
    return beginning + emotion + divider


def generateDoSth(something, divider):
    todosth = randomWord(materialDict["todosth"])
    if 'dosth' in todosth:
        if ' ' in something:
            something = something.replace(' ', '')
        todosth = todosth.replace('dosth', something)
    emotions = randomRepeat(randomWord(materialDict["emotions"]["emoji"]))
    return todosth + emotions + divider


def praiseSth(something, praisedWords, hasAlso=False):
    praiseWord = randomWord(praisedWords)
    verb = something.split(' ')[0]
    noun = something.split(' ')[1]
    result = ''
    intro = randomWord(['这家的', '这家店的', '这个', '这件', '这杯'])
    also = '也' if hasAlso else ''
    if 'dosth' in praiseWord:
        praiseWord = praiseWord.replace('dosth', verb)
        result = intro + noun + also + praiseWord
    else:
        result = intro + noun + also + praiseWord
    return result


def randomButNotContain(words, already):
    random = randomWord(words)
    mySet = set(list(already.replace(' ', '')))
    randomSet = set(list(random.replace(' ', '')))
    intersect = randomSet & mySet
    if len(intersect) == 0:
        return random
    else:
        return randomButNotContain(words, already)


def generate(something):
    random.seed()
    divider = randomWord(materialDict["dividers"])
    fashionWords = randomWords(
        materialDict["fashion"], len(materialDict["fashion"]))
    first = generateBeginning(divider)
    second = fashionWords[0] + divider
    third = generateDoSth(something, divider)
    forth = fashionWords[1] + divider
    fifth = randomRepeat(randomWord(
        materialDict["auxiliaryWords"]), 3) + divider
    sixth = praiseSth(something, materialDict["attribute"]) + \
        randomRepeat(randomWord(materialDict["symbols"]), 3)
    seventh = praiseSth(randomButNotContain(
        materialDict["another"], something), materialDict["attribute"], True) + randomRepeat(randomWord(materialDict["symbols"]), 3)
    eighth = fashionWords[2] + divider
    ninth = randomWord(materialDict["collections"],
                       True, divider) + fashionWords[3] + divider
    tenth = randomRepeat(randomWord(
        materialDict["auxiliaryWords"]), 3) + divider
    last = randomWord(materialDict["ending"]) + \
        randomWord(materialDict["emotions"]["emoji"])
    return first + second + third + forth + fifth + sixth + seventh + eighth + ninth + tenth + last



@on_command('绝绝子', only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    arg = session.current_arg_text.strip().lower()
    if len(arg.split()) != 2:
        await session.send("使用方法：绝绝子 [动词] [名词]")
        return
    await session.send(generate(arg))
    return

