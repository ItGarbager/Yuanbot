from nonebot.matcher import Matcher
from nonebot.plugin import on_regex
from nonebot.adapters.onebot.v11 import Message, unescape

test = on_regex("run\s*(.+)", block=True)
test.__doc__ = r'''测试回复
    使用方法: run xxxx'''


@test.handle()
async def _(matcher: Matcher):
    command = matcher.state['_matched_groups']
    await test.finish(Message(unescape(command[0])))
