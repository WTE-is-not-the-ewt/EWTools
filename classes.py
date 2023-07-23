from time import time
from constants import *
from functions import *

class User(dict):
    def __init__(self): super().__init__()
    def login(self, account, password):
        self.update(get_token(locals()))
    def load_info(self):
        self.update(get_school(self))
    def get_homeworks(self):
        return {i['homeworkID']: Homework(i, self) for i in get_homeworks(self)}

class Homework(dict):
    def __init__(self, active, user: User):
        super().__init__(active)
        self.user = user
    def get_days(self):
        return {i['day']: Day({**i, **dict_filter(self, ['homeworkID'])}, self.user) for i in get_days({**self.user, **self})}

class Day(dict):
    def __init__(self, active, user: User):
        super().__init__(active)
        self.user = user
    def get_tasks(self):
        return {i[{
            '课程讲': 'lessonID',
            '试卷': 'paperID',
            'FM': 'FMID'
        }[i['type']]]: Lesson(i, self.user) for i in get_tasks({**self.user, **self})}

class Lesson(dict):
    def __init__(self, active, user: User):
        super().__init__(active)
        self.user = user
    def get_test(self): return get_test({**self.user, **self})
    def progress(self, stay_time=1000, speed=60*10):
        send_batch({
            **self.user, **self, **get_secret(self.user),
            'stayTime': stay_time,
            'beginTime': (ts := int(time.time() * 1000)) - stay_time,
            'timestamp': ts,
            'uuid': f"{scripts.call('randomString')}_{0}",
            'speed': speed
        })

class Paper(dict):
    def __init__(self, active, user: User):
        super().__init__(active)
        self.user = user
    def get_paper(self): return get_paper({**self.user, **get_report(**self.user, **self)})
