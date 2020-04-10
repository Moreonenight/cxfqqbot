import nonebot
from nonebot import on_command, CommandSession

@on_command('help', aliases=['使用帮助', '帮助', '使用方法', 'man', 'manual'])
async def _(session: CommandSession):
    plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))
    arg = session.current_arg_text.strip().lower()
    if not arg:
        await session.send(
            '我现在支持的功能有：\n' + '\n'.join(p.name for p in plugins) + '\n\n' + '输入help [功能名] 可以查看具体使用方法。\n' + \
            '另外，此bot还缝合了跑团掷骰功能。请输入.dicehelp以查看该功能的使用说明。')
        return

    for p in plugins:
        if p.name.lower() == arg:
            await session.send(p.usage)
