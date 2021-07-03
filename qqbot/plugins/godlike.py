from nonebot import on_command, CommandSession, scheduler, permission as perm
from random import randint
from blacklist import check_blacklist, check_whitelist
import sys
sys.path.insert(0, r"C:\Users\Administrator\Desktop\qqbot\qqbot\plugins")

__plugin_name__ = '神威'
__plugin_usage__ = r"""
神威

神 【数据删除】 999
神威：转换技，出牌阶段，阳：你可以用一张手牌与若干角色同时拼点。若你赢，没赢的角色选择一项：1.失去1点体力；2.交给你1张牌并令你获得1个“强”标记。当你有2个或更多“强”标记时，你弃掉所有“强”标记，然后回复1点体力并增加1点体力上限；阴：你可将全部手牌扣置于武将牌上（称为“弱”），直到你的下个出牌阶段开始，当你将要受到伤害时，你可以移去一张“弱”并防止该伤害。你的下个出牌阶段开始时，你将武将牌上的“弱”置入手牌。
神明：游戏开始时，你废除判定区。出牌阶段，你可以减1点体力上限，然后切换转换技。
""".strip()

# 唯有历经试炼者方可聆听神谕
luyan_yin = [
    '''
【数据删除】
''',
]

victim_list_yin = []
victim_list_yang = []


def get_yinyang_list(mode=None):
    global victim_list_yin
    global victim_list_yang
    global luyan_yin
    global luyan_yang
    if mode != 'yin' and mode != 'yang':
        tmp = randint(0, 1)
        if tmp == 1:
            mode = "yin"
        else:
            mode = "yang"
    if mode == "yin":
        while True:
            tmp = randint(0, len(luyan_yin) - 1)
            if tmp not in victim_list_yin:
                victim_list_yin.append(tmp)
                return luyan_yin[tmp]
            else:
                victim_list_yin.remove(tmp)
    if mode == "yang":
        while True:
            tmp = randint(0, len(luyan_yang) - 1)
            if tmp not in victim_list_yang:
                victim_list_yang.append(tmp)
                return luyan_yang[tmp]
            else:
                victim_list_yang.remove(tmp)


@on_command('神威', only_to_me=False)
async def shenwei(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    if session.ctx.get('group_id') == 【数据删除】:
        return None
    arg = session.current_arg_text.strip().lower()
    if arg == "阴":
        profile = get_yinyang_list(mode='yin').strip().split("\n")
    elif arg == "阳":
        profile = get_yinyang_list(mode='yang').strip().split("\n")
    else:
        profile = get_yinyang_list().strip().split("\n")
    for text in profile:
        await session.send(text)
