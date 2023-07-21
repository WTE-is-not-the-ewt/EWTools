from functions import *
import json, time

config = json.load(open('config.json'))
for day in get_days(config['task']):
    print(day)
    for i, lesson in enumerate(get_lessons({**config['task'], **day})):
        print(lesson)
        if lesson['finished'] or lesson['type'] != '课程讲': continue
        while True:
            send_batch({
                **config['batch'], **lesson,
                'stayTime': 60000,
                'beginTime': (ts := int(time.time() * 1000)) - 60000,
                'timestamp': ts,
                'uuid': f"{scripts.call('randomString')}_{0}"
            })
            time.sleep(60)
            if (status := get_lessons({**config['task'], **day})[i])['finished']: break
            print(status)
