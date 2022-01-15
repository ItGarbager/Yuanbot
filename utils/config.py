from nonebot import get_driver

global_config = get_driver().config.dict()
TULING_API_KEY = global_config['tuling_api_key']
SUPERUSERS = global_config['superusers']
MODEL_ON = global_config['model_on']
