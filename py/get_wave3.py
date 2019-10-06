# - coding: utf-8 -
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from scipy import signal
import pyaudio
import wave

import math

freq_std = 440
length = 0.1


if __name__ == '__main__':
    #in_file = "hoge.wav"
    
    #data, rate = sf.read(in_file)
    
    in_code = ""
    in_txt = ""
    

    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 3
    WAVE_OUTPUT_FILENAME = "sample.wav"

    p = pyaudio.PyAudio()
    stream = p.open(
        format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        input = True,
        frames_per_buffer = chunk
    )

    all = []
    for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
        data = stream.read(chunk)
        all.append(data)
        try:
            print(int(i / 50))
            pass
        except ZeroDivisionError as identifier:
            pass

    stream.close()
    p.terminate()
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(all))
    waveFile.close()

    in_file = WAVE_OUTPUT_FILENAME

    data, rate = sf.read(in_file)
    
    in_code = ""
    in_txt = ""
    
    in_sec = len(data) / rate
    print(in_sec)

    i = 0
    while i < int(in_sec/length):

        x = []
        
        for copy_data in range(int(1/length)):
            x.extend(data[int(i*44100*length):int((i+1)*44100*length)])
        #X = fftpack.fft(data[int(i*44100*length):int((i+1)*44100*length)])
        X = fftpack.fft(x)
        freqList = fftpack.fftfreq(44100, d =  1.0 / rate)
        amplitude = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]
        in_freq = []
        
        for j in range(16):
            l_lim = ((freq_std * math.pow(2, (j-1) *(1/12)))+(freq_std * math.pow(2, j *(1/12))))/2
            h_lim = ((freq_std * math.pow(2, (j+1) *(1/12)))+(freq_std * math.pow(2, j *(1/12))))/2
            if (in_freq[0] > l_lim )and(in_freq[0] < h_lim):
                in_code += hex(j)[2:4]
                break
        print(i, in_freq, hex(j)[2:4])

        i += 1

        #描画周り
        #plt.plot(freqList, amplitude, marker=".", linestyle="-", label = "fft plot")
        #plt.axis([0, 2000, 0, 7000])
        #plt.xlabel("frequency [Hz]")
        #plt.ylabel("amplitude")
        
        #plt.show()

    for code in range(int(len(in_code)/2)):
        in_txt += chr(int(in_code[code*2:(code+1)*2], 16))
    print("input : ", in_code, "→", in_txt)
    #print(in_code[code*2:(code+1)*2], chr(int(in_code[code*2:(code+1)*2], 16)))
        
