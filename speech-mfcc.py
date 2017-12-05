from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import pyaudio
import wave
import time

import scipy.io.wavfile as wav
import scipy


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "file.wav"


x=3
while x>0:
    time.sleep(1)
    print("Recording will start in: ",x)
    x-=1
time.sleep(1)
audio = pyaudio.PyAudio()
# start Recordingpython -m pip install pyaudio
stream = audio.open(format=FORMAT, channels=CHANNELS,rate=RATE, input=True,frames_per_buffer=CHUNK)
print ("recording...")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print ("finished recording")

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

(rate,sig) = wav.read("file.wav")
mfcc_feat1 = mfcc(sig,rate)
d_mfcc_feat = delta(mfcc_feat1, 2)

(rate,sig) = wav.read("file1.wav")
mfcc_feat2 = mfcc(sig,rate)
d_mfcc_feat = delta(mfcc_feat2, 2)

score = 0.0
correct_Counter=0
incorrect_Counter=0
sum1=[]
sum2=[]

for i in range(13):
        sum11 = 0
        sum22 = 0
        for j in range(32):
            sum11+=mfcc_feat1[j][i]
            sum22+=mfcc_feat2[j][i]
        sum1.append(sum11/33)
        sum2.append(sum22/33)

print(sum1,"\n",sum2)

for i in range(13):
        x = (sum1[i])
        y = (sum2[i])

        score = x - y
        if score < 10 and score > -10:

            score = 0
            correct_Counter +=1
        else:

            incorrect_Counter +=1

print("correct", correct_Counter)
print("incorrect", incorrect_Counter)
percent=correct_Counter/(correct_Counter+incorrect_Counter)*100
round(percent)
print("score: ", round(percent),"%")
if(percent>=80):
    print("Access!! ")
if(percent<80):
    print("Access denied")