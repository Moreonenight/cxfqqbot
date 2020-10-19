from nonebot import on_command, CommandSession
import requests
import base64
import binascii
import random
import json


from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from string import ascii_letters, digits


__plugin_name__ = '网易云音乐'
__plugin_usage__ = r"""163 <song name>
大小写需要完全匹配"""

_charset = ascii_letters + digits


def rand_char(num=16):
    return ''.join(random.choice(_charset) for _ in range(num))


def padded(msg):
    pad = 16 - len(msg) % 16
    return msg + str(pad * chr(pad))


def aes_encrypt(msg, key, iv='0102030405060708'):
    msg = padded(msg)
    cryptor = AES.new(key.encode(), IV=iv.encode(), mode=AES.MODE_CBC)
    text = cryptor.encrypt(msg.encode())
    text = base64.b64encode(text)
    return text


def gen_params(d, i):
    text = aes_encrypt(d, '0CoJUm6Qyw8W8jud')
    text = text.decode()
    text = aes_encrypt(text, i)
    return text


def rsa_encrypt(msg):
    msg = binascii.b2a_hex(msg[::-1].encode())
    msg = int(msg, 16)
    text = 1
    for _ in range(0x10001):
        text *= msg
        text %= 0x00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7
    return format(text, 'x')


def encrypt(query):
    query = json.dumps(query)
    rand_i = rand_char(16)
    params = gen_params(query, rand_i)
    enc_sec_key = rsa_encrypt(rand_i)
    data = {
        'params': params,
        'encSecKey': enc_sec_key
    }
    return data


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'music.163.com',
    'Referer': 'https://music.163.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.130 Safari/537.36 '
}

# query = "タイニーリトル・アジアンタム"


@on_command('163', aliases=["网易云"], only_to_me=False)
async def netease_music(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    # await session.send("在使用 mirai 的情况下无法发送自定义的音乐消息，所以该功能已停用。")
    # return
    song_name = session.get('arg', prompt='乐曲名？')
    # 获取城市的天气预报
    result = await get_163_music_(song_name)
    if result == -114514:
        await session.send("似乎没有找到")
    elif result == -114513:
        await session.send("根本什么都没有")
    elif result == -114512:
        await session.send("和服务器的连接可能发生错误，请稍后再试")
    else:
        await session.send("[CQ:music,type=163,id=" + str(result) + "]")


@netease_music.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['arg'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('乐曲名？')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


async def get_163_music_(query: str) -> int:
    payload = {
        "hlpretag": "<span class=\"s-fc7\">",
        "hlposttag": "</span>",
        "s": query,
        "type": "1",
        "offset": "0",
        "total": "true",
        "limit": "30",
        "csrf_token": ""
    }
    request_body = encrypt(payload)

    r = requests.post("https://music.163.com/weapi/cloudsearch/get/web?csrf_token=", headers=headers, data=request_body)
    decode_headers = {
    "Content-Type": "text/plain",
    }
    true = True
    false = False
    proxies = {
        "http": "http://127.0.0.1:9876",
        "https": "https://127.0.0.1:9876"
    }    
    decode_r = requests.post("https://netease-music-abroad-decode.vercel.app/api/decode", data=(eval(r.text))["result"], headers=decode_headers, proxies=proxies)
    try:
        result = json.loads(decode_r.text)
    except json.decoder.JSONDecodeError:
        return -114512
    try:
        song_list_length = len(result['songs'])
    except KeyError:
        return -114513
    for i in range(0, song_list_length):
        target = result['songs'][i]['name']
        try:
            begin = target.index(query)
        except ValueError:
            continue
            # print(result['result']['songs'][i]['name'])
        return result['songs'][i]['id']
    return -114514
