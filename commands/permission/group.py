from nonebot import get_driver
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import Arg
from nonebot.plugin import on_regex
from nonebot.adapters.onebot.v11 import MessageEvent

from utils.wrapper import try_except

switch = on_regex(r'(.+)权限([开关])', block=True, priority=4, permission=SUPERUSER)  # block 阻断向低级响应传递
switch.__doc__ = '''权限管理
    使用方法: 功能名 开/关'''

driver = get_driver()


@switch.handle()
@try_except
async def _(matcher: Matcher, event: MessageEvent):
    state = matcher.state
    plugin_name, is_switch = state["_matched_groups"]
    switch_int = is_switch == '开' and 1 or 0
    group_id = event.dict().get('group_id')
    if group_id:

        res = driver.litedb.query('select switch from permission where group_id=? and plugin_name=?', (group_id, plugin_name))
        if res:
            if res[0][0] - switch_int:
                driver.litedb.execute('update permission set switch=? where group_id=? and plugin_name=?',
                                      (switch_int, group_id, plugin_name))
                await switch.finish(f'功能 {plugin_name} => {is_switch}')
            else:
                await switch.finish(f'无需修改，功能 {plugin_name} 当前即为[{is_switch}]')
        else:
            driver.litedb.execute('insert into permission(group_id, plugin_name, switch) values(?, ?, ?)',
                                  (group_id, plugin_name, switch_int))
            await switch.finish(f'功能 {plugin_name} => {is_switch}')
    else:
        matcher.set_arg("plugin_name", plugin_name)
        matcher.set_arg("switch_int", switch_int)
        matcher.set_arg("is_switch", is_switch)


@switch.got("group_id", prompt="请问是哪个群呢？")
@try_except
async def _(matcher: Matcher, group_id: Message = Arg()):
    switch_int = matcher.get_arg('switch_int')
    plugin_name = matcher.get_arg('plugin_name')
    is_switch = matcher.get_arg('is_switch')
    group_id = str(group_id)
    if not group_id.isdigit():
        raise Exception('请输入群号！！')
    group_id = int(group_id)
    print(plugin_name, type(plugin_name))
    res = driver.litedb.query('select switch from permission where group_id=? and plugin_name=?', (group_id, plugin_name))
    if res:
        if res[0][0] - switch_int:
            driver.litedb.execute('update permission set switch=? where group_id=? and plugin_name=?',
                                  (switch_int, group_id, plugin_name))
            await switch.send(f'功能 {plugin_name} => {is_switch}')
        else:
            await switch.send(f'无需修改，功能 {plugin_name} 当前即为[{is_switch}]')
    else:
        driver.litedb.execute('insert into permission(group_id, plugin_name, switch) values(?, ?, ?)',
                              (group_id, plugin_name, switch_int))
        await switch.send(f'功能 {plugin_name} => {is_switch}')
