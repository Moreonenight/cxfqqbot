from datetime import datetime
from datetime import timedelta
from nonebot import on_command, CommandSession, scheduler, permission as perm
from nonebot import on_natural_language, NLPSession, NLPResult
from nonebot.message import unescape
from apscheduler.triggers.date import DateTrigger

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
from random import randint

victim_list = []

_can_auto_check = False
_can_random_check = False


def get_random_list():
    random_check_list = [
        ["Amdahl定律", "当对一个系统中的某个部件进行改进后，所能获得的整个系统性能的提高，受限于该部件的执行时间占总执行时间的百分比。"],
        ["程序的局部性原理", "程序执行时所访问的存储器地址不是随机分布的，而是相对地簇聚。包括时间局部性和空间局部性。"],
        ["虚拟机", "用软件实现的机器。"],
        ["翻译", "先用转换程序把高一级机器上的程序转换为低一级机器上等效的程序，然后再在这低一级机器上运行，实现程序的功能。"],
        ["解释", "对于高一级机器上的程序中的每一条语句或指令，都是转去执行低一级机器上的一段等效程序。执行完后，再去高一级机器取下一条语句或指令，再进行解释执行，如此反复，直到解释执行完整个程序。"],
        ["系统加速比", "对系统中某部分进行改进时，改进后系统性能提高的倍数。"],
        ["软件兼容", "一个软件可以不经修改或者只需少量修改就可以由一台计算机移植到另一台计算机上运行。差别只是执行时间的不同。"],
        ["耦合度", "反映多机系统中各计算机之间物理连接的紧密程度和交互作用能力的强弱。"],
        ["数据相关", "考虑两条指令i和j，i在j的前面，如果下述条件之一成立，则称指令j与指令i数据相关：（1）指令j 使用指令i 产生的结果；（2）指令j与指令k数据相关，而指令k又与指令i数据相关。"],
        ["向后兼容", "按某个时期投入市场的某种型号计算机编制的程序，不加修改地就能运行于在它之后投入市场的计算机。"],
        ["命中时间", "访问Cache命中时所用的时间。"],
        ["定向技术", "用来解决写后读冲突的。在发生写后读相关的情况下，在计算结果尚未出来之前，后面等待使用该结果的指令并不一定马上就要用该结果。如果能够将该计算结果从其产生的地方直接送到其它指令需要它的地方，那么就可以避免停顿。"],
        ["常见的计算机系统结构分类法有哪两种？", "Flynn 分类法、冯氏分类法"],
        ["指令系统编码格式有哪三种？", "变长编码格式、固定长度编码格式、混合型编码格式"],
        ["延迟分支方法有哪3种调度策略？", "从前调度，从目标处调度，从失败处调度"],
        ["现有的MIMD机器可分为哪两类？", "集中式共享存储器结构、分布式存储器结构"],
        ["伪相联的基本思想是什么？", "采用这种方法时，在命中情况下，访问Cache的过程和直接映象Cache中的情况相同；而发生不命中时，在访问下一级存储器之前，会先检查Cache另一个位置（块），看是否匹配。确定这个另一块的一种简单的方法是将索引字段的最高位取反，然后按照新索引去寻找伪相联组中的对应块。如果这一块的标识匹配，则称发生了伪命中。否则，就只好访问下一级存储器。它既能获得多路组相联Cache的低不命中率，又能保持直接映象Cache的命中速度。"],
        ["向上兼容", "按某档计算机编制的程序，不加修改就能运行于比它高档的计算机。"],
        ["仿真", "用一台现有计算机（称为宿主机）上的微程序去解释实现另一台计算机（称为目标机）的指令系统。"],
        ["计算机系统结构的Flynn分类法是按什么来分类的？", "Flynn分类法是按照指令流和数据流的多倍性进行分类。"],
        ["计算机系统结构的Flynn分类法共分为哪几类？", "单指令流单数据流SISD、单指令流多数据流SIMD、多指令流单数据流MISD、多指令流多数据流MIMD"],
        ["RISC", "精简指令集计算机"],
        ["累加器型机器", "CPU 中存储操作数的单元是累加器的机器。"],
        ["寻址方式", "指令系统中如何形成所要访问的数据的地址。一般来说，寻址方式可以指明指令中的操作数是一个常数、一个寄存器操作数或者是一个存储器操作数。"],
        ["数据表示", "硬件结构能够识别、指令系统可以直接调用的那些数据结构。"],
        ["指令集应满足哪几个基本要求？", "完整性、规整性、高效率和兼容性。"],
        ["指令集结构设计所涉及的内容有哪些？", "(1) 指令集功能设计：主要有RISC和CISC两种技术发展方向； (2) 寻址方式的设计：设置寻址方式可以通过对基准程序进行测试统计，察看各种寻址方式的使用频率，根据适用频率设置必要的寻址方式。 (3) 操作数表示和操作数类型：主要的操作数类型和操作数表示的选择有：浮点数据类型、整型数据类型、字符型、十进制数据类型等等。 (4) 寻址方式的表示：可以将寻址方式编码于操作码中，也可以将寻址方式作为一个单独的域来表示。 (5) 指令集格式的设计：有变长编码格式、固定长度编码格式和混合型编码格式3种。"],
        ["简述RISC指令集结构的设计原则。", "（1） 选取使用频率最高的指令，并补充一些最有用的指令；（2）每条指令的功能应尽可能简单，并在一个机器周期内完成；（3）所有指令长度均相同；（4）只有Load和Store操作指令才访问存储器，其它指令操作均在寄存器之间进行； (5) 以简单有效的方式支持高级语言。"],
        ["流水线", "将一个重复的时序过程，分解成为若干个子过程，而每一个子过程都可有效地在其专用功能段上与其它子过程同时执行。"],
        ["单功能流水线", "指流水线的各段之间的连接固定不变、只能完成一种固定功能的流水线。"],
        ["静态流水线", "指在同一时间内，多功能流水线中的各段只能按同一种功能的连接方式工作的流水线。当流水线要切换到另一种功能时，必须等前面的任务都流出流水线之后，才能改变连接。"],
        ["线性流水线", "指各段串行连接、没有反馈回路的流水线。数据通过流水线中的各段时，每一个段最多只流过一次。"],
        ["乱序流水线", "流水线输出端任务流出的顺序与输入端任务流入的顺序可以不同，允许后进入流水线的任务先完成。这种流水线又称为无序流水线、错序流水线、异步流水线。"],
        ["流水线的效率", "即流水线设备的利用率，它是指流水线中的设备实际使用时间与整个运行时间的比值。"],
        ["吞吐率", "在单位时间内流水线所完成的任务数量或输出结果的数量。"],
        ["处理机间流水线", "又称为宏流水线。它是把多个处理机串行连接起来，对同一数据流进行处理，每个处理机完成整个任务中的一部分。前一个处理机的输出结果存入存储器中，作为后一个处理机的输入。"],
        ["名相关", "如果两条指令使用了相同的名，但是它们之间并没有数据流动，则称这两条指令存在名相关。"],
        ["控制相关", "是指由分支指令引起的相关。它需要根据分支指令的执行结果来确定后面该执行哪个分支上的指令。"],
        ["反相关", "考虑两条指令i和j，i在j的前面，如果指令j所写的名与指令i所读的名相同，则称指令i和j发生了反相关。"],
        ["换名技术", "名相关的两条指令之间并没有数据的传送，只是使用了相同的名。可以把其中一条指令所使用的名换成别的，以此来消除名相关。"],
        ["数据冲突", "当指令在流水线中重叠执行时，因需要用到前面指令的执行结果而发生的冲突。"],
        ["读后写冲突", "考虑两条指令i和j，且i在j之前进入流水线，指令j的目的寄存器和指令i的源操作数寄存器相同，而且j在i读取该寄存器之前就先对它进行了写操作，导致i读到的值是错误的。"],
        ["写后写冲突", "考虑两条指令i和j，且i在j之前进入流水线，，指令j和指令i的结果单元（寄存器或存储器单元）相同，而且j在i写入之前就先对该单元进行了写入操作，从而导致写入顺序错误。这时在结果单元中留下的是i写入的值，而不是j写入的。"],
        ["解决流水线瓶颈问题有哪两种常用方法？", "细分瓶颈段、重复设置瓶颈段"],
        ["减少流水线分支延迟的静态方法有哪些？", "（1）预测分支失败：沿失败的分支继续处理指令，就好象什么都没发生似的。当确定分支是失败时，说明预测正确，流水线正常流动；当确定分支是成功时，流水线就把在分支指令之后取出的指令转化为空操作，并按分支目标地址重新取指令执行。（2）预测分支成功：当流水线ID段检测到分支指令后，一旦计算出了分支目标地址，就开始从该目标地址取指令执行。（3）延迟分支：主要思想是从逻辑上“延长”分支指令的执行时间。把延迟分支看成是由原来的分支指令和若干个延迟槽构成。不管分支是否成功，都要按顺序执行延迟槽中的指令。"],
        ["减少流水线分支延迟的静态方法有什么共同特点？", "它们对分支的处理方法在程序的执行过程中始终是不变的。它们要么总是预测分支成功，要么总是预测分支失败。"],
        ["指令级并行", "简称ILP。是指指令之间存在的一种并行性，利用它，计算机可以并行执行两条或两条以上的指令。"],
        ["指令的静态调度", "是指依靠编译器对代码进行静态调度，以减少相关和冲突。它不是在程序执行的过程中、而是在编译期间进行代码调度和优化的。"],
        ["保留站", "在采用Tomasulo算法的MIPS处理器浮点部件中，在运算部件的入口设置的用来保存一条已经流出并等待到本功能部件执行的指令（相关信息）。"],
        ["CDB", "公共数据总线"],
        ["动态分支预测技术", "是用硬件动态地进行分支处理的方法。在程序运行时，根据分支指令过去的表现来预测其将来的行为。如果分支行为发生了变化，预测结果也跟着改变。"],
        ["BHT", "分支历史表。用来记录相关分支指令最近一次或几次的执行情况是成功还是失败，并据此进行预测。"],
        ["前瞻执行", "解决控制相关的方法，它对分支指令的结果进行猜测，然后按这个猜测结果继续取指、流出和执行后续的指令。只是指令执行的结果不是写回到寄存器或存储器，而是放到一个称为ROB的缓冲器中。等到相应的指令得到“确认”（即确实是应该执行的）后，才将结果写入寄存器或存储器。"],
        ["超标量", "一种多指令流出技术。它在每个时钟周期流出的指令条数不固定，依代码的具体情况而定，但有个上限。"],
        ["循环展开", "是一种增加指令间并行性最简单和最常用的方法。它将循环展开若干遍后，通过重命名和指令调度来开发更多的并行性。"],
        ["多级存储层次", "采用不同的技术实现的存储器，处在离CPU不同距离的层次上，各存储器之间一般满足包容关系，即任何一层存储器中的内容都是其下一层（离CPU更远的一层）存储器中内容的子集。目标是达到离CPU最近的存储器的速度，最远的存储器的容量。"],
        ["全相联映象", "主存中的任一块可以被放置到Cache中任意一个地方。"],
        ["直接映象", "主存中的每一块只能被放置到Cache中唯一的一个地方。"],
        ["组相联映象", "主存中的每一块可以放置到Cache中唯一的一组中任何一个地方（Cache分成若干组，每组由若干块构成）。"],
        ["替换算法", "由于主存中的块比Cache中的块多，所以当要从主存中调一个块到Cache中时，会出现该块所映象到的一组（或一个）Cache块已全部被占用的情况。这时，需要被迫腾出其中的某一块，以接纳新调入的块。"],
        ["LRU", "选择最近最少被访问的块作为被替换的块。实际实现都是选择最久没有被访问的块作为被替换的块。"],
        ["写直达法", "在执行写操作时，不仅把信息写入Cache中相应的块，而且也写入下一级存储器中相应的块。"],
        ["按写分配法", "写不命中时，先把所写单元所在的块调入Cache，然后再进行写入。"],
        ["不命中开销", "CPU向二级存储器发出访问请求到把这个数据调入一级存储器所需的时间。"],
        ["强制性不命中", "当第一次访问一个块时，该块不在Cache中，需要从下一级存储器中调入Cache，这就是强制性不命中。"],
        ["冲突不命中", "在组相联或直接映象Cache中，若太多的块映象到同一组（块）中，则会出现该组中某个块被别的块替换（即使别的组或块有空闲位置），然后又被重新访问的情况。"],
        ["请求字优先", "调块时，首先向存储器请求CPU所要的请求字。请求字一旦到达，就立即送往CPU，让CPU继续执行，同时从存储器调入该块的其余部分。"],
        ["2：1 Cache经验规则", "大小为N的直接映象Cache的不命中率约等于大小为N /2的两路组相联Cache的不命中率。"],
        ["相联度", "在组相联中，每组Cache中的块数。"],
        ["降低Cache不命中率有哪几种方法？", "增加Cache块大小。增加块大小利用了程序的空间局部性；增加Cache的容量；提高相联度，降低冲突不命中；伪相联Cache，降低冲突不命中；硬件预取技术。在处理器提出访问请求前预取指令和数据；由编译器控制的预取，硬件预取的替代方法，在编译时加入预取的指令，在数据被用到之前发出预取请求；编译器优化，通过对软件的优化来降低不命中率；“牺牲”Cache。在Cache和其下一级存储器的数据通路之间增设一个全相联的小Cache，存放因冲突而被替换出去的那些块。"],
        ["响应时间", "从用户键入命令开始，到得到结果所花的时间。"],
        ["可靠性", "指系统从某个初始参考点开始一直连续提供服务的能力，它通常用平均无故障时间来衡量。"],
        ["可用性", "指系统正常工作的时间在连续两次正常服务间隔时间中所占的比率。"],
        ["通道", "专门负责整个计算机系统输入/输出工作的专用处理机，能执行有限的一组输入输出指令。"],
        ["RAID0", "亦称数据分块，即把数据分布在多个盘上，实际上是非冗余阵列，无冗余信息。"],
        ["RAID1", "亦称镜像盘，使用双备份磁盘。每当数据写入一个磁盘时，将该数据也写到另一个冗余盘，这样形成信息的两份复制品。如果一个磁盘失效，系统可以到镜像盘中获得所需要的信息。镜像是最昂贵的解决方法。特点是系统可靠性很高，但效率很低。"],
        ["RAID2", "位交叉式海明编码阵列。即数据以位或字节交叉的方式存于各盘，采用海明编码。原理上比较优越，但冗余信息的开销太大，因此未被广泛应用。"],
        ["RAID3", "位交叉奇偶校验盘阵列，是单盘容错并行传输的阵列。即数据以位或字节交叉的方式存于各盘，冗余的奇偶校验信息存储在一台专用盘上。"],
        ["RAID4", "专用奇偶校验独立存取盘阵列。即数据以块(块大小可变)交叉的方式存于各盘，冗余的奇偶校验信息存在一台专用盘上。"],
        ["RAID5", "块交叉分布式奇偶校验盘阵列，是旋转奇偶校验独立存取的阵列。即数据以块交叉的方式存于各盘，但无专用的校验盘，而是把冗余的奇偶校验信息均匀地分布在所有磁盘上。"],
        ["RAID6", "双维奇偶校验独立存取盘阵列。即数据以块(块大小可变)交叉的方式存于各盘，冗余的检、纠错信息均匀地分布在所有磁盘上。并且，每次写入数据都要访问一个数据盘和两个校验盘，可容忍双盘出错。"],
        ["试比较三种通道的优缺点及适用场合。", "（1）字节多路通道。一种简单的共享通道，主要为多台低速或中速的外围设备服务。（2）数组多路通道。适于为高速设备服务。（3）选择通道。为多台高速外围设备（如磁盘存储器等）服务的。"],
        ["监听协议", "每个Cache除了包含物理存储器中块的数据拷贝之外，也保存着各个块的共享状态信息。Cache通常连在共享存储器的总线上，各个Cache控制器通过监听总线来判断它们是否有总线上请求的数据块。"],
        ["目录协议", "用一种专用的存储器所记录的数据结构。它记录着可以进入Cache的每个数据块的访问状态、该块在各个处理器的共享状态以及是否修改过等信息。"],
        ["写作废协议", "在处理器对某个数据项进行写入之前，它拥有对该数据项的唯一的访问权。"],
        ["写更新协议", "当一个处理器对某数据项进行写入时，它把该新数据广播给所有其它Cache。这些Cache用该新数据对其中的副本进行更新。"],
    ]
    global victim_list
    while True:
        tmp = randint(0, len(random_check_list) - 1)
        if tmp not in victim_list:
            victim_list.append(tmp)
            return random_check_list[tmp]
        else:
            victim_list.remove(tmp)
            

@nonebot.scheduler.scheduled_job('interval', minutes=20)
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    if now.hour >= 1 and now.hour <= 7:
        return None
    global _can_auto_check
    if not _can_auto_check:
        return None
    check_list = get_random_list()
    try:
        await bot.send_group_msg(group_id= 【数据删除】,
                                 message='抽查 '+ check_list[0])
        delta = timedelta(seconds=60)
        trigger = DateTrigger(
            run_date=datetime.now() + delta
        )
        scheduler.add_job(
            func=bot.send_group_msg, 
            trigger=trigger,
            kwargs= {'group_id': 【数据删除】, 'message': check_list[0] + "：" + check_list[1]},
            misfire_grace_time=60, 
        )    
    except CQHttpError:
        pass


@on_command('抽查', only_to_me=False)
async def random_check_function(session: CommandSession):
    global _can_random_check
    arg = session.current_arg_text.strip().lower()
    if arg:
        return None
    if not _can_random_check:
        await session.send(
            '无法抽查菜鸡已经挂科的科目。')
        return
    check_list = get_random_list()
    try:
        await session.send('抽查 '+ check_list[0])
        delta = timedelta(seconds=60)
        trigger = DateTrigger(
            run_date=datetime.now() + delta
        )        
        scheduler.add_job(
            func=session.send,  
            trigger=trigger,  
            args=(check_list[0] + "：" + check_list[1],),  
            misfire_grace_time=60,  
        )    
    except CQHttpError:
        pass


@on_command('关闭自动抽查', only_to_me=False)
async def _(session: CommandSession):
    global _can_auto_check
    _can_auto_check = False
    await session.send(
        '收到')
    return


@on_command('开启自动抽查', only_to_me=False)
async def _(session: CommandSession):
    global _can_auto_check
    global _can_random_check
    if _can_random_check:
        _can_auto_check = True
        await session.send(
            '收到')
    else:
        await session.send(
            '无法抽查菜鸡已经挂科的科目。')        
    return

@on_command('关闭抽查', only_to_me=False)
async def _(session: CommandSession):
    global _can_random_check
    _can_random_check = False
    await session.send(
        '收到')
    return


@on_command('开启抽查', only_to_me=False)
async def _(session: CommandSession):
    global _can_random_check
    _can_random_check = True
    await session.send(
        '收到')
    return