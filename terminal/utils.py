# -*- coding: utf-8 -*-

from builtins import Exception, str, bytes

import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import wave
import librosa
import soundfile as sf
import xml.etree.ElementTree as ET

text_dict = {
    '1. 静夜思' : '静夜思\n李白\n床前明月光，\n疑似地上霜。\n举头望明月，\n低头思故乡。',
    '2. 悯农' : '悯农\n李绅\n春种一粒粟，\n秋收万颗子。\n四海无闲田，\n农夫犹饿死。'
}

def connect_api():

    # Convert sampling rate from 44.1khz to 16khz
    x,_ = librosa.load('test_in.wav', sr=16000)
    sf.write('test_out.wav', x, 16000)

    with open('text.txt', 'r') as fin:
        text = fin.read()

    STATUS_FIRST_FRAME = 0  # 第一帧的标识
    STATUS_CONTINUE_FRAME = 1  # 中间帧标识
    STATUS_LAST_FRAME = 2  # 最后一帧的标识

    #  BusinessArgs参数常量
    SUB = "ise"
    ENT = "cn_vip"
    #中文题型：read_syllable（单字朗读，汉语专有）read_word（词语朗读）read_sentence（句子朗读）read_chapter(篇章朗读)
    #英文题型：read_word（词语朗读）read_sentence（句子朗读）read_chapter(篇章朗读)simple_expression（英文情景反应）read_choice（英文选择题）topic（英文自由题）retell（英文复述题）picture_talk（英文看图说话）oral_translation（英文口头翻译）
    CATEGORY = "read_sentence"
    #待评测文本 utf8 编码，需要加utf8bom 头
    TEXT = '\uFEFF'+ text
    #直接从文件读取的方式

    #TEXT = '\uFEFF'+ open("cn_sentence.txt","r",encoding='utf-8').read()

    class Ws_Param(object):
        # 初始化
        def __init__(self, APPID, APIKey, APISecret, AudioFile, Text):
            self.APPID = APPID
            self.APIKey = APIKey
            self.APISecret = APISecret
            self.AudioFile = AudioFile
            self.Text = Text

            # 公共参数(common)
            self.CommonArgs = {"app_id": self.APPID}
            # 业务参数(business)，更多个性化参数可在官网查看
            self.BusinessArgs = {"category": CATEGORY, "sub": SUB, "ent": ENT, "cmd": "ssb", "auf": "audio/L16;rate=16000",
                                 "aue": "raw", "text": self.Text, "ttp_skip": True, "aus": 1}

        # 生成url
        def create_url(self):
            # wws请求对Python版本有要求，py3.7可以正常访问，如果py版本请求wss不通，可以换成ws请求，或者更换py版本
            url = 'ws://ise-api.xfyun.cn/v2/open-ise'
            # 生成RFC1123格式的时间戳
            now = datetime.now()
            date = format_date_time(mktime(now.timetuple()))

            # 拼接字符串
            signature_origin = "host: " + "ise-api.xfyun.cn" + "\n"
            signature_origin += "date: " + date + "\n"
            signature_origin += "GET " + "/v2/open-ise " + "HTTP/1.1"
            # 进行hmac-sha256进行加密
            signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                     digestmod=hashlib.sha256).digest()
            signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

            authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
                self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
            authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
            # 将请求的鉴权参数组合为字典
            v = {
                "authorization": authorization,
                "date": date,
                "host": "ise-api.xfyun.cn"
            }
            # 拼接鉴权参数，生成url
            url = url + '?' + urlencode(v)

            # 此处打印出建立连接时候的url,参考本demo的时候，比对相同参数时生成的url与自己代码生成的url是否一致
            print("date: ", date)
            print("v: ", v)
            print('websocket url :', url)
            return url


    # 收到websocket消息的处理
    def on_message(ws, message):
        try:
            code = json.loads(message)["code"]
            sid = json.loads(message)["sid"]
            if code != 0:
                errMsg = json.loads(message)["message"]
                print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))

            else:
                data = json.loads(message)["data"]
                status = data["status"]
                result = data["data"]
                if (status == 2):
                    xml = base64.b64decode(result)
                    #python在windows上默认用gbk编码，print时需要做编码转换，mac等其他系统自行调整编码
                    
                    print("received data")
                    with open("out.xml", 'w') as fout:
                        fout.write(xml.decode("gbk"))

        except Exception as e:
            print("receive msg,but parse exception:", e)


    # 收到websocket错误的处理
    def on_error(ws, error):
        print("### error:", error)


    # 收到websocket关闭的处理
    def on_close(ws):
        print("### closed ###")


    # 收到websocket连接建立的处理
    def on_open(ws):

        def run(*args):
            frameSize = 1280  # 每一帧的音频大小
            intervel = 0.04  # 发送音频间隔(单位:s)
            status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

            with open(wsParam.AudioFile, "rb") as fp:
                while True:
                    buf = fp.read(frameSize)
                    # 文件结束
                    if not buf:
                        status = STATUS_LAST_FRAME
                    # 第一帧处理
                    # 发送第一帧音频，带business 参数
                    # appid 必须带上，只需第一帧发送
                    if status == STATUS_FIRST_FRAME:
                        d = {"common": wsParam.CommonArgs,
                             "business": wsParam.BusinessArgs,
                             "data": {"status": 0}}
                        d = json.dumps(d)
                        ws.send(d)
                        status = STATUS_CONTINUE_FRAME
                    # 中间帧处理
                    elif status == STATUS_CONTINUE_FRAME:
                        d = {"business": {"cmd": "auw", "aus": 2, "aue": "raw"},
                             "data": {"status": 1, "data": str(base64.b64encode(buf).decode())}}
                        ws.send(json.dumps(d))
                    # 最后一帧处理
                    elif status == STATUS_LAST_FRAME:
                        d = {"business": {"cmd": "auw", "aus": 4, "aue": "raw"},
                             "data": {"status": 2, "data": str(base64.b64encode(buf).decode())}}
                        ws.send(json.dumps(d))
                        time.sleep(1)
                        break
                    # 模拟音频采样间隔
                    time.sleep(intervel)
            ws.close()

        thread.start_new_thread(run, ())


    if __name__ == "__main__":
        # 测试时候在此处正确填写相关信息即可运行
        time1 = datetime.now()
        #APPID、APISecret、APIKey信息在控制台——语音评测了（流式版）——服务接口认证信息处即可获取
        wsParam = Ws_Param(APPID='5fe6f94e', APISecret='2426972b6425b5024eaebc3c34293987',
                           APIKey='6cddc0b3e9bc5425c918dca3d3715925',
                           AudioFile='test_out.wav', Text=TEXT)
        websocket.enableTrace(False)
        wsUrl = wsParam.create_url()
        ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
        ws.on_open = on_open
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        time2 = datetime.now()
        print(time2 - time1)


def audio_recording():

    print()
    print('=== 古诗列表 ===')
    for key in text_dict:
        print(key)

    choice = input('请选择你想朗读的古诗[输入序号]: ')
    while True:
        if choice == '1':
            text = text_dict['1. 静夜思']
            break
        elif choice == '2':
            text = text_dict['2. 悯农']
            break
        else:
            choice = input('你输入的序号并不在列表当中，请重新选择: ')

    with open('text.txt', 'w') as fout:
        fout.write(text)

    print('=== 古诗选择完成 ===')
    print()

    print('==========')
    print(text)
    print('==========')
    print()

    print('=== 设置预估朗读时间 ===')
    print('1. 10s\n2. 20s\n3. 30s')


    # Recording duration 
    duration = input('请选择你阅读古诗需要的时间[1/2/3]: ')
    while duration != '1' and duration != '2' and duration != '3':
        duration = input('请重新选择你需要的朗读时间: ')
    if duration == '1':
        duration = 10
    elif duration == '2':
        duration = 20
    elif duration == '3':
        duration = 30

    print(f'你选择在{duration}s里完成阅读，请做好准备')

    start_decision = input('是否选择开始录音[y/n]: ')

    while start_decision != 'y':
        start_decision = input('请做好准备并输入y开始录音: ')

    if start_decision == 'y':

        print()
        print('=== 现在开始录音 ===')


        # import required libraries 
        import sounddevice as sd 
        from scipy.io.wavfile import write 
        import wavio as wv 
      
        # Sampling frequency 
        freq = 44100
      

      
        # Start recorder with the given values  
        # of duration and sample frequency 
        recording = sd.rec(int(duration * freq),  
                        samplerate=freq, channels=1) 
     

        # Record audio for the given number of seconds 
        sd.wait() 

        # This will convert the NumPy array to an audio 
        # file with the given sampling frequency 
        # write("recording0.wav", freq, recording) 
      
        # Convert the NumPy array to audio file 
        wv.write("test_in.wav", recording, freq, sampwidth=2)


        print('=== 现在结束录音 ===')


def print_accuracy():

    tree = ET.parse('out.xml')
    accuracy = int(float(tree.find("./read_sentence/rec_paper/read_sentence").get("total_score")))


    with open('information.txt', 'r') as fin:
        info = fin.readlines()[0].split(' ')

    name = info[0]

    gender = info[1]
    if gender == '男':
        gender_name = '先生'
    else: gender_name = '女士'

    location = info[2]

    vx = info[3]

    if accuracy > 90:
        say = '非常不错，加油!'
    elif accuracy > 80:
        say = '很优秀，加油!'
    elif accuracy > 70:
        say = '不错，加油!'
    elif accuracy > 60:
        say = '还需要继续努力，加油!'
    else:
        say = '不是很好，请继续加油!'

    print(f'你好，来自{location}的{name}{gender_name}你的语音收入了“种子计划”! \n你的分数是{accuracy}! 满分是100。\n{say}')


def collect_information():

    print("====== 欢迎使用\"种子计划\" ======")
    name = input("请输入你的名字: ")
    gender = input('1. 男    2. 女\n请选择你的性别[1/2]: ')

    while gender != '1' and gender != '2':
        gender = input('请重新选择，输入1或2进行选择: ')

    if gender == '1':
        gender = '男'
    elif gender == '2':
        gender = '女'

    city = input('请输入你的城市: ')
    vx = input('输入你的微信号: ')

    with open('information.txt', 'w') as fout:
        fout.write(str(name)+' '+str(gender)+' '+str(city)+' '+str(vx))


def empty_information():

    with open('information.txt', 'w') as fout:
        fout.truncate()

    with open('out.txt', 'w') as fout:
        fout.truncate()

    with open('text.txt', 'w') as fout:
        fout.truncate()

if __name__ == "__main__":

    print_accuracy()