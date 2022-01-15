from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import matchers

# 实现一个响应器 用来恢复机器人所包含的功能
help = on_command('菜单', aliases={'功能', '帮助'}, rule=to_me(), block=True)


@help.handle()
async def _():
    msg = 'YuanBot支持:\n'
    c = 0  # 初始化一个计数器
    matchers_list = sorted(matchers.items(), key=lambda x: x[0])
    for index, matcher_list in matchers_list:
        for matcher in matcher_list:
            if matcher.plugin_name and matcher.__doc__:
                c += 1
                msg += f'{c}.{matcher.plugin_name}：{matcher.__doc__}\n'
    await help.finish(msg)
