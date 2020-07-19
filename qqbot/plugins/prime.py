import sys
sys.path.insert(0, r"C:\Users\Administrator\Desktop\qqbot\qqbot\plugins")
from blacklist import check_blacklist
import nonebot
from nonebot import on_command, CommandSession

__plugin_name__ = '素性测试'
__plugin_usage__ = r"""
素性测试

使用方法：素性测试 [待测整数]
在小于3,317,044,064,679,887,385,961,981时保证答案正确
""".strip()


def try_prime(pickup, d, n, s):
    if pow(pickup, d, n) == 1:
        return False
    for i in range(s):
        if pow(pickup, 2**i * d, n) == n - 1:
            return False
    return True


def is_prime(n):
    if n in (0, 1):
        return False
    if n in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
        return True
    d, s = n - 1, 0
    while not d % 2:
        d, s = d >> 1, s + 1
    return not any(
        try_prime(
            pickup,
            d,
            n,
            s) for pickup in (
            2,
            3,
            5,
            7,
            11,
            13,
            17,
            19,
            23,
            29,
            31,
            37,
            41,
            43))


@on_command('素性测试', aliases=['素数测试', '素数', '素性', '质数'], only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    arg = session.current_arg_text.strip().lower()
    if not arg:
        await session.send("使用方法：素性测试 [待测整数]")
        return
    else:
        try:
            n = int(arg)
        except BaseException:
            await session.send("爬爬爬")
            return
    if n < 0:
        n = -n
    answer = is_prime(n)
    if not answer:
        await session.send(
            "不是素数")
    else:
        if n < 3317044064679887385961981:
            await session.send(
                "是素数")
        else:
            await session.send(
                "很可能是素数")
    return
