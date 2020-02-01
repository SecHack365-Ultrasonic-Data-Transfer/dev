import pyaudio
import numpy as np
import wave
from datetime import datetime, timedelta
import platform
import sched
import time

def sync():
    try:
        CHUNK = 1024
        RATE = 44100
        l = 10 ** 5
        sound_count = 0
        data1 = []
        chkNum1 = 0
    
        freqList = np.fft.fftfreq(44100, d = 0.5 / RATE)
        p = pyaudio.PyAudio()
        stream = p.open(format = pyaudio.paInt16,
                        channels = 1,
                        input_device_index = 0,
                        rate = RATE,
                        frames_per_buffer = CHUNK,
                        input = True,
                        output = False)
        print('check...',end='')

        while stream.is_active():#マイク起動
            print('.',end='')
            for i in range(0, int(RATE / CHUNK * 1)):
                d = np.frombuffer(stream.read(CHUNK), dtype='int16')
                data1.append(d)
            if sound_count >= 1:
                data = np.asarray(data1).flatten()
                fft_data = np.fft.fft(data)
                data1 = [] 
                fft_abs = np.abs(fft_data)
    
                data1000 = fft_abs[np.where((freqList > 1500) & (freqList < 2500))]    #2000Hz付近の周波数成分

                print(len(data1000))
                print('data:',data1000.max())
                if (0.25 * l  < data1000.max()) :
                    if(chkNum1 == 0): 
                        chkNum1 = sound_count
                        print(chkNum1)
                    elif(chkNum1 != 0):#検討中。これ逆じゃね？？？
                        if(chkNum1+1 == sound_count):
                            print('接続要求')
                        else:
                            chkNum1 = 0
                    this_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
                    print('conencting...: ' + this_time)
                    break
            sound_count += 1

        print('end') 
        return this_time

    except KeyboardInterrupt:   
        print('keyborad')
        stream.stop_stream()
        stream.close()
        p.terminate()