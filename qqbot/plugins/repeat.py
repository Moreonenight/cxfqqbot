import sys
sys.path.insert(0, r"C:\Users\Administrator\Desktop\qqbot\qqbot\plugins")
from blacklist import check_blacklist
from nonebot import on_command, CommandSession, permission as perm
from nonebot import on_natural_language, NLPSession, NLPResult
from nonebot.message import unescape

__plugin_name__ = '打断复读'
__plugin_usage__ = r"""
打断复读

在多人复读后自动进行打断。
""".strip()


@on_command('说打断', only_to_me=False)
async def pleasebanit(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    await session.send("打断")

'''
@on_command('say', permission=perm.SUPERUSER)
async def say(session: CommandSession):
    await session.send(
        unescape(session.state.get('message') or session.current_arg))
'''


@on_command('复读', only_to_me=False)
async def echo(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    await session.send(session.state.get('message') or session.current_arg)

group_list = []
group_dict = {}

_can_break = False
_can_repeat = True


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    if check_blacklist(session.ctx.get('user_id')
                       ) or session.msg.strip()[0] == ".":
        return None
    group_id = session.ctx.get('group_id')
    global group_list
    global group_dict
    if group_id not in group_list:
        group_list.append(group_id)
        group_dict[group_id] = [None, None]
    global _can_break
    global _can_repeat
    result = None
    if group_dict[group_id][0] is None:
        group_dict[group_id][0] = session
        return None
    if group_dict[group_id][1] is None:
        group_dict[group_id][1] = session
        return None
    if group_dict[group_id][1] and \
            group_dict[group_id][1].msg == session.msg and \
            group_dict[group_id][1].ctx['user_id'] != session.ctx['user_id'] and \
            group_dict[group_id][1].ctx['user_id'] != group_dict[group_id][0].ctx['user_id'] and \
            group_dict[group_id][1].msg == group_dict[group_id][0].msg:
        if _can_break:
            result = NLPResult(
                100.0, '说打断', {
                    'message': group_dict[group_id][1].msg})
        if _can_repeat:
            result = NLPResult(
                100.0, '复读', {
                    'message': group_dict[group_id][1].msg})
        group_dict[group_id][1] = None
        group_dict[group_id][0] = None
    else:
        group_dict[group_id][0] = group_dict[group_id][1]
        group_dict[group_id][1] = session
    return result


@on_command('禁止打断', only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    global _can_break
    _can_break = False
    await session.send(
        '收到')
    return


@on_command('禁止复读', only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    global _can_repeat
    _can_repeat = False
    await session.send(
        '学习时间不要复读')
    return


@on_command('可以复读', only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    global _can_break
    global _can_repeat
    if not _can_break:
        _can_repeat = True
        await session.send(
            '可以复读')
        return
    else:
        await session.send(
            '无法在打断的同时复读')
        return


@on_command('可以打断', only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    global _can_break
    global _can_repeat
    if not _can_repeat:
        _can_break = True
        await session.send(
            '收到')
        return
    else:
        await session.send(
            '无法在复读的同时打断')
        return
