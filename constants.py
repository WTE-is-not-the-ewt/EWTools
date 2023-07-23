from base64 import b64decode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher

BASE_HEADERS = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Sec-Fetch-Site': 'same-origin',
    'Referer': 'https://teacher.ewt360.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62',
    'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
} # 基础 Headers

AJAX_HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'X-Requested-With': 'XMLHttpRequest'
} # ajax headers

BROSWER_APP_VERSION = BASE_HEADERS['User-Agent'].split('/', 1)[-1]

VERSION = '3.0.7'

LOGIN_URL = 'https://gateway.ewt360.com/api/authcenter/v2/oauth/login/account'
BOUND_INFO_URL = 'https://web.ewt360.com/api/eteacherproduct/studentManage/getJoinedClassesAndExtendedInfo'
HOMEWORK_URL = 'https://gateway.ewt360.com/api/homeworkprod/homework/student/getStudentHomeworkInfo'
SIGN_HMAC_URL = 'http://bfe.ewt360.com/monitor/hmacSecret'
PLAYER_TOKEN_URL = 'https://gateway.ewt360.com/api/homeworkprod/player/getPlayerToken'
RSA_ENCRYPTOR = lambda plain_text, public_key:Cipher.new(RSA.importKey(public_key)).encrypt(bytes(plain_text.encode())).hex()
VIDEO_INFO_URL = 'https://web.ewt360.com/api/videoplayerprod/videoplayer/getExternalVideoInfo'
SIMPLE_AES_RSA_PUBLIC_KEY_B64ENCODED = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC3pDA7GTxOvNbXRGMi9QSIzQEI+EMD1HcUPJSQSFuRkZkWo4VQECuPRg/xVjqwX1yUrHUvGQJsBwTS/6LIcQiSwYsOqf+8TWxGQOJyW46gPPQVzTjNTiUoq435QB0v11lNxvKWBQIZLmacUZ2r1APta7i/MY4Lx9XlZVMZNUdUywIDAQAB'
SIMPLE_AES_RSA_ENCRYPTED_KEY_AND_IV = RSA_ENCRYPTOR('0'*32, b64decode(SIMPLE_AES_RSA_PUBLIC_KEY_B64ENCODED))
SIMPLE_AES_MANI_URL = 'https://playvideo.qcloud.com/getplayinfo/v4/{platformID}/{videoID}'
SIMPLE_AES_M3U8_KEY_URL = 'https://drm.vod2.myqcloud.com/getlicense/v1'
DAY_URL = 'https://gateway.ewt360.com/api/homeworkprod/homework/student/studentHomeworkDistribution'
TASK_URL = 'https://gateway.ewt360.com/api/homeworkprod/homework/student/pageHomeworkTasks'
TEST_URL = 'https://gateway.ewt360.com/api/homeworkprod/player/getPlayerLessonConfig'
PAPER_REPORT_URL = 'https://web.ewt360.com/customerApi/api/studyprod/web/answer/report'
PAPER_ANSWER_URL = 'https://web.ewt360.com/customerApi/api/studyprod/web/answer/webreport'
