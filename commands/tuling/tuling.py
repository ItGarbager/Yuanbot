import json
import aiohttp
from random import choice
from typing import Optional

from nonebot.matcher import Matcher
from nonebot.plugin import on_regex
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Event
from utils.wrapper import check_switch
from utils.encrypt import MD5
from utils.config import TULING_API_KEY

# 定义无法获取图灵回复时的回答

EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～'
)

tuling = on_regex('.+', rule=to_me(), priority=5)
tuling.__doc__ = '智能聊天'


# 注册一个仅内部使用的命令，不需要 aliases

@tuling.handle()
@check_switch
async def _(matcher: Matcher, event: Event):
    Dict = event.dict()
    user_id = Dict.get('user_id')
    if user_id in {}:
        return

    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    message = Dict.get('raw_message')

    # 通过封装的函数获取图灵机器人的回复
    reply = await call_tuling_api(event, message)
    if reply:
        # 如果调用图灵机器人成功，得到了回复，则转义之后发送给用户
        # 转义会把消息中的某些特殊字符做转换，以避免 酷Q 将它们理解为 CQ 码
        await tuling.finish(reply)
    else:
        await tuling.finish(choice(EXPR_DONT_UNDERSTAND))


async def call_tuling_api(event: Event, text: str) -> Optional[str]:
    # 调用图灵机器人的 API 获取回复

    if not text:
        return None

    url = 'http://openapi.tuling123.com/openapi/api/v2'

    # 构造请求数据
    payload = {
        'reqType': 0,
        'perception': {
            'inputText': {
                'text': text
            }
        },
        'userInfo': {
            'apiKey': TULING_API_KEY,
            'userId': MD5(str(event.dict()['user_id']))
        }
    }

    try:

        # 使用 aiohttp 库发送最终的请求
        async with aiohttp.ClientSession() as sess:
            async with sess.post(url, json=payload) as response:
                if response.status != 200:
                    # 如果 HTTP 响应状态码不是 200，说明调用失败
                    return None

                resp_payload = json.loads(await response.text())
                if resp_payload['results']:
                    for result in resp_payload['results']:
                        if result['resultType'] == 'text':
                            # 返回文本类型的回复
                            return result['values']['text']

    except (aiohttp.ClientError, json.JSONDecodeError, KeyError):
        # 抛出上面任何异常，说明调用失败
        return await tuling.finish(choice(EXPR_DONT_UNDERSTAND))
