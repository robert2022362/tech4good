import base64
import hashlib
import json
import time

import requests


def main():
    x_appid = '5fe6f94e'
    api_key = '6cddc0b3e9bc5425c918dca3d3715925'
    curTime = str(int(time.time()))
    url = 'http://api.xfyun.cn/v1/service/v1/ise'
    text = '早上好'
    AUDIO_PATH = 'test1.wav'
    with open(AUDIO_PATH, 'rb') as f:
        file_content = f.read()
    base64_audio = base64.b64encode(file_content)
    body = {'audio': base64_audio, 'text': text}
    param = json.dumps({"aue": "raw", "result_level": "entirety", "language": "zh_cn", "category": "read_sentence"})
    paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
    m2 = hashlib.md5()
    m2.update((api_key + curTime + paramBase64).encode('utf-8'))
    checkSum = m2.hexdigest()
    x_header = {
                'X-Appid': x_appid,
                'X-CurTime': curTime,
                'X-Param': paramBase64,
                'X-CheckSum': checkSum,
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                }
    req = requests.post(url, data=body, headers=x_header)
    result = req.content.decode('utf-8')
    print(result)
    return


if __name__ == '__main__':
    main()