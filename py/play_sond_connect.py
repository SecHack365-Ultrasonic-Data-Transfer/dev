#メモ : これなに?
#文字入れたらasciiコード化、16進化した上で音にして流すよ

#参考 : https://fardog.io/blog/2013/02/16/making-noise-in-python/
#複数音鳴らせれば(和音を作り出せれば)、伝送ミスのチェックと再送要求が楽になる?


#coding:utf-8
import pyaudio
import numpy as np
import wave
from datetime import datetime, timedelta
import platform
import sched
import time
import math
import numpy
import pyaudio
import numpy
from scipy.io import wavfile

import parity_bit

#音声出力関係
#freq_std = 1760
freq_math = {}

#---
freq_std = 440

#文字→音声化のための変換関係
sp_len = 0
sp_in = {}

#chunks = []
import platform
def beep(freq, dur=100):
    """
        ビープ音を鳴らす.
        @param freq 周波数
        @param dur  継続時間（ms）
    """
    if platform.system() == "Windows":
        # Windowsの場合は、winsoundというPython標準ライブラリを使います.
        import winsound
        winsound.Beep(freq, dur)
    else:
        # Macの場合には、Macに標準インストールされたplayコマンドを使います.
        import os
        os.system('play -n synth %s sin %s' % (dur/1000, freq))

#指定周波数でサイン波を生成する
def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)

#16進→周波数(音階テイスト)
def str_to_sound(code):
    out_freq = freq_std * math.pow(2, int(code, 16)*(1/12))
    return out_freq
    
#オーディオ鳴らす
def play_tone(stream, frequency, length=1.0, rate=44100):
    print(float(frequency), length, rate)
    chunks = []
    chunks.append(sine(int(frequency), length, rate))
    chunk = numpy.concatenate(chunks) * 0.25
    stream.write(chunk.astype(numpy.float32).tostring())
    
    return chunk
    
#文字入れたらasciiコード
def txt_to_asciicode(input):
    sp_len = len(input)
    sp_in = list(input)  #input -> 1文字ずつ
    sp_out = ""
    ascii_out = []
    ascii_0x_out = []
    for i in range(sp_len) :
        ascii_out.append(hex(ord(sp_in[i])))
        #sp_out += str(hex(ord(sp_in[i])))[2:4] #ascii化→16進化→文字列化
    #横のパリティビット作る
        #print('正しい',ascii_out[i])
        sp_after_out,sp_0x_out = parity_bit.parity_bit_side(ascii_out[i])
        sp_out += sp_after_out
        ascii_0x_out.append(sp_0x_out)
    #print(ascii_0x_out)
    #縦のパリティビット作る
    sp_after_out,sp_0x_out = parity_bit.parity_bit_height(ascii_0x_out,sp_len)
    sp_out += sp_after_out

    #print('ラスト',sp_out)
    return sp_out

def send(out_txt):
    print(out_txt)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)

    chunks = []
    for i in list(out_txt) :
        print(i, int(i, 16))
        chunks.append(play_tone(stream, str_to_sound(i)))

    chunk = numpy.concatenate(chunks)
    wavfile.write("hoge.wav", 44100, chunk)

    stream.close()
    p.terminate()

if __name__ == '__main__':
    in_txt = input("send message :")
    out_txt = txt_to_asciicode(in_txt)
    
    print(in_txt, "→", out_txt)
    p = pyaudio.PyAudio()
    #connect
    sound_count = 0
    while(True):
        #接続オン鳴らす
        beep(2000,2000)
        #返信確認

        CHUNK = 1024
        RATE = 44100
        l = 10 ** 5


        data1 = []
        data2 = []
        chkNum1 = 0
 
        freqList = np.fft.fftfreq(44100, d = 0.5 / RATE)
        
        stream = p.open(format = pyaudio.paInt16,
                channels = 1,
                input_device_index = 0,
                rate = RATE,
                frames_per_buffer = CHUNK,
                input = True,
                output = False)
 
        try:
            print('check...',end='')
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
                            print('接続完了')
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

                    print('The bell is ringing! ' + this_time)
                    data1 = []
                    data2 = []
                    #sound_count = 0
                    break
                else :
                    print('uwaaa')
                sound_count += 1
            print('return') 
            sound_count += 1
            print(sound_count)
            
        except KeyboardInterrupt:   
                    print('keyborad')
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
    #同期
    now = datetime.now()
    comp = datetime(now.year, now.month, now.day, now.hour, now.minute+1,0)
    print(now)
    print(comp)
    diff = comp - now
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(diff.seconds, 1, send,(out_txt,) )
    scheduler.run()