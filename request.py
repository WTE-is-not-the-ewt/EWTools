import requests, re
from settings import *

def get(kwargs):
    '''
    requests 请求封装
    '''
    # 根据参数判断 get 或 post 请求
    method = requests.post if kwargs.get('data', 0) or kwargs.get('json', 0) else requests.get
    return method(**kwargs)

def eget(upkd_kwargs={}, ajax=False, addon_headers={}, **kwargs):
    '''
    Easy get，进一步封装
    省略 Headers 配置
    upkd_kwargs: 需解包参数
    ajax: bool，是否启用 ajax headers
    addon_headers: 添加/修改的 headers
    kwargs: 关键词参数
    '''
    res = get({
        'headers': {
            **base_headers,
            **(page_headers if not ajax else ajax_headers),
            **addon_headers
        },
        **upkd_kwargs,
        **kwargs
    })
    try: print(res.url, res.json())
    except: pass
    return res
