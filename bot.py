#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from os import path
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from model.db import LiteDb

# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function


nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

# nonebot.load_builtin_plugins("echo")

# Please DO NOT modify this file unless you know what you are doing!
# As an alternative, you should use command `nb` or modify `pyproject.toml` to load plugins
nonebot.load_from_toml("pyproject.toml")

# Modify some config / config depends on loaded configs
# 获取本地插件开关
MODEL_ON = driver.config.dict().get('model_on')
for model_name in MODEL_ON:
    # os.path.join  os.path.dirname
    # 利用importlib加载插件
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'commands', model_name),
        f'commands.{model_name}'
    )

# 将 litedb 挂载到 driver 上
driver.litedb = LiteDb()
# 打开 bot.db
driver.litedb = LiteDb('bot')
try:
    res = driver.litedb.query('select * from permission')
except:
    # 创建一个权限表
    driver.litedb.create_table('''create table permission(
pid integer primary key autoincrement not null,
group_id int not null,
plugin_name char(50) not null,
switch int default 1 not null
);''')
    res = driver.litedb.query('select * from permission')

if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
