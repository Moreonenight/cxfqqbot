from nonebot import on_command, CommandSession, permission as perm
from nonebot import on_natural_language, NLPSession, NLPResult
from nonebot.message import unescape

__plugin_name__ = '打断复读'
__plugin_usage__ = r"""
打断复读

在多人复读后自动进行打断。
""".strip()

@on_command('说打断', only_to_me = False)
async def pleasebanit(session: CommandSession):
    await session.send("打断")

'''
@on_command('say', permission=perm.SUPERUSER)
async def say(session: CommandSession):
    await session.send(
        unescape(session.state.get('message') or session.current_arg))
'''

_last_session = None
__last_session = None


@on_natural_language(only_to_me = False)
async def _(session: NLPSession):
    global _last_session
    global __last_session
    result = None
    if __last_session == None:
       __last_session = session
       return None   
    if _last_session == None:
       _last_session = session
       return None 
    if _last_session and \
            _last_session.msg == session.msg and \
            _last_session.ctx['user_id'] != session.ctx['user_id'] and \
            _last_session.ctx['user_id'] != __last_session.ctx['user_id'] and \
            _last_session.msg == __last_session.msg:
        result = NLPResult(100.0, '说打断', {'message': _last_session.msg})
        _last_session = None
    else:
        __last_session = _last_session
        _last_session = session
    return result
