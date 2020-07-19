import sys
sys.path.insert(
    0, r"C:\Users\Administrator\Desktop\qqbot\qqbot\plugins\my_emoji")
sys.path.insert(0, r"C:\Users\Administrator\Desktop\qqbot\qqbot\plugins")
from blacklist import check_blacklist
import nmsl_local
import nonebot
from nonebot import on_command, CommandSession
from pypinyin import Style, pinyin

__plugin_name__ = '抽象话'
__plugin_usage__ = r"""
抽象话

使用方法：抽象话 [正常的话]
""".strip()


def chouxiang_process(old_str):
    number_dict = {
        "one": "",
        "1": "1⃣",
        "two": "2⃣",
        "2": "2⃣",
        "three": "3⃣",
        "3": "3⃣",
        "four": "4⃣",
        "4": "4⃣",
        "five": "5⃣",
        "5": "5⃣",
        "six": "6⃣",
        "6": "6⃣",
        "seven": "7⃣",
        "7": "7⃣",
        "eight": "8⃣",
        "8": "8⃣",
        "nine": "9⃣",
        "9": "9⃣",
        "ten": "0⃣",
        "0": "0⃣"}
    for key, value in number_dict.items():
        old_str = old_str.replace(key, value)
    new_str = nmsl_local.text_to_emoji(old_str)
    return new_str


@on_command('抽象话', aliases=['抽象', '带话'], only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    arg = session.current_arg_text.strip().lower()
    if not arg:
        await session.send("使用方法：抽象话 [正常的话]")
        return
    answer = chouxiang_process(arg)
    await session.send(answer)
    return
