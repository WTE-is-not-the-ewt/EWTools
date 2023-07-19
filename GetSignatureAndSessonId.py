import requests
import json
import hmac
from hashlib import sha1

#仅供测试
url = "http://bfe.ewt360.com/monitor/hmacSecret?userId={userid}"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

def main():
    endTime = int(input("输入end_time的值,13位时间戳:"))
    stayTime = int(input("输入stay_time的值,单位为ms:"))
    token = str(input("输入token的值,从cookie中获取:"))
    print("请等待...")
    
    req = requests.get(url.format(userid=token.split("-")[0]),headers=header)
    res = json.loads(req.text)

    sessid = res["data"]["sessionId"]
    secret = res["data"]["secret"]
    
    print("x-bfe-session-id="+sessid)

    key = "action=4&duration={duration}&mstid={mstid}&signatureMethod=HMAC-SHA1&signatureVersion=1.0&timestamp={timestamp}&version=2022-08-02"
    hmac_code = hmac.new(secret.encode(), key.format(duration=stayTime,mstid=token,timestamp=endTime).encode(),sha1)
    signature = hmac_code.hexdigest()
    print("signature:"+signature)

if __name__ == "__main__":
    main()