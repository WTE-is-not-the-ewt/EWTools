from fastapi import FastAPI

from classes import *
from fullduplex import FullDuplex

api = FastAPI()
fullduplex = FullDuplex()

@fullduplex.serve('init')
async def login(states, conn, account, password):
    states['user'] = user = User()
    user.login(account, password)
    await conn.send_json({'hint': 'user has logged in'})
    user.load_info()
    await conn.send_json({'hint': 'user info loaded'})
    return {'code': 0, 'msg': 'init func finished'}

@fullduplex.serve('eval')
async def get_and_set(states, conn, evaluatable):
    try: res = eval(evaluatable, states)
    except Exception as err: return {'code': 500, 'msg': f'{type(err).__name__}: {err}'}
    return {'code': 0, 'msg': 'state set', 'result': res}

@fullduplex.serve('update')
async def get_and_set(states, conn, state_name, evaluatable):
    try: states[state_name] = eval(evaluatable, states)
    except Exception as err: return {'code': 500, 'msg': f'{type(err).__name__}: {err}'}
    return {'code': 0, 'msg': 'state set', 'result': states[state_name]}

@fullduplex.serve('execute')
async def get_and_set(states, conn, evaluatable, kwargs):
    try: res = eval(evaluatable, states)(**kwargs)
    except Exception as err: return {'code': 500, 'msg': f'{type(err).__name__}: {err}'}
    return {'code': 0, 'msg': 'executed', 'result': res}

api.websocket('/')(fullduplex.endpoint)
