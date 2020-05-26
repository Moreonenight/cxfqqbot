import nonebot
from nonebot import on_command, CommandSession
import requests

__plugin_name__ = '离散对数'
__plugin_usage__ = r"""
离散对数

使用方法：离散对数 [模数 m] [原根 a] [幂 b]
亦即求解 b = a ** i (mod m)，输出指数 i，不保证能求出结果
""".strip()

def find_discrete_log(mod_number, root, integer):
    true = True
    false = False
    url = "https://sagecell.sagemath.org/service"
    data = {
        "code": '''
ZmodN = Zmod({mod_number})
m = ZmodN({integer})
base = ZmodN({root})
print(m.log(base))
        '''.format(mod_number = mod_number, integer = integer, root = root).strip()
    }
    r = requests.post(url, data=data)
    result = eval(r.text)
    if result["success"]:
        return result["stdout"].strip()
    else:
        return "没求出来。注意 a 必须是原根，否则离散对数无定义。输入“离散对数”四个字可以查看使用方法"
        
@on_command('离散对数', only_to_me = False)
async def _(session: CommandSession):    
    if session.ctx.get('user_id') in (数据删除, 数据删除, 数据删除):
        return None
    arg = session.current_arg_text.strip().lower()
    if not arg:
        await session.send("使用方法：离散对数 [模数 m] [原根 a] [幂 b]，亦即求解 b = a ** i (mod m)，输出指数 i")
        return
    else:
        tmp_list = arg.split()
        if len(tmp_list) != 3:
            await session.send("爬爬爬")
            return            
        try:
            mod_number, integer, root = (int(i) for i in tmp_list)
            if mod_number <= 0 or root <= 0 or integer <= 0:
                await session.send("爬爬爬")
                return
        except:
            await session.send("爬爬爬")
            return
    await session.send("在求了在求了")
    answer = find_discrete_log(mod_number, root, integer)
    await session.send(answer)
    return    
