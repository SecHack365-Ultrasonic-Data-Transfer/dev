import pyaudio
import numpy as np
import wave
from datetime import datetime
 
CHUNK = 1024
RATE = 44100
l = 10 ** 7
sound_count = 0
 
data1 = []
data2 = []
 
freqList = np.fft.fftfreq(44100, d = 0.5 / RATE)
 
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,
                channels = 1,
                input_device_index = 0,
                rate = RATE,
                frames_per_buffer = CHUNK,
                input = True,
                output = False)
 
try:
    print('check...',end='')
    while stream.is_active():
        print('.',end='')
        for i in range(0, int(RATE / CHUNK * 1)):
            print('!',end='')
            #print(stream.read(CHUNK))
            d = np.frombuffer(stream.read(CHUNK), dtype='int16')
            #print(d)
            if sound_count == 0:
                
                data1.append(d)
                data2.append(d)
 
            else:
                data1.append(d)
                data2.append(d)
        print('soundの前',sound_count)
        if sound_count >= 1:
            print('soundo後')
            if sound_count % 2 == 1:
                data = np.asarray(data1).flatten()
                fft_data = np.fft.fft(data)
                data1 = []
 
            else:
                data = np.asarray(data2).flatten()
                #print(data)
                fft_data = np.fft.fft(data)
                data2 = []
 
            fft_abs = np.abs(fft_data)
 
            data1000 = fft_abs[np.where((freqList > 5000) & (freqList < 7000))]    #2050Hz付近の周波数成分
            #data2600 = fft_abs[np.where((freqList > 2500) & (freqList < 3000))]    #2600Hz付近の周波数成分
            #print(data2050)
            #print(data1000)
            print(data1000.max())
            if (0.25 * l  < data1000.max()) :    #2050Hz付近と2600Hz付近の強度が一定以上あったとき、インターホンが鳴ったと判断
                print(data1000.max())
                #print(0.5 * l)
                this_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
                file_name = this_time + '.wav'
 
                wf = wave.open(file_name, 'w')
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(RATE)
                wf.writeframes(data)
                wf.close()
 
                print('The bell is ringing! ' + this_time)
                data1 = []
                data2 = []
                sound_count = 0
            else :
                print('uwaaa')
 
        sound_count += 1
 
except KeyboardInterrupt:
    print('keyborad')
    stream.stop_stream()
    stream.close()
    p.terminate()