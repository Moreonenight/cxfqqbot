import sys
sys.path.insert(0, r"C:\Users\Administrator\Desktop\qqbot\qqbot\plugins")
from blacklist import check_blacklist, check_whitelist
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand, NLPResult
from urllib import parse
from aiocqhttp.message import MessageSegment
import random

__plugin_name__ = '@ta'
__plugin_usage__ = r"""
@ta

在检测到下列关键词时进行@：
黑客哥哥, 大黑客, 带黑客, 章鱼王, 章鱼人, 强者, 神明, 神祇, 木马人, 牧马人, 内卷人, 卷卷人, 恶竞人, 国奖人, 全栈人, 阴阳人, 阴阳师, 阴阳大师
""".strip()


@on_command('TheBlackGuest', only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    mybot = session.bot
    if session.ctx.get('group_id') == 【数据删除】:
        tmp_info = await mybot.get_group_member_info(group_id=【数据删除】, user_id=【数据删除】, no_cache=True)
    else:
        tmp_info = await mybot.get_group_member_info(group_id=【数据删除】, user_id=【数据删除】, no_cache=True)
    MyText = session.state.get('message').strip()
    Mylist = ["黑客哥哥", "带黑客", "大黑客"]
    for keyword in Mylist:
        if MyText.find(keyword) != -1:
            answer = MyText.find(keyword)
            text0 = MyText[0:answer]
            if text0 != "":
                text0 = text0 + " "
            text1 = MyText[(answer + len(keyword)):]
            if text1 != "":
                text1 = " " + text1
            await session.send(text0 + "@" + tmp_info["nickname"] + text1)
            return None
    return None


@on_command('Zhangyuwang', only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    mybot = session.bot
    tmp_info = await mybot.get_group_member_info(group_id=【数据删除】, user_id=【数据删除】, no_cache=True)
    MyText = session.state.get('message').strip()
    Mylist = ["章鱼人", "章鱼王"]
    for keyword in Mylist:
        if MyText.find(keyword) != -1:
            answer = MyText.find(keyword)
            text0 = MyText[0:answer]
            if text0 != "":
                text0 = text0 + " "
            text1 = MyText[(answer + len(keyword)):]
            if text1 != "":
                text1 = " " + text1
            await session.send(text0 + "@" + tmp_info["nickname"] + text1)
            return None
    return None


@on_command('TheStrongOne', only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    mybot = session.bot
    tmp_info = await mybot.get_group_member_info(group_id=【数据删除】, user_id=【数据删除】, no_cache=True)
    MyText = session.state.get('message').strip()
    Mylist = ["强者", "全栈人"]
    for keyword in Mylist:
        if MyText.find(keyword) != -1:
            answer = MyText.find(keyword)
            text0 = MyText[0:answer]
            if text0 != "":
                text0 = text0 + " "
            text1 = MyText[(answer + len(keyword)):]
            if text1 != "":
                text1 = " " + text1
            await session.send(text0 + "@" + tmp_info["nickname"] + text1)
            return None
    return None


@on_command('OhMyGod', only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    if session.ctx.get('group_id') == 【数据删除】:
        return None
    mybot = session.bot
    tmp_info = await mybot.get_group_member_info(group_id=【数据删除】, user_id=【数据删除】, no_cache=True)
    MyText = session.state.get('message').strip()
    Mylist = ["神明", "神祇"]
    for keyword in Mylist:
        if MyText.find(keyword) != -1:
            answer = MyText.find(keyword)
            text0 = MyText[0:answer]
            if text0 != "":
                text0 = text0 + " "
            text1 = MyText[(answer + len(keyword)):]
            if text1 != "":
                text1 = " " + text1
            await session.send(text0 + "@" + tmp_info["nickname"] + text1)
            return None
    return None


@on_command('HorseRider', only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    mybot = session.bot
    tmp_info = await mybot.get_group_member_info(group_id=【数据删除】, user_id=【数据删除】, no_cache=True)
    MyText = session.state.get('message').strip()
    Mylist = ["牧马人", "木马人"]
    for keyword in Mylist:
        if MyText.find(keyword) != -1:
            answer = MyText.find(keyword)
            text0 = MyText[0:answer]
            if text0 != "":
                text0 = text0 + " "
            text1 = MyText[(answer + len(keyword)):]
            if text1 != "":
                text1 = " " + text1
            await session.send(text0 + "@" + tmp_info["nickname"] + text1)
            return None
    return None


@on_command('InnerRoll', only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    mybot = session.bot
    tmp_info = await mybot.get_group_member_info(group_id=【数据删除】, user_id=【数据删除】, no_cache=True)
    MyText = session.state.get('message').strip()
    Mylist = ["内卷人", "卷卷人", "恶竞人"]
    for keyword in Mylist:
        if MyText.find(keyword) != -1:
            answer = MyText.find(keyword)
            text0 = MyText[0:answer]
            if text0 != "":
                text0 = text0 + " "
            text1 = MyText[(answer + len(keyword)):]
            if text1 != "":
                text1 = " " + text1
            await session.send(text0 + "@" + tmp_info["nickname"] + text1)
            return None
    return None

@on_command('NationalAward', only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    mybot = session.bot
    NationalAwardTuple = (【数据删除】, 【数据删除】, 【数据删除】, 【数据删除】, 【数据删除】)
    if session.ctx.get('user_id') in NationalAwardTuple:
        tmp_info = await mybot.get_group_member_info(group_id=【数据删除】, user_id=session.ctx.get('user_id'), no_cache=True)
    else:
        random.seed()
        chosen_id = NationalAwardTuple[int(random.uniform(0, len(NationalAwardTuple) - 0.001))]
        tmp_info = await mybot.get_group_member_info(group_id=【数据删除】, user_id=chosen_id, no_cache=True)
    MyText = session.state.get('message').strip()
    Mylist = ["国奖人"]
    for keyword in Mylist:
        if MyText.find(keyword) != -1:
            answer = MyText.find(keyword)
            text0 = MyText[0:answer]
            if text0 != "":
                text0 = text0 + " "
            text1 = MyText[(answer + len(keyword)):]
            if text1 != "":
                text1 = " " + text1
            await session.send(text0 + "@" + tmp_info["nickname"] + text1)
            return None
    return None

@on_command('ToYourself', only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    mybot = session.bot
    tmp_info = await mybot.get_group_member_info(group_id=【数据删除】, user_id=session.ctx.get('user_id'), no_cache=True)
    MyText = session.state.get('message').strip()
    Mylist = ['阴阳人', "学习人", "阴阳师", "阴阳大师"]
    for keyword in Mylist:
        if MyText.find(keyword) != -1:
            answer = MyText.find(keyword)
            text0 = MyText[0:answer]
            if text0 != "":
                text0 = text0 + " "
            text1 = MyText[(answer + len(keyword)):]
            if text1 != "":
                text1 = " " + text1
            await session.send(text0 + "@" + tmp_info["nickname"] + text1)
            return None
    return None


@on_command('机器人', only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    await session.send("也会梦见电子🐻")
    return None


@on_natural_language(keywords={'黑客哥哥', '大黑客', '带黑客'}, only_to_me=False)
async def _(session: NLPSession):
    if check_blacklist(session.ctx.get('user_id')
                       ) or session.msg.strip()[0] == ".":
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    result = NLPResult(85.0, 'TheBlackGuest', {'message': session.msg})
    return result


@on_natural_language(keywords={'章鱼王', '章鱼人'}, only_to_me=False)
async def _(session: NLPSession):
    if check_blacklist(session.ctx.get('user_id')
                       ) or session.msg.strip()[0] == ".":
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    if session.ctx.get('group_id') == 【数据删除】:
        return None
    if not check_whitelist(session.event.group_id):
        return None
    result = NLPResult(85.0, 'Zhangyuwang', {'message': session.msg})
    return result


@on_natural_language(keywords={'强者', "全栈人"}, only_to_me=False)
async def _(session: NLPSession):
    if check_blacklist(session.ctx.get('user_id')
                       ) or session.msg.strip()[0] == ".":
        return None
    if session.ctx.get('group_id') == 【数据删除】:
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    result = NLPResult(75.0, 'TheStrongOne', {'message': session.msg})
    return result


@on_natural_language(keywords={'神明', '神祇'}, only_to_me=False)
async def _(session: NLPSession):
    if check_blacklist(session.ctx.get('user_id')
                       ) or session.msg.strip()[0] == ".":
        return None
    if session.ctx.get('group_id') == 【数据删除】:
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    result = NLPResult(70.0, 'OhMyGod', {'message': session.msg})
    return result


@on_natural_language(keywords={'牧马人', '木马人'}, only_to_me=False)
async def _(session: NLPSession):
    if check_blacklist(session.ctx.get('user_id')
                       ) or session.msg.strip()[0] == ".":
        return None
    if session.ctx.get('group_id') == 【数据删除】:
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    result = NLPResult(70.0, 'HorseRider', {'message': session.msg})
    return result


@on_natural_language(keywords={'内卷人', '卷卷人', "恶竞人"}, only_to_me=False)
async def _(session: NLPSession):
    if check_blacklist(session.ctx.get('user_id')
                       ) or session.msg.strip()[0] == ".":
        return None
    if session.ctx.get('group_id') == 【数据删除】:
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    result = NLPResult(70.0, 'InnerRoll', {'message': session.msg})
    return result
    
@on_natural_language(keywords={"国奖人"}, only_to_me=False)
async def _(session: NLPSession):
    if check_blacklist(session.ctx.get('user_id')
                       ) or session.msg.strip()[0] == ".":
        return None
    if session.ctx.get('group_id') == 【数据删除】:
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    result = NLPResult(70.0, 'NationalAward', {'message': session.msg})
    return result

@on_natural_language(keywords={'阴阳人', "学习人", "阴阳师", "阴阳大师"}, only_to_me=False)
async def _(session: NLPSession):
    if check_blacklist(session.ctx.get('user_id')
                       ) or session.msg.strip()[0] == ".":
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    result = NLPResult(70.0, 'ToYourself', {'message': session.msg})
    return result
