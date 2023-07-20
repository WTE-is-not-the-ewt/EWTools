from functions import *
import json, time

config = json.load(open('config.json'))
send_batch({
    **config['course'],
    'beginTime': str(int(time.time() * 1000) - 60000),
    'timestamp': int(time.time() * 1000),
    'uuid': f"{scripts.call('randomString')}_{0}"
})
get_m3u8_via_simple_AES(config['m3u8'])
