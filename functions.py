import execjs
from os import environ
import hmac
import time
from urllib.parse import urlencode, urlparse, parse_qs
from hashlib import sha1
from constants import *
from request import eget
from Crypto.Cipher import AES
from binascii import b2a_hex

scripts = execjs.compile(open('script.js', encoding='utf-8').read()) # 以 node 为环境编译爬虫所需 JavaScript 代码
# 为转换 JavaScript Object 为 dict，需要 JavaScript 环境
environ["EXECJS_RUNTIME"] = "JScript" # JavaScript Object 在 node 环境会报编码错误，转用 Windows 自带 JScript 环境
script_eval = execjs.eval # 转换函数别名
dict_reform = lambda d,r:{r[k]:d[k] for k in d if k in r}
dict_filter = lambda d,l:{k:d[k] for k in d if k in l}
urlquery = lambda x:parse_qs(urlparse(x).query)

def compute_password(active):
    password = active['password'].encode("utf-8")
    cryptor = AES.new(b"20171109124536982017110912453698", AES.MODE_CBC, iv=b"2017110912453698")
    pad = 16 - len(password) % 16
    password += (chr(pad) * pad).encode("utf-8")
    return b2a_hex(cryptor.encrypt(password)).decode("utf-8").upper()

def get_token(active):
    return dict_reform(eget(LOGIN_URL, json={
        "platform": 1,
        "userName": active['account'],
        "password": compute_password(active),
        "autoLogin": True
    }).json()['data'], {
        'userId': 'userID',
        'token': 'token'
    })

def get_school(active):
    return dict_reform(eget(BOUND_INFO_URL, {
        'Token': active['token']
    }).json()['data'], {
        'schoolId': 'schoolID',
        'schoolName': 'schoolName'
    })

def get_homeworks(active):
    return list(map(lambda x:dict_reform(x, {
        'homeworkId': 'homeworkID',
        'title': 'title',
        'teacherName': 'releaser'
    }), eget(HOMEWORK_URL, {
        'Token': active['token']
    }, json={
        "subject": None,
        "type": None,
        "status": 2,
        "pageIndex": 1,
        "pageSize": 20,
        "schoolId": active['schoolID']
    }).json()['data']))

def get_secret(active):
    return dict_reform(eget(SIGN_HMAC_URL, params={
        'userId': active['userID']
    }).json()['data'], {
        'sessionId': 'sessionID',
        'secret': 'secret'
    })

def compute_signature(active):
    inactive = {
        'signMethod': 'HMAC-SHA1',
        'signVer': '1.0',
        'signVerDate': '2022-08-02',
    }
    return hmac.new(active['secret'].encode(), urlencode({
        'action': 2,
        'duration': active['stayTime'],
        'mstid': active['token'],
        'signatureMethod': inactive['signMethod'], 
        'signatureVersion': inactive['signVer'],
        'timestamp': active['timestamp'],
        'version': inactive['signVerDate'] 
    }).encode(), sha1).hexdigest()

def send_batch(active):
    inactive = {
        'videoType': 1,
        'playStatusEnum': 1
    }
    ineffective = {
        'unitTime': 60000,
        'unitTimeIndex': 1,
        "totalUnitTime": 15
    }
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
        "CommonPackage": {
            "userid": active['userID'],
            "os": 'Windows',
            "resolution": '1920*1080',
            "mstid": active['token'],
            "browser": 'Edge',
            "browser_ver": BROSWER_APP_VERSION,
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
            "speed": active['speed'],
            "fallback": 0,
            "quality": '高清',
            "uuid": active['uuid']
        }],
        "sn": "ewt_web_video_detail",
        "signature": compute_signature(active),
        '_': active['timestamp']
    })

def get_days(active):
    return list(map(lambda x:{
        'day': x['day'],
        'dayID': x['dayId']
    }, eget(DAY_URL, {
        'token': active['token']
    }, json={
        "homeworkIds": [
            active['homeworkID']
        ],
        "sceneId": 0,
        "taskDistributionTypeEnum": 1,
        "schoolId": active['schoolID']
    }).json()['data']['days']))

def get_tasks(active):
    return list(map(lambda x:{
        **dict_reform(urlquery(urlparse(x['contentUrl']).fragment), {
            'courseId': 'courseID',
            'lessonId': 'lessonID'
        }),
        'progress': x['ratio'],
        'finished': x['finished'],
        'type': x['contentTypeName']
    }, eget(TASK_URL, {
        'token': active['token']
    }, json={
        "homeworkIds": [
            active['homeworkID']
        ],
        "sceneId": 0,
        "pageIndex": 1,
        "pageSize": 30,
        "day": active['day'],
        "dayId": active['dayID'],
        "schoolId": active['schoolID']
    }).json()['data']['data']))

def get_test(active):
    return dict_reform(eget(TEST_URL, {
        'Token': active['token']
    }, json={
        'schoolId': active['schoolID'],
        'homeworkId': active['homeworkID'],
        'lessonIdList': [
            active['lessonID']
        ]
    }).json()['data'][0]['studyTest'], {
        'paperId': 'paperID'
    })

def get_report(active):
    dict_reform(eget(PAPER_REPORT_URL, {
        'Token': active['token']
    }, params={
        'paperId': active['paperID'],
        'platform': 1,
        'isRepeat': 1,
        'bizCode': '204'
    }).json()['data'], {
        'finish': 'finished',
        'reportId': 'reportID'
    })

def get_paper(active):
    question_handler = lambda x:{**(obj := dict_reform(x, {
        'rightAnswer': 'answer',
        'questionContent': 'content',
        'childQuestions': 'children',
        'analyse': 'explain'
    })), 'children': list(map(question_handler, obj['children']))}
    return list(map(question_handler, eget(PAPER_ANSWER_URL, {
        'Token': active['token']
    }, params={
        'reportId': active['reportID'],
        'bizCode': '204'
    }).json()['data']['questions']))

def get_m3u8_via_simple_AES(active):
    player_token = eget(PLAYER_TOKEN_URL, json={
        'lessonId': active['lessonID'],
        'schoolId': active['schoolID'],
        'type': 1
    }, headers={
        'Token': active['token']
    }).json()['data']
    video_info = eget(VIDEO_INFO_URL, params={
        'videoBizCode': 1013,
        'lessonId': active['lessonID'],
        'videoToken': player_token,
        'sdkVersion': VERSION,
        '_': int(time.time() * 1000)
    }, headers={
        'Token': active['token']
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
