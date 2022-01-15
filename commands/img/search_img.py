import json
import aiohttp
from nonebot.matcher import Matcher
from nonebot.rule import to_me
from nonebot import on_regex
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Message, escape, Event

from utils.UnittoNum import chinese_to_arabic
from utils.wrapper import check_switch, try_except

search_img = on_regex(r'来(.+)[张張](.+)', rule=to_me(), permission=SUPERUSER)  # permission 匹配超级用户
search_img.__doc__ = '''搜图功能
    使用方法: 来?张?'''


@search_img.handle()
@try_except
@check_switch
async def _(matcher: Matcher, event: Event):
    state = matcher.state
    # 设定一个阈值
    max_page = 5
    num, keyword = state["_matched_groups"]

    if num.isdigit():
        num = int(num)
    else:
        try:
            num = chinese_to_arabic(num)
        except:
            raise Exception('请不要捣乱，发一个整数好么')

    if num > max_page:
        raise Exception(f'上限只可以发{max_page}张')

    img_list = await get_images(keyword=keyword, num=num)
    if not img_list:
        raise Exception('搜不到该图片')
    await search_img.send(Message('图片搜索如下:\n' + '\n'.join(img_list)))


async def get_images(keyword, num):
    headers = {
        'Cookie': 'BDqhfp=%E5%88%BB%E6%99%B4%E5%A4%B4%E5%83%8F%26%260000-10-1undefined%26%260%26%261; BIDUPSID=3E607554DF57D43822D4048A00500518; PSTM=1633622356; __yjs_duid=1_dd02bc04ddfad61400f62e9c93f8082e1633706351349; BAIDUID=3E607554DF57D438A8BF45C697F55A5A:SL=0:NR=10:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=35105_35631_34967_35457_34584_35491_35584_35246_35688_35685_35315_26350_35474_35514_35745; cleanHistoryStatus=0; delPer=0; PSINO=2; BAIDUID_BFESS=3E607554DF57D438A8BF45C697F55A5A:SL=0:NR=10:FG=1; BCLID=11756338712150052526; BDSFRCVID=ZjkOJexroG04u15HYZWhuzedtkw3v3rTDYrEOwXPsp3LGJLVgg9bEG0PtOVzGoFbI1odogKK0mOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tRAOoC85fIvjDb7GbKTD-tFO5eT22-us3RTA2hcH0KLKbJP6b-OkyhFl0trthtQbbg_H--3dBMb1MRjv5xjI3xuRLGjHBb5QLIT00p5TtUJs8DnTDMRhqqJXqfbyKMnitIj9-pnKHlQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKuD6AKDjb-DGLs5JtXKD600PK8Kb7VbP3kLUnkbJkXhPtjtnLDJmbkhfnKb4cqe-bc5Tb-DnD7QbrH0xRfyNReQIO13hcdSR3Tet5pQT8r5-nphfby3DrAoR7eab3vOIJzXpO1jxPzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-FtqjDOtJCfVC_hfbo5KRopMtOhq4tehH4Lbjv9WDTOQJ7TtIbhhD5SWqC2MbLhbfOJab-ebJ7H-pbw-q5cfUnMKn05XM-pXbjMK5ca3mkjbPbvQtcnDpQPyjQob-4syP4j2xRnWnciKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJzJCFKbK_ljTuKDjPVKgTa54cbb4o2WbCQMtch8pcN2b5oQTO35HLtBpcztnrtXJ5ebnvbhPLRKlOUWJDkXpJvQnJjt2JxaqRC5b0BHl5jDh3MXpKhQUnl5fFDaKny0hvctn6cShPCyUjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDGAHJ6-8tJCs3t88KJjEe-Kk-PnVepIqMPnZKRvHa2kj_PKhJlnZox3d5J6qbb0f5NbqJbjn3N5HKl75yUJ5qKOsQU6d34-sef5405OTbgOpXq3O3JozhJ7ghPJvyT8DXnO7tfnlXbrtXp7_2J0WStbKy4oTjxL1Db3JKjvMtgDtVJO-KKCaMDt4eM5; BCLID_BFESS=11756338712150052526; BDSFRCVID_BFESS=ZjkOJexroG04u15HYZWhuzedtkw3v3rTDYrEOwXPsp3LGJLVgg9bEG0PtOVzGoFbI1odogKK0mOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tRAOoC85fIvjDb7GbKTD-tFO5eT22-us3RTA2hcH0KLKbJP6b-OkyhFl0trthtQbbg_H--3dBMb1MRjv5xjI3xuRLGjHBb5QLIT00p5TtUJs8DnTDMRhqqJXqfbyKMnitIj9-pnKHlQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKuD6AKDjb-DGLs5JtXKD600PK8Kb7VbP3kLUnkbJkXhPtjtnLDJmbkhfnKb4cqe-bc5Tb-DnD7QbrH0xRfyNReQIO13hcdSR3Tet5pQT8r5-nphfby3DrAoR7eab3vOIJzXpO1jxPzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-FtqjDOtJCfVC_hfbo5KRopMtOhq4tehH4Lbjv9WDTOQJ7TtIbhhD5SWqC2MbLhbfOJab-ebJ7H-pbw-q5cfUnMKn05XM-pXbjMK5ca3mkjbPbvQtcnDpQPyjQob-4syP4j2xRnWnciKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJzJCFKbK_ljTuKDjPVKgTa54cbb4o2WbCQMtch8pcN2b5oQTO35HLtBpcztnrtXJ5ebnvbhPLRKlOUWJDkXpJvQnJjt2JxaqRC5b0BHl5jDh3MXpKhQUnl5fFDaKny0hvctn6cShPCyUjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDGAHJ6-8tJCs3t88KJjEe-Kk-PnVepIqMPnZKRvHa2kj_PKhJlnZox3d5J6qbb0f5NbqJbjn3N5HKl75yUJ5qKOsQU6d34-sef5405OTbgOpXq3O3JozhJ7ghPJvyT8DXnO7tfnlXbrtXp7_2J0WStbKy4oTjxL1Db3JKjvMtgDtVJO-KKCaMDt4eM5; BA_HECTOR=2g2g0kag2g040424rt1gttec50r; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; userFrom=www.baidu.com; firstShowTip=1; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; BDRCVFR[Txj84yDU4nc]=mk3SLVN4HKm; indexPageSugList=%5B%22%E5%88%BB%E6%99%B4%E5%A4%B4%E5%83%8F%22%2C%22%E5%88%BB%E6%99%B4%22%5D; ab_sr=1.0.1_NzU4NDBiMzE5YTU2YTNlMmMzYzg4MTJlMjY4MWQzNjZhZWQyNWJmMzg2MzViMjdlYzI3M2ZmMTFiNmI0YzA2ZTYyMWJkMTlkNDhiZDc1OTdhZjRjYWMwYzJkNTk2NjAxOTc5ZTFmMzQwZTU1NzRhNzc5ZjIwNWNkN2IxOTE0YjA4OTAwNTUxMjc2NjZmNjkxNTZlMjE2YmMyN2JlNGYwYQ==',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

    url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=9418852174407235922&ipn=rj&ct=201326592&is=&fp=result&fr=&word=%s&queryWord=%s&cl=2&lm=-1&ie=utf-8&oe=utf-8' \
          '&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn=0&rn=%s&gsm=1e&1642189051915=' % (keyword, keyword, num)
    # 使用 aiohttp 库发送最终的请求
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url, headers=headers) as response:
            if response.status != 200:
                # 如果 HTTP 响应状态码不是 200，说明调用失败
                return None

            data = json.loads(await response.text())
            msg_list = []  # 初始化的图片列表
            if data:
                data = data.get('data')
                for img in data:
                    url = img.get('hoverURL')
                    if url:
                        url = f'[CQ:image,file={escape(url)}]'
                        msg_list.append(url)
                return msg_list
