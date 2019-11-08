#メモ : これなに?
#文字入れたらasciiコード化、16進化した上で音にして流すよ

#参考 : https://fardog.io/blog/2013/02/16/making-noise-in-python/
#複数音鳴らせれば(和音を作り出せれば)、伝送ミスのチェックと再送要求が楽になる?


#coding:utf-8
import math
import numpy
import pyaudio

#---
import numpy
from scipy.io import wavfile

#音声出力関係
#freq_std = 1760
freq_math = {}

#---
freq_std = 440

#文字→音声化のための変換関係
sp_len = 0
sp_in = {}

#chunks = []

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
def play_tone(stream, frequency, length=0.1, rate=44100):
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
    vertical_checkbit_str = '0'
    ascii_out = []
    for i in range(sp_len) :
        ascii_out.append(hex(ord(sp_in[i])))
        sp_out += str(hex(ord(sp_in[i])))[2:4] #ascii化→16進化→文字列化
    
    #横のパリティビット作る
        side_checkbit_str = '0'
        ascii_array_str = list(bin(int(ascii_out[i],0))[2:])
        for j in range(len(ascii_array_str)) :
            int_bit = int(ascii_array_str[j],16)
            side_checkbit_str = hex(int(side_checkbit_str,16) ^ int_bit)
        sp_out += str(side_checkbit_str)[2:4]



    for i in range(sp_len) : #縦のパリティビット作る
        ascii_out[i] = int(ascii_out[i],16)
        vertical_checkbit_str = hex(int(vertical_checkbit_str,16) ^ ascii_out[i])
    sp_out += str(vertical_checkbit_str)[2:4]

    #縦のパリティの横のパリティ
    side_checkbit_str = '0'
    ascii_array_str = list(bin(int(vertical_checkbit_str,0))[2:])
    for j in range(len(ascii_array_str)) :
        int_bit = int(ascii_array_str[j],16)
        side_checkbit_str = hex(int(side_checkbit_str,16) ^ int_bit)
    sp_out += str(side_checkbit_str)[2:4]
    return sp_out

if __name__ == '__main__':
    in_txt = input("send message :")
    out_txt = txt_to_asciicode(in_txt)
    
    print(in_txt, "→", out_txt)
    
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