import nonebot
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import on_command

# echo = on_command("echo", to_me()) 官方代码
echo = on_command("echo", rule=to_me(), block=True, priority=4)  # block 阻断向低级响应传递
echo.__doc__ = '''复读机
    使用方法: echo xxxx'''


@echo.handle()
async def echo_escape(message: Message = CommandArg()):
    await echo.send(message=message)
