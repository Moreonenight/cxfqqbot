import nonebot
import requests
from nonebot import on_command, CommandSession

__plugin_name__ = '知乎热榜'
__plugin_usage__ = r"""
知乎热榜

使用方法：知乎热榜 [显示条数]
""".strip()

_can_zhihu = True

def get_zhihu_hot(n):
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
	r = requests.get(url, headers=headers)
	src = []
	for i in range(n):
		tmp = str(i+1) + '. ' + eval(r.text)["data"][i]["target"]["title"]
		src.append(tmp)
	return src

@on_command('知乎热榜', aliases=['知乎热搜'], only_to_me = False)
async def _(session: CommandSession):
	global _can_zhihu
	if(_can_zhihu == False):
		await session.send("爬嘞您喽")
		return		
	arg = session.current_arg_text.strip().lower()
	if not arg:
		n = 10
	else:
		try:
			n = int(arg)
		except:
			await session.send("爬爬爬")
			return
	mylist = get_zhihu_hot(n)
	await session.send(
		'知乎热榜：\n' + '\n'.join(i for i in mylist))
	return

@on_command('禁止知乎热榜', aliases=['禁止知乎热搜'], only_to_me = False)
async def _(session: CommandSession):
	global _can_zhihu
	_can_zhihu = False
	await session.send(
		'收到')
	return
	
@on_command('可以知乎热榜', aliases=['可以知乎热搜'], only_to_me = False)
async def _(session: CommandSession):
	global _can_zhihu
	_can_zhihu = True
	await session.send(
		'收到')
	return
