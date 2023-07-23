import requests, pprint
from constants import *

def get(kwargs, print_enable=False):
    '''
    requests 请求封装
    '''
    # 根据参数判断 get 或 post 请求
    if print_enable: pprint.pprint(kwargs)
    method = requests.post if kwargs.get('data') or kwargs.get('json') else requests.get
    return method(**kwargs)

def eget(url, addon_headers=None, upkd_kwargs=None, ajax=True, print_enable=False, **req_kwargs):
    '''
    Easy get，进一步封装
    省略 Headers 配置
    ajax: bool，是否启用 ajax headers
    addon_headers: 添加/修改的 headers
    upkd_kwargs: 需解包参数
    req_kwargs: 关键词参数
    '''
    res = get({
        'url': url,
        'headers': {
            **BASE_HEADERS,
            **(AJAX_HEADERS if ajax else {}),
            **(addon_headers or {})
        },
        **(upkd_kwargs or {}),
        **req_kwargs
    })
    try: print_enable and pprint.pprint(res.json())
    except: pass
    return res
