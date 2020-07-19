from blacklist import check_blacklist
from nonebot import on_command, CommandSession
import nonebot
import requests
import sys
sys.path.insert(0, r"C:\Users\Administrator\Desktop\qqbot\qqbot\plugins")

__plugin_name__ = '知乎热榜'
__plugin_usage__ = r"""
知乎热榜

使用方法：知乎热榜 [显示条数] 或 [关键词] 或 [开始序号-结束序号]
""".strip()

_can_zhihu = True


def get_zhihu_hot(n=0, start=0, search=None):
    false = False
    true = True
    null = ""

    if n > 50:
        n = 50
    if n < 0:
        n = 0
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
    }
    proxies = {
        "http": "http://127.0.0.1:9876",
        "https": "https://127.0.0.1:9876"
    }
    r = requests.get(url, headers=headers, proxies=proxies)
    src = []
    excerpt = ""
    if search is not None:
        for i in range(0, 50):
            tmp = str(i + 1) + '. ' + \
                eval(r.text)["data"][i]["target"]["title"]
            if tmp.find(search) != -1:
                src.append(tmp)
                excerpt = eval(r.text)["data"][i]["target"]["excerpt"]
    else:
        for i in range(start, n):
            tmp = str(i + 1) + '. ' + \
                eval(r.text)["data"][i]["target"]["title"]
            src.append(tmp)
            excerpt = eval(r.text)["data"][i]["target"]["excerpt"]
    if len(src) == 1:
        src.append("问题简述：" + excerpt)
    return src


@on_command('知乎热榜', aliases=['知乎热搜'], only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    global _can_zhihu
    if(_can_zhihu == False):
        await session.send("爬嘞您喽")
        return
    arg = session.current_arg_text.strip().lower()
    if not arg:
        mylist = get_zhihu_hot(n=10)
    elif arg.find("-") != -1:
        try:
            start = int(arg[:arg.find("-")])
            n = int(arg[arg.find("-") + 1:])
        except BaseException:
            pass
        else:
            mylist = get_zhihu_hot(n=n, start=start - 1)
    else:
        try:
            n = int(arg)
        except BaseException:
            mylist = get_zhihu_hot(search=arg)
        else:
            mylist = get_zhihu_hot(n=n)
    if mylist == []:
        await session.send("似乎什么都没有找到。")
    else:
        await session.send(
            '知乎热榜：\n' + '\n'.join(i for i in mylist))
    return


@on_command('禁止知乎热榜', aliases=['禁止知乎热搜'], only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    global _can_zhihu
    _can_zhihu = False
    await session.send(
        '收到')
    return


@on_command('可以知乎热榜', aliases=['可以知乎热搜'], only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    global _can_zhihu
    _can_zhihu = True
    await session.send(
        '收到')
    return
