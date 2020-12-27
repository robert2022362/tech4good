import wave
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import librosa
import soundfile as sf
import scipy

np.set_printoptions(threshold=sys.maxsize)

def wav2data(wf):
    buf = wf.readframes(wf.getnframes())
    data = np.frombuffer(buf, dtype="int16")
    return data

def downsampling(conversion_rate,data,fs):
    """
    执行抽样。
    功率，可变速率，数据和采样频率。
    返回未采样后的数据和采样频率的数
    """
    # 确定要稀疏的样本数量
    decimationSampleNum = conversion_rate-1

    # 准备FIR滤波器
    nyqF = fs/2.0             # 转换后的奈奎斯特频率
    cF = (fs/conversion_rate/2.0-500.)/nyqF     # 设置截止频率（设置为略低于转换前的奈奎斯特频率）
    taps = 511                                  # 滤波系数（必须为奇数）
    b = scipy.signal.firwin(taps, cF)           # 准备LPF

    #过滤
    # data = scipy.signal.lfilter(b,1,data)

    #细化工艺
    downData = []
    for i in range(0,len(data),decimationSampleNum+1):
        downData.append(data[i])

    return np.array(downData)


def voice_trimming(data):    
    data = frombuffer(data, dtype="int16")
    print(data)
    #print(data.ndim)

    threshold = 1000
    
    #Return index of audio samples that resemble voice portion of data
    voices = np.squeeze(np.where(np.absolute(data)>threshold))
    print(voices)
    start_index = voices[0]
    end_index = voices[len(voices) - 1]
    trimmed_data = data[start_index:end_index+1]
    return trimmed_data


def data_normalize(trimmed_data, axis=None):
    min = trimmed_data.min(axis=axis, keepdims=True)
    max = trimmed_data.max(axis=axis, keepdims=True)
    norm_data = (trimmed_data-min)/(max-min)
    return norm_data
    
    
def zscore(trimmed_data, axis = None):
    xmean = trimmed_data.mean(axis=axis, keepdims=True)
    xstd  = np.std(trimmed_data, axis=axis, keepdims=True)
    zscore = (trimmed_data-xmean)/xstd
    return zscore
    

def calc_pecgram(wf, voice_type): 
    data = wav2data(wf)
    trimmed_data = voice_trimming(data)
    downsampled_data = downsampling(2,trimmed_data,48000)
    zscore_data = zscore(downsampled_data, axis = None)
        

    # FFT样本数
    N = 8192
    
    # FFT中使用的嗡嗡声窗口
    hammingWindow = np.hamming(N)

    # 绘制频谱图
    pxx, freqs, bins, im = specgram(zscore_data, NFFT=N, Fs=len(zscore_data), noverlap=0, window=hammingWindow)
    
    return (pxx, freqs, bins, im)

def append_zero(vec):
    max_len = 4
    if len(vec) != max_len:
        append = np.zeros(max_len - len(vec))
        extended_vec = np.append(vec, append)
    else: extended_vec = vec
    return extended_vec

def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# voice1
#第一个声音
wf_voice1 = wave.open("barbara1.wav" , "r" )
specgram_voice1 = calc_pecgram(wf_voice1, "person")
matcrix_voice1 = specgram_voice1[0]

vec_1 = np.amax(matcrix_voice1, axis=0)
ex_1 = append_zero(vec_1)

#第二个声音
wf_f = wave.open("barbara2.wav" , "r" )
specgram_f = calc_pecgram(wf_f, "pokemon")
matcrix_f = specgram_f[0]

vec_f = np.amax(matcrix_f, axis=0)
ex_f = append_zero(vec_f)

print("两个声音的相似度：", cos_sim(ex_1, ex_f))