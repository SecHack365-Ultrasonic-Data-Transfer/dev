import pyaudio
import numpy as np
import wave
from datetime import datetime, timedelta
import platform
import sched
import time
import get_wave4

CHUNK = 1024
RATE = 44100
l = 10 ** 5
sound_count = 0
 
data1 = []
data2 = []
chkNum1 = 0
 
freqList = np.fft.fftfreq(44100, d = 0.5 / RATE)
print(freqList)
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
        for i in range(0, int(RATE / CHUNK * 1)):
            #print(stream.read(CHUNK))
            d = np.frombuffer(stream.read(CHUNK), dtype='int16')
            #print(d)
            if sound_count == 0:
                
                data1.append(d)
                data2.append(d)
 
            else:
                data1.append(d)
                data2.append(d)
        if sound_count >= 1:
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
 
            data1000 = fft_abs[np.where((freqList > 1500) & (freqList < 2500))]    #2050Hz付近の周波数成分
            #data2600 = fft_abs[np.where((freqList > 2500) & (freqList < 3000))]    #2600Hz付近の周波数成分
            #print(data2050)
            print(len(data1000))
            print('data:',data1000.max())
            if (0.25 * l  < data1000.max()) :    #2050Hz付近と2600Hz付近の強度が一定以上あったとき、インターホンが鳴ったと判断
                print(data1000.max())
                #print(0.5 * l)
                if(chkNum1 == 0):
                    chkNum1 = sound_count
                    print(chkNum1)
                elif(chkNum1 != 0):
                    if(chkNum1+1 == sound_count):
                        print('接続要求')
                    else:
                        chkNum1 = 0
                    
                this_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
                #file_name = this_time + '.wav'
 
                #wf = wave.open(file_name, 'w')
                #wf.setnchannels(1)
                #wf.setsampwidth(2)
                #wf.setframerate(RATE)
                #wf.writeframes(data)
                #wf.close()
 
                print('connecting... ' + this_time)
                data1 = []
                data2 = []
                #sound_count = 0
                break
            else :
                print('uwaaa')
 
        sound_count += 1
    print('end') 
    #ここから返信ですぅ


    freq = 2000
    dur = 2000
    if platform.system() == "Windows":
        # Windowsの場合は、winsoundというPython標準ライブラリを使います.
        import winsound
        winsound.Beep(freq, dur)
    else:
        # Macの場合には、Macに標準インストールされたplayコマンドを使います.
        import os
        os.system('play -n synth %s sin %s' % (dur/1000, freq))
    #同期
    now = datetime.now()
    comp = datetime(now.year, now.month, now.day, now.hour, now.minute+1,0)
    print(now)
    print(comp)
    diff = comp - now
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(diff.seconds, 1, get_wave4.get_wave )
    #スタート
    scheduler.run()

except KeyboardInterrupt:   
    print('keyborad')
    stream.stop_stream()
    stream.close()
    p.terminate()