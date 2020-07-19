from blacklist import check_blacklist, check_whitelist
import nonebot
import csv
from nonebot import on_command, CommandSession
import sys
sys.path.insert(0, r"C:\Users\Administrator\Desktop\qqbot\qqbot\plugins")

__plugin_name__ = '查询'
__plugin_usage__ = r"""
查询

使用方法：查询本科/查询硕博/查询教师 [姓名/学（工）号/拼音首字母]
或 查询学号 [学工号]
或 查询姓名 [姓名]
""".strip()


def get_undergraduate(undergraduate):
    with open(r'C:\Users\Administrator\Desktop\qqbot\qqbot\plugins\database\UndergraduateOutput.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        mylist = []
        for row in spamreader:
            if row[5] == undergraduate or row[0] == undergraduate or row[1] == undergraduate:
                mylist.append(row)
        csvfile.close()
        return mylist


def get_graduate(graduate):
    with open(r'C:\Users\Administrator\Desktop\qqbot\qqbot\plugins\database\GraduateOutput.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        mylist = []
        for row in spamreader:
            if row[5] == graduate or row[0] == graduate or row[1] == graduate:
                mylist.append(row)
        csvfile.close()
        return mylist


def get_teacher(teacher):
    with open(r'C:\Users\Administrator\Desktop\qqbot\qqbot\plugins\database\TeacherOutput.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        mylist = []
        for row in spamreader:
            if row[4] == teacher or row[0] == teacher or row[1] == teacher:
                mylist.append(row)
        csvfile.close()
        return mylist


def get_by_name(name):
    with open(r'C:\Users\Administrator\Desktop\qqbot\qqbot\plugins\database\CompleteOutput.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        mylist = []
        for row in spamreader:
            if row[1] == name:
                mylist.append(row)
        csvfile.close()
        return mylist


def get_by_id(id):
    with open(r'C:\Users\Administrator\Desktop\qqbot\qqbot\plugins\database\CompleteOutput.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        mylist = []
        for row in spamreader:
            if row[0] == id:
                mylist.append(row)
        csvfile.close()
        return mylist


@on_command('查询拼音', aliases=("拼音查询",), only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    else:
        await session.send("命令已弃用。当前可用命令为 1)查询本科/查询硕博/查询教师，可以相应范围内精确查找姓名，学（工）号或拼音首字母。2)查询姓名/查询学号，可以在全部范围内精确查找姓名/学（工）号。")
    return


@on_command('查询本科', aliases=('本科查询',), only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    arg = session.current_arg_text.strip().lower()
    if not arg:
        arg = session.get('arg', prompt='请输入查询内容')
    mylist = get_undergraduate(arg)
    if mylist:
        await session.send("\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4]) for i in mylist))
    else:
        await session.send("本次查询无结果")
    return


@on_command('查询教师', aliases=('教师查询',), only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    arg = session.current_arg_text.strip().lower()
    if not arg:
        arg = session.get('arg', prompt='请输入查询内容')
    mylist = get_teacher(arg)
    if mylist:
        base_str_list = []
        for i in mylist:
            base_str = i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[5]
            if i[6]:
                base_str += "\n" + "办公电话：" + i[6]
            if i[7]:
                base_str += "\n" + "手机：" + i[7]
            if i[8]:
                base_str += "\n" + "邮箱：" + i[8]
            if i[9]:
                base_str += "\n" + "简介：" + i[9]
            base_str_list.append(base_str)
        await session.send("\n".join(k for k in base_str_list))
    else:
        await session.send("本次查询无结果")
    return


@on_command('查询硕博', aliases=('硕博查询',), only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    arg = session.current_arg_text.strip().lower()
    if not arg:
        arg = session.get('arg', prompt='请输入查询内容')
    mylist = get_graduate(arg)
    if mylist:
        await session.send("\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4] + " " + i[6]) for i in mylist))
    else:
        await session.send("本次查询无结果")
    return


@on_command('查询姓名', aliases=('姓名查询', '名称查询', '查询名称'), only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    arg = session.current_arg_text.strip().lower()
    if not arg:
        arg = session.get('arg', prompt='请输入查询内容')
    mylist = get_by_name(arg)
    if mylist:
        await session.send(
            "\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4] + " " + i[5]) for i in mylist))
    else:
        await session.send("本次查询无结果")
    return


@on_command('查询学号', aliases=('学号查询', '工号查询', '查询工号'), only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    arg = session.current_arg_text.strip().lower()
    if not arg:
        arg = session.get('arg', prompt='请输入查询内容')
    mylist = get_by_id(arg)
    if mylist:
        await session.send(
            "\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4] + " " + i[5]) for i in mylist))
    else:
        await session.send("本次查询无结果")
    return
