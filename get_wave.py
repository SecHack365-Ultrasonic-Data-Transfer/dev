# - coding: utf-8 -
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from scipy import signal

import math

freq_std = 440


if __name__ == '__main__':
    in_file = "hoge.wav"
    
    data, rate = sf.read(in_file)
    
    in_code = ""
    in_txt = ""
    
    in_sec = len(data) / rate
    for i in range(int(in_sec)):
        X = fftpack.fft(data[i*44100:(i+1)*44100])
        freqList = fftpack.fftfreq(44100, d=1.0/ rate)
        
        amplitude = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]
        in_freq = amplitude.index(max(amplitude))  #1番大きい振幅を拾ってるだけ(雑音出たら、たぶん上手くいかない)
        
        for j in range(16):
            l_lim = ((freq_std * math.pow(2, (j-1) *(1/12)))+(freq_std * math.pow(2, j *(1/12))))/2
            h_lim = ((freq_std * math.pow(2, (j+1) *(1/12)))+(freq_std * math.pow(2, j *(1/12))))/2
            if (in_freq > l_lim )and(in_freq < h_lim):
                in_code += hex(j)[2:4]
                break
        print(i, in_freq, j)

        #描画周り
        #plt.plot(freqList, amplitude, marker=".", linestyle="-", label = "fft plot")
        #plt.axis([0, 2000, 0, 7000])
        #plt.xlabel("frequency [Hz]")
        #plt.ylabel("amplitude")
        
        plt.show()

    for code in range(int(in_sec/2)):
        in_txt += chr(int(in_code[code*2:(code+1)*2], 16))
    print("input : ", in_code, "→", in_txt)
    #print(in_code[code*2:(code+1)*2], chr(int(in_code[code*2:(code+1)*2], 16)))
        
