from fastapi import FastAPI

from classes import *
from fullduplex import FullDuplex

api = FastAPI()
fullduplex = FullDuplex()

@fullduplex.serve('init')
async def login(states, conn, account, password):
    states['user'] = user = User()
    user.login(account, password)
    user.load_info()
    return {'code': 0, 'msg': 'init func finished'}

@fullduplex.serve('homeworks')
async def get_and_set(states, conn):
    states['homeworks'] = res = states['user'].get_homeworks()
    return {'code': 0, 'result': res}

@fullduplex.serve('days')
async def get_and_set(states, conn, homeworkID):
    states['days'] = res = states['homeworks'][homeworkID].get_days()
    return {'code': 0, 'result': res}

@fullduplex.serve('tasks')
async def get_and_set(states, conn, dayID):
    states['tasks'] = res = states['days'][dayID].get_tasks()
    return {'code': 0, 'result': res}

@fullduplex.serve('progress')
async def get_and_set(states, conn, lessonID):
    states['tasks'][lessonID].progress()
    return {'code': 0, 'msg': 'executed'}

@fullduplex.serve('test')
async def get_and_set(states, conn, lessonID):
    states['test'] = res = states['tasks'][lessonID].get_test()
    return {'code': 0, 'msg': 'executed', 'result': res}

@fullduplex.serve('eval')
async def get_and_set(states, conn, evaluatable):
    try: res = eval(evaluatable, states)
    except Exception as err: return {'code': 500, 'msg': f'{type(err).__name__}: {err}'}
    return {'code': 0, 'msg': 'executed', 'result': res}

api.websocket('/')(fullduplex.endpoint)
