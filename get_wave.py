# - coding: utf-8 -
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from scipy import signal
import math
def get_wave1():
    freq_std = 440
    length = 0.1


    #if __name__ == '__main__':
    in_file = "hoge.wav"
    
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

        """
        #描画周り
        plt.plot(freqList, amplitude, marker=".", linestyle="-", label = "fft plot")
        plt.axis([0, 5000, 0, 7000])
        plt.xlabel("frequency [Hz]")
        plt.ylabel("amplitude")
        plt.show()
        """
        
        for amp in amplitude:
            if (amp > 3500) and (amplitude.index(amp) not in in_freq):
                in_freq.append(amplitude.index(amp))
        #amplitude.index(max(amplitude))  #1番大きい振幅を拾ってるだけ(雑音出たら、たぶん上手くいかない)
        
        for j in range(16):
            l_lim = ((freq_std * math.pow(2, (j-1) *(1/12)))+(freq_std * math.pow(2, j *(1/12))))/2
            h_lim = ((freq_std * math.pow(2, (j+1) *(1/12)))+(freq_std * math.pow(2, j *(1/12))))/2
            if (in_freq[0] > l_lim )and(in_freq[0] < h_lim):
                in_code += hex(j)[2:4]
                break
        print(i, in_freq, hex(j)[2:4])

        i += 1
    for code in range(int(len(in_code)/2)):
        in_txt += chr(int(in_code[code*2:(code+1)*2], 16))
    print("input : ", in_code, "→", in_txt)
    #print(in_code[code*2:(code+1)*2], chr(int(in_code[code*2:(code+1)*2], 16)))
        
