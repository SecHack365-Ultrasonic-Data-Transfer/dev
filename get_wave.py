# - coding: utf-8 -
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from scipy import signal

import statistics
import math

import codecs
import collections

if __name__ == '__main__':
    in_file = "hoge.wav"
    
    data, rate = sf.read(in_file)
    
    in_sec = len(data) / rate
    for i in range(int(in_sec)):
        print(i)
        X = fftpack.fft(data[i*44100:(i+1)*44100])
        freqList = fftpack.fftfreq(44100, d=1.0/ rate)
        
        amplitude = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]
        print(amplitude.index(max(amplitude)))  #1番大きい振幅を拾ってるだけ(雑音出たら、たぶん上手くいかない)
        
        plt.plot(freqList, amplitude, marker=".", linestyle="-", label = "fft plot")
        plt.axis([0, 2000, 0, 7000])
        plt.xlabel("frequency [Hz]")
        plt.ylabel("amplitude")
        
        plt.show()