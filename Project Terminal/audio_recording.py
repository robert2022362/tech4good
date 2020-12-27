text_dict = {
    '1. 静夜思' : '静夜思\n李白\n床前明月光，\n疑似地上霜。\n举头望明月，\n低头思故乡。',
    '2. 悯农' : '悯农\n李绅\n春种一粒粟，\n秋收万颗子。\n四海无闲田，\n农夫犹饿死。'
}

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

