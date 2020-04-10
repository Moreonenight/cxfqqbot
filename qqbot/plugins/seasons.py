from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from urllib import parse
from time import sleep

__plugin_name__ = 'seasons有无'
__plugin_usage__ = r"""
seasons有无

在收到“seasons有无”后回复“无无无”。
""".strip()

@on_command('seasons有无', only_to_me = False)
async def getpcip(session: CommandSession):
    await session.send("无无无")
    

@on_command('打断', aliases=('断', '打断复读', '禁止复读'), only_to_me = False)
async def getpcip(session: CommandSession):
    await session.send("学习时间不要复读")

@on_command('学习！', only_to_me = False)
async def getpcip(session: CommandSession):
    await session.send("那你学吧")

@on_command('别学了！', only_to_me = False)
async def getpcip(session: CommandSession):
    await session.send("我会成为摸鱼时代最后的守望者")
    sleep(1)
    await session.send("永不背弃")  
    
@on_natural_language(keywords={'seasons','四季物语'}, only_to_me = False)
async def _(session: NLPSession):
    return IntentCommand(100.0, 'seasons有无')

@on_natural_language(keywords={'学习时间', '就要学', '偏要学'}, only_to_me = False)
async def _(session: NLPSession):
    return IntentCommand(100.0, '学习！')

@on_natural_language(keywords={'别学了'}, only_to_me = False)
async def _(session: NLPSession):
    return IntentCommand(100.0, '别学了！')
