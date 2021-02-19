import sys
sys.path.insert(0, r"C:\Users\Administrator\Desktop\qqbot\qqbot\plugins")
from blacklist import check_blacklist, check_whitelist
import requests
import json
import pickle
import asyncio
import nonebot
from nonebot import on_command, CommandSession
__plugin_name__ = '彩云小梦'
__plugin_usage__ = r"""
彩云小梦

彩云小梦 拉取模型：拉取可用的写作模型
彩云小梦 列出模型：列出可用的写作模型
彩云小梦 切换模型 [模型名]：切换自己要使用的写作模型
彩云小梦 设置标题 [标题]：设置续写使用的文章标题
彩云小梦 设置内容 [内容]：设置续写使用的文章内容
彩云小梦 续写 [文字]：
如果无参数，则以当前结果追加并接着续写；如果收到文字，则以文字追加（不追加当前结果）；
彩云小梦 切换结果：显示下一条结果
彩云小梦 全文：显示全部已写内容
彩云小梦 重置：回到初始状态
""".strip()

# This uid is prescribed in JavaScripts.
uid = "602de51039b3b5c297cd8915"
try:
    with open("models.pickle", "rb") as pickleFile:
        model_dict = pickle.load(pickleFile)
except(FileNotFoundError):
    model_dict = {}
try:
    with open("contents.pickle", "rb") as pickleFile:
        grand_data_dict = pickle.load(pickleFile)
except(FileNotFoundError):
    grand_data_dict = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
}

# Pull available models


def pull_models():
    url = "http://if.caiyunai.com/v1/dream/model_list"
    data = {
        "ostype": ""
    }
    r = requests.post(url, headers=headers, json=data)
    result = json.loads(r.text)
    global model_dict
    if result["status"] == 0:
        model_dict = {}
        for model in result["data"]["public_rows"]:
            model_dict[model["name"]] = model["mid"]

# Get nid


def get_nid(title, content, nid=None):
    url = "http://if.caiyunai.com/v1/dream/" + uid + "/novel_save"
    if nid is None:
        data = {"content": content, "title": title, "ostype": ""}
    else:
        data = {"content": content, "title": title, "nid": nid, "ostype": ""}
    r = requests.post(url, headers=headers, json=data)
    result = json.loads(r.text)
    if result["status"] == 0:
        nid = result["data"]["nid"]
    return nid

# Get next part of novel


async def get_novel(title, content, mid, nid):
    novel_ai_url = "http://if.caiyunai.com/v1/dream/" + uid + "/novel_ai"
    novel_ai_data = {"nid": nid, "content": content,
                     "uid": uid, "mid": mid, "title": title, "ostype": ""}
    novel_ai_r = requests.post(
        novel_ai_url, headers=headers, json=novel_ai_data)
    novel_ai_result = json.loads(novel_ai_r.text)
    xid = None
    if novel_ai_result["status"] == 0:
        xid = novel_ai_result["data"]["xid"]
    if xid is not None:
        novel_dream_loop_url = "http://if.caiyunai.com/v1/dream/" + uid + "/novel_dream_loop"
        novel_dream_loop_data = {"nid": nid, "xid": xid, "ostype": ""}
        while(True):
            await asyncio.sleep(0.5)
            novel_dream_loop_r = requests.post(
                novel_dream_loop_url, headers=headers, json=novel_dream_loop_data)
            novel_dream_loop_result = json.loads(novel_dream_loop_r.text)
            if novel_dream_loop_result["data"]["count"] == 0:
                result = []
                for item in novel_dream_loop_result["data"]["rows"]:
                    result.append(item["content"])
                return result


@on_command('彩云小梦', only_to_me=False)
async def _(session: CommandSession):
    global grand_data_dict
    user_id = session.ctx.get('user_id')
    if check_blacklist(user_id):
        return None
    group_id = session.ctx.get('group_id')
    arg = session.current_arg_text.strip()
    if not arg:
        arg = session.get('arg', prompt='请问要做什么？')
        if arg.startswith("彩云小梦"):
            arg = arg[4:].strip()
    if arg.startswith("拉取模型"):
        pull_models()
        await session.send("拉取完成")
        with open("models.pickle", "wb") as pickleFile:
            pickle.dump(model_dict, pickleFile)
        return
    if arg.startswith("列出模型"):
        await session.send("当前可用模型包括：" + '、'.join(model_dict.keys()))
        return
    if user_id not in grand_data_dict.keys():
        grand_data_dict[user_id] = {}
    if group_id not in grand_data_dict[user_id].keys():
        grand_data_dict[user_id][group_id] = {
            "title": "", "content": "", "currentOptions": [""], "model": "小梦0号", "nid": None}
    if arg.startswith("切换模型"):
        grand_data_dict[user_id][group_id]["model"] = arg.split()[1]
        await session.send("您使用的模型已切换为" + arg.split()[1])
        with open("contents.pickle", "wb") as pickleFile:
            pickle.dump(grand_data_dict, pickleFile)
        return
    if arg.startswith("续写"):
        try:
            mid = model_dict[grand_data_dict[user_id][group_id]["model"]]
        except(KeyError):
            await session.send("写作模型不存在，请切换为正确的模型")
            return
        if len(arg) != 2 and len(arg.split()) != 1:
            grand_data_dict[user_id][group_id]["content"] += arg[2:].strip()
        else:
            grand_data_dict[user_id][group_id]["content"] += grand_data_dict[user_id][group_id]["currentOptions"][0]
        if grand_data_dict[user_id][group_id]["title"] == "" and grand_data_dict[user_id][group_id]["content"] == "":
            await session.send("标题和内容不能全空，请先“彩云小梦 设置标题 [标题]”或“彩云小梦 设置内容 [内容]”")
            return
        if grand_data_dict[user_id][group_id]["nid"] is None:
            grand_data_dict[user_id][group_id]["nid"] = get_nid(
                grand_data_dict[user_id][group_id]["title"], grand_data_dict[user_id][group_id]["content"])
        novel_text_list = await get_novel(grand_data_dict[user_id][group_id]["title"], grand_data_dict[user_id][group_id]["content"], mid, grand_data_dict[user_id][group_id]["nid"])
        grand_data_dict[user_id][group_id]["currentOptions"] = novel_text_list
        result = grand_data_dict[user_id][group_id]["currentOptions"][0]
        if len(grand_data_dict[user_id][group_id]["content"]) >= 100:
            result = "[" + grand_data_dict[user_id][group_id]["content"][-100:] + "]" + result
        await session.send(result)
        with open("contents.pickle", "wb") as pickleFile:
            pickle.dump(grand_data_dict, pickleFile)
        return
    if arg.startswith("切换结果"):
        if grand_data_dict[user_id][group_id]["currentOptions"][0] == "":
            await session.send("尚未进行过续写")
            return
        del grand_data_dict[user_id][group_id]["currentOptions"][0]
        if len(grand_data_dict[user_id][group_id]["currentOptions"]) == 0:
            try:
                mid = model_dict[grand_data_dict[user_id][group_id]["model"]]
            except(KeyError):
                await session.send("写作模型不存在，请切换为正确的模型")
                return
            novel_text_list = await get_novel(grand_data_dict[user_id][group_id]["title"], grand_data_dict[user_id][group_id]["content"], mid, grand_data_dict[user_id][group_id]["nid"])
            if novel_text_list:
                grand_data_dict[user_id][group_id]["currentOptions"] = novel_text_list
            else:
                return session.send("彩云小梦似乎出了些故障，请重新尝试续写")
        result = grand_data_dict[user_id][group_id]["currentOptions"][0]
        if len(grand_data_dict[user_id][group_id]["content"]) >= 100:
            result = "[" + grand_data_dict[user_id][group_id]["content"][-100:] + "]" + result
        await session.send(result)
        with open("contents.pickle", "wb") as pickleFile:
            pickle.dump(grand_data_dict, pickleFile)
        return
    if arg.startswith("全文"):
        await session.send(grand_data_dict[user_id][group_id]["title"] + "\n" + grand_data_dict[user_id][group_id]["content"])
        return
    if arg == "重置":
        del grand_data_dict[user_id][group_id]
        await session.send("已重置")
        with open("contents.pickle", "wb") as pickleFile:
            pickle.dump(grand_data_dict, pickleFile)
        return
    if arg.startswith("设置标题"):
        if len(arg) != 2 and len(arg.split()) != 1:
            grand_data_dict[user_id][group_id]["title"] = arg[4:].strip()
            await session.send("标题设置成功")
            with open("contents.pickle", "wb") as pickleFile:
                pickle.dump(grand_data_dict, pickleFile)
        return
    if arg.startswith("设置内容"):
        if len(arg) != 2 and len(arg.split()) != 1:
            grand_data_dict[user_id][group_id]["content"] = arg[4:].strip()
            await session.send("内容设置成功")
            with open("contents.pickle", "wb") as pickleFile:
                pickle.dump(grand_data_dict, pickleFile)
        return
    await session.send("未知命令，请输入“@[bot] help 彩云小梦”查看说明。")
    return
