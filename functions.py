import execjs
from os import environ
import json
import hmac
import time
from urllib.parse import urlencode
from hashlib import sha1
from constants import *
from request import eget

scripts = execjs.compile(open('script.js', encoding='utf-8').read()) # 以 node 为环境编译爬虫所需 JavaScript 代码
# 为转换 JavaScript Object 为 dict，需要 JavaScript 环境
environ["EXECJS_RUNTIME"] = "JScript" # JavaScript Object 在 node 环境会报编码错误，转用 Windows 自带 JScript 环境
script_eval = execjs.eval # 转换函数别名

def get_signature(active, inactive=None, ineffective=None):
    inactive = {
        'signMethod': 'HMAC-SHA1',
        'signVer': '1.0',
        'signVerDate': '2022-08-02',
        **(inactive or {})
    }
    req = eget(SIGN_HMAC_URL, {
        'Token': active['token']
    }, params={
        'userId': active['userID']
    })
    res = json.loads(req.text)
    active.setdefault('sessionID', res["data"]["sessionId"])
    secret = res["data"]["secret"]
    key = urlencode({
        'action': 2,
        'duration': active['stayTime'],
        'mstid': active['token'],
        'signatureMethod': inactive['signMethod'], 
        'signatureVersion': inactive['signVer'],
        'timestamp': active['timestamp'],
        'version': inactive['signVerDate'] 
    })
    hmac_code = hmac.new(secret.encode(), key.encode(), sha1)
    return hmac_code.hexdigest()

def get_packages(active, inactive=None, ineffective=None):
    inactive = {
        'videoType': 1,
        'playStatusEnum': 1,
        **(inactive or {})
    }
    ineffective = {
        'unitTime': 60000,
        'unitTimeIndex': 1,
        "totalUnitTime": 15,
        **(ineffective or {})
    }
    return {
        "CommonPackage": {
            "userid": active['userID'],
            "os": 'Windows',
            "resolution": '1920*1080',
            "mstid": active['token'],
            "browser": 'Edge',
            "browser_ver": '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82', # navigator.appVersion
            "playerType": 1,
            "sdkVersion": VERSION,
            "videoBizCode": "1013"
        },
        "EventPackage": [{
            "action": 2,
            "lesson_id": active['lessonID'],
            "course_id": active['courseID'],
            "stay_time": active['stayTime'],
            "begin_time": active['beginTime'],
            "report_time": active['timestamp'],
            "point_time": ineffective['unitTime'],
            "point_num": ineffective['totalUnitTime'],
            "point_time_id": ineffective['unitTimeIndex'],
            "status": inactive['playStatusEnum'],
            "video_type": inactive['videoType'],
            "speed": 1,
            "fallback": 0,
            "quality": '高清',
            "uuid": active['uuid']
        }]
    }

def send_batch(active, inactive=None, ineffective=None):
    packages = get_packages(active, inactive, ineffective)
    signature = get_signature(active, inactive, ineffective)
    eget('https://bfe.ewt360.com/monitor/web/collect/batch', {
        'Token': active['token'],
        'X-Bfe-Session-Id': active['sessionID']
    }, params={
        'TrVideoBizCode': 1013,
        'TrFallback': 0,
        'TrUserId': active['userID'],
        'TrLessonId': active['lessonID'],
        'TrUuId': active['uuid'],
        'sdkVersion': VERSION,
        '_': active['timestamp']
    }, json={
        **packages,
        "sn": "ewt_web_video_detail",
        "signature": signature,
        '_': active['timestamp']
    })

def get_m3u8_via_simple_AES(required):
    player_token = eget(PLAYER_TOKEN_URL, json={
        'lessonId': required['lessonID'],
        'schoolId': required['schoolID'],
        'type': 1
    }, headers={
        'Token': required['token']
    }).json()['data']
    video_info = eget(VIDEO_INFO_URL, params={
        'videoBizCode': 1013,
        'lessonId': required['lessonID'],
        'videoToken': player_token,
        'sdkVersion': '3.0.7',
        '_': int(time.time() * 1000)
    }, headers={
        'Token': required['token']
    }).json()
    mani_info = eget(SIMPLE_AES_MANI_URL.format(
        platformID=video_info['data']['videoList'][1]['platFormUuId'],
        videoID=video_info['data']['videoList'][1]['videoId']
    ), params={
        'psign': video_info['data']['videoList'][1]['definitionList'][0]['psign'],
        'cipheredOverlayKey': SIMPLE_AES_RSA_ENCRYPTED_KEY_AND_IV,
        'cipheredOverlayIv': SIMPLE_AES_RSA_ENCRYPTED_KEY_AND_IV,
        'keyId': 1
    }).json()
    mani_url = mani_info['media']['streamingInfo']['drmOutput'][0]['url']
    mani_token = mani_info['media']['streamingInfo']['drmToken']
    origin_filename = mani_url.split('/')[-1]
    correct_filename = f'voddrm.token.{mani_token}.{origin_filename}'
    mani_url = mani_url.replace(origin_filename, correct_filename)
    '''
    key_content = eget(SIMPLE_AES_M3U8_KEY_URL, params={
        'drmType': 'SimpleAES',
        'token': mani_token
    }).content
    '''
    return mani_url
