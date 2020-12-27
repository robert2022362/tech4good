# import required libraries 
import sounddevice as sd 
from scipy.io.wavfile import write 
import wavio as wv 
import subprocess
import os
  
# Sampling frequency 
freq = 44100

def start():

    print('=== 现在开始录音 ===')

    # Recording duration 
    duration = 10
  
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

    os.system("python connect_api.py > out.txt")

    os.system("python print_accuracy.py")