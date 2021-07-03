import sys
sys.path.insert(0, r"C:\Users\Administrator\Desktop\qqbot\qqbot\plugins")
from blacklist import check_blacklist, check_whitelist
import nonebot
import csv
from nonebot import on_command, CommandSession
import editdistance
import pickle

__plugin_name__ = '查询'
__plugin_usage__ = r"""
查询

使用方法：查询本科/查询硕博/查询教师 [姓名/学（工）号/拼音首字母]
或 查询学号 [学工号]
或 查询姓名 [姓名]
""".strip()

with open(r"C:\Users\Administrator\Desktop\qqbot\qqbot\plugins\database\full_stu.pickle", "rb") as picklefile:
    full_stu_list = pickle.load(picklefile)
with open(r"C:\Users\Administrator\Desktop\qqbot\qqbot\plugins\database\school.pickle", "rb") as picklefile:
    school_dict = pickle.load(picklefile)
with open(r"C:\Users\Administrator\Desktop\qqbot\qqbot\plugins\database\major.pickle", "rb") as picklefile:
    major_dict = pickle.load(picklefile)


def judge_identity(id):
    if len(id) == 7 and id[2] == "5":
        return "undergraduated"
    elif len(id) == 7:
        return "graduated"
    else:
        return "teacher"


def get_undergraduate(undergraduate):
    mylist = []
    with open(r'C:\Users\Administrator\Desktop\qqbot\qqbot\plugins\database\UndergraduateOutput.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        for row in spamreader:
            if row[5] == undergraduate or row[0] == undergraduate or row[1] == undergraduate:
                mylist.append(row)
    fullList = []
    for stu in full_stu_list:
        if (stu["姓名"] == undergraduate or stu["学号"] ==
                undergraduate) and judge_identity(stu["学号"]) == "undergraduated":
            fullList.append([stu["学号"], stu["姓名"], stu["性别"], convert_school(
                school_dict, stu["学院"]), convert_major(major_dict, stu["专业"]), ""])
    tmpList = []
    for stu in mylist:
        tmpList.append(stu[0])
    for stu in fullList:
        if stu[0] not in tmpList:
            mylist.append(stu)
    return mylist


def get_graduate(graduate):
    mylist = []
    with open(r'C:\Users\Administrator\Desktop\qqbot\qqbot\plugins\database\GraduateOutput.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        for row in spamreader:
            if row[5] == graduate or row[0] == graduate or row[1] == graduate:
                mylist.append(row)
    fullList = []
    for stu in full_stu_list:
        if (stu["姓名"] == graduate or stu["学号"] ==
                graduate) and judge_identity(stu["学号"]) == "graduated":
            fullList.append([stu["学号"], stu["姓名"], stu["性别"], convert_school(
                school_dict, stu["学院"]), convert_major(major_dict, stu["专业"]), "", ""])
    tmpList = []
    for stu in mylist:
        tmpList.append(stu[0])
    for stu in fullList:
        if stu[0] not in tmpList:
            mylist.append(stu)
    return mylist


def get_teacher(teacher):
    mylist = []
    with open(r'C:\Users\Administrator\Desktop\qqbot\qqbot\plugins\database\TeacherOutput.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        for row in spamreader:
            if row[4] == teacher or row[0] == teacher or row[1] == teacher:
                mylist.append(row)
    return mylist


def get_by_name(name):
    mylist = []
    with open(r'C:\Users\Administrator\Desktop\qqbot\qqbot\plugins\database\CompleteOutput.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        for row in spamreader:
            if row[1] == name:
                mylist.append(row)
    fullList = []
    for stu in full_stu_list:
        if stu["姓名"] == name:
            fullList.append([stu["学号"], stu["姓名"], stu["性别"], convert_school(
                school_dict, stu["学院"]), convert_major(major_dict, stu["专业"]), ""])
    tmpList = []
    for stu in mylist:
        tmpList.append(stu[0])
    for stu in fullList:
        if stu[0] not in tmpList:
            mylist.append(stu)
    return mylist


def get_by_name_fuzzy(name):
    with open(r'C:\Users\Administrator\Desktop\qqbot\qqbot\plugins\database\CompleteOutput.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        mylist = []
        for row in spamreader:
            if editdistance.eval(row[1], name) in (0, 1):
                mylist.append(row)
        return mylist


def convert_school(school_dict, school):
    if school in school_dict.keys():
        return school_dict[school]
    else:
        return "未知学院号（" + school + "）"


def convert_major(major_dict, major):
    if major in major_dict.keys():
        return major_dict[major]
    else:
        return "未知专业号（" + major + "）"


def get_by_id(id):
    mylist = []
    with open(r'C:\Users\Administrator\Desktop\qqbot\qqbot\plugins\database\CompleteOutput.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        for row in spamreader:
            if row[0] == id:
                mylist.append(row)
    fullList = []
    for stu in full_stu_list:
        if stu["学号"] == id:
            fullList.append([stu["学号"], stu["姓名"], stu["性别"], convert_school(
                school_dict, stu["学院"]), convert_major(major_dict, stu["专业"]), ""])
    tmpList = []
    for stu in mylist:
        tmpList.append(stu[0])
    for stu in fullList:
        if stu[0] not in tmpList:
            mylist.append(stu)
    return mylist


def split_array(arrayToSplit, step=10):
    splitarray = [arrayToSplit[i:i + step]
                  for i in range(0, len(arrayToSplit), step)]
    return splitarray


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
    split_flag = False
    if session.ctx.get('group_id') is None:
        split_flag = True
    # split_flag = False
    # split_flag = True
    arg = session.current_arg_text.strip().lower()
    if not arg:
        arg = session.get('arg', prompt='请输入查询内容')
    mylist = get_undergraduate(arg)
    if mylist:
        if split_flag:
            listToSend = split_array(mylist)
            for myArray in listToSend:
                await session.send(
                    "\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4]) for i in myArray))
        else:
            await session.send(
                "\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4]) for i in mylist))
    else:
        if arg.encode('UTF-8').isalnum() == False:
            mylist = get_by_name(arg)
            if mylist:
                await session.send("本次查询无结果。但你是否在找：\n" + "\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4] + " " + i[5]) for i in mylist))
                return
        await session.send("本次查询无结果")
    return


@on_command('查询教师', aliases=('教师查询',), only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    split_flag = False
    if session.ctx.get('group_id') is None:
        split_flag = True
    # split_flag = False
    # split_flag = True
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
        if arg.encode('UTF-8').isalnum() == False:
            mylist = get_by_name(arg)
            if mylist:
                await session.send("本次查询无结果。但你是否在找：\n" + "\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4] + " " + i[5]) for i in mylist))
                return
        await session.send("本次查询无结果")
    return


@on_command('查询硕博', aliases=('硕博查询',), only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    split_flag = False
    if session.ctx.get('group_id') is None:
        split_flag = True
    # split_flag = False
    # split_flag = True
    arg = session.current_arg_text.strip().lower()
    if not arg:
        arg = session.get('arg', prompt='请输入查询内容')
    mylist = get_graduate(arg)
    if mylist:
        if split_flag:
            listToSend = split_array(mylist)
            for myArray in listToSend:
                await session.send(
                    "\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4] + " " + i[6]) for i in myArray))
        else:
            await session.send(
                "\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4] + " " + i[6]) for i in mylist))
    else:
        if arg.encode('UTF-8').isalnum() == False:
            mylist = get_by_name(arg)
            if mylist:
                await session.send("本次查询无结果。但你是否在找：\n" + "\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4] + " " + i[5]) for i in mylist))
                return
        await session.send("本次查询无结果")
    return


@on_command('查询姓名', aliases=('姓名查询', '名称查询', '查询名称'), only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    split_flag = False
    if session.ctx.get('group_id') is None:
        split_flag = True
    # split_flag = False
    # split_flag = True
    arg = session.current_arg_text.strip().lower()
    if not arg:
        arg = session.get('arg', prompt='请输入查询内容')
    mylist = get_by_name(arg)
    if mylist:
        if split_flag:
            listToSend = split_array(mylist)
            for myArray in listToSend:
                await session.send(
                    "\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4] + " " + i[5]) for i in myArray))
        else:
            await session.send(
                "\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4] + " " + i[5]) for i in mylist))
    else:
        if arg.encode('UTF-8').isalnum() == False and len(arg) > 2:
            mylist = get_by_name_fuzzy(arg)
            if mylist and len(mylist) <= 10:
                await session.send("本次查询无结果。但你是否在找：\n" + "\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4] + " " + i[5]) for i in mylist))
                return
        await session.send("本次查询无结果")
    return


@on_command('查询学号', aliases=('学号查询', '工号查询', '查询工号'), only_to_me=False)
async def _(session: CommandSession):
    if check_blacklist(session.ctx.get('user_id')):
        return None
    if not check_whitelist(session.ctx.get('group_id')):
        return None
    split_flag = False
    if session.ctx.get('group_id') is None:
        split_flag = True
    # split_flag = False
    split_flag = True
    arg = session.current_arg_text.strip().lower()
    if not arg:
        arg = session.get('arg', prompt='请输入查询内容')
    mylist = get_by_id(arg)
    if mylist:
        if split_flag:
            listToSend = split_array(mylist)
            for myArray in listToSend:
                await session.send(
                    "\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4] + " " + i[5]) for i in myArray))
        else:
            await session.send(
                "\n".join((i[0] + " " + i[1] + " " + i[2] + " " + i[3] + " " + i[4] + " " + i[5]) for i in mylist))
    else:
        await session.send("本次查询无结果")
    return
