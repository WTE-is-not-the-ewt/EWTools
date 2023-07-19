base_headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62',
    'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
} # 基础 Headers

ajax_headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'X-Requested-With': 'XMLHttpRequest'
} # ajax headers

page_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Upgrade-Insecure-Requests': '1'
} # HTML 页面 headers

eduxl_domains = {
    '选择学校': None,
    **eval(open('colleges.json', encoding='utf-8').read()) # 从 colleges.json (python dict 语法) 获取学校信息
}
LOGIN_URL = 'https://{}/Index/SignIn'
HOME_URL = 'https://{}/MyOnlineCourseNew/OnlineLearningNew/OnlineLearningNewIndex'
LEARN_URL = 'https://{}/MyOnlineCourseNew/OnlineLearningNew/GetCourseUrl'
PROGRESS_URL = 'https://whcj.edu-edu.com/cws/home/couresware/runtime/sco/records?_={now}&__ajax=true'
STATUS_URL = 'https://whcj.edu-edu.com/cws/home/couresware/runtime/node/record/init?__ajax=true&_node={scoid}&_={now}'
VIEWED_URL = 'https://whcj.edu-edu.com/cws/home/couresware/runtime/record/save'
EXAM_URL = 'https://{}/MyOnlineCourseNew/OnlineLearningNew/GetExamUrl'
RECORD_URL = 'https://whcj.edu-edu.com/exam-admin/home/my/exam/view/result/{examid}'
PAPER_RESTART_URL = 'https://whcj.edu-edu.com/exam-admin/home/my/exam/restart/{paperid}'
PAPER_REVIEW_URL = 'https://whcj.edu-edu.com/exam-admin/home/my/exam/review/{paperid}'
ANSWERS_URL = 'https://{subdomain}.edu-edu.com/exam/student/exam/answer/{paperid}'
ANSWER_URL = 'https://{subdomain}.edu-edu.com/exam/student/exam/myanswer/newSave/{paperid}/{quesid}'

CACHE_PATH = 'accounts'
DATA_PATH = 'data.db'

config = {
    'use_proxy': False
}
