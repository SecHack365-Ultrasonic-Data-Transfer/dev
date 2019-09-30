#これなに? : 音が出るよ
#参考 : https://fardog.io/blog/2013/02/16/making-noise-in-python/

#coding:utf-8
import math
import numpy
import pyaudio

sound_freq = 14000    #[Hz] : 再生したい音の周波数
sound_len = 1    #[sec]? : 再生したい長さ

def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)

def play_tone(stream, frequency=sound_freq, length=sound_len, rate=44100):
    chunks = []
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks) * 0.25
    stream.write(chunk.astype(numpy.float32).tostring())

if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, output=1)
    play_tone(stream)
    stream.close()
    p.terminate()