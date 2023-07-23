from classes import *
import json, time

config = json.load(open('config.json'))

user = User()
user.login(**config)
user.load_info()
for homework in user.get_homeworks():
    print(homework)
    for day in homework.get_days():
        print(day)
        for i, task in enumerate(day.get_tasks()):
            print(task)
            if task['finished'] or task['type'] != '课程讲': continue
            while True:
                task.progress()
                time.sleep(1)
                if (status := day.get_tasks()[i])['finished']: break
                print(status)
