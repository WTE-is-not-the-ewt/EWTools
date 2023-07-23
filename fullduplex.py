import traceback

from fastapi import WebSocket, WebSocketDisconnect

class FullDuplex:
    def __init__(self, initial_states: dict = None) -> None:
        self.routers = {}
        self.states = initial_states or {}
    def serve(self, servpointer: str):
        def wrapper(func):
            self.add_service(servpointer, func)
        return wrapper
    def add_service(self, servpointer: str, func):
        self.routers[servpointer] = func
    async def endpoint(self, websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                msg = await websocket.receive_json()
                try: await websocket.send_json(await self.routers[msg['servp']](self.states, websocket, **msg.get('params', {})))
                except Exception as err: await websocket.send_json({'code': 500, 'exception': str(err), 'traceback': traceback.format_exc()})
        except WebSocketDisconnect: pass
