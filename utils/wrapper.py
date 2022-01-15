from functools import wraps
from nonebot.log import logger
from nonebot import get_driver


def check_switch(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        driver = get_driver()
        logger.info('开始权限校验')
        matcher = kwargs.get('matcher')
        plugin_name = matcher.plugin_name  # 获取插件名
        event = kwargs.get('event')
        group_id = event.dict().get('group_id')  # 获取群号
        if group_id:
            switch = driver.litedb.query('select switch from permission where group_id=? and plugin_name=?', (group_id, plugin_name))
            if not switch:
                driver.litedb.execute('insert into permission(group_id, plugin_name, switch) values(?, ?, ?)', (group_id, plugin_name, 1))
                await func(*args, **kwargs)
            else:
                switch = switch[0][0]
                if switch:
                    await func(*args, **kwargs)
                else:
                    await matcher.finish(f'群内未开通该权限 [{plugin_name}]')
        else:
            await func(*args, **kwargs)

    return wrapper


def try_except(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info('异常处理')
        matcher = kwargs.get('matcher')
        try:
            await func(*args, **kwargs)
        except Exception as e:
            if str(e):
                if matcher:
                    await matcher.finish(f'Error:{e}')
            else:
                await matcher.finish()
    return wrapper
