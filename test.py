import pyaudio
import time
import sys
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from scipy import signal

input_device = 0  # 入力デバイス
output_device = 1  # 出力デバイス
sampling_rate = 44100  # サンプリングレート マイクの特性に合わせる
CHUNK = 2 ** 10  # データ長になる
record_seconds = 1.0  # サンプリングする必要最低限の時間
freq_limit = 12000  # Hz


class Plot():  # もうすこしマトモなclassにしたい
    def __init__(self):
        self.fig, self.ax = plt.subplots(1, 1)
        self.lines, = self.ax.plot(0, 0, color='b')  # 第一プロット
        self.lines2, = self.ax.plot(0, 0, color='c')  # 第二プロット
        self.lines3, = self.ax.plot(0, 0)  # 第三プロット
        self.points, = self.ax.plot(0, 0, color='orange', marker='o', markersize=15, linestyle='None')  # ポイント
        self.target, = self.ax.plot(0, 0, color='red', marker='o', markersize=15, linestyle='None')
        #カットオフ周波数表示
        self.ann = self.ax.annotate("", (0, 0))
        self.ann2 = self.ax.annotate("", (0, 0))
        self.ann3 = self.ax.annotate("", (0, 0))
        plt.yscale('symlog')

    def set(self, x_data, y_data):
        self.lines.set_data(x_data, y_data)
        # 現在の値を取得(これで合ってる？)
        y = y_data[-1]
        # 値を更新
        self.ann.set_text(f'fe1={y:0.2f}')
        # 動的に表示箇所を変更する場合は以下のような処理を記述
        self.ann.set_position((0, y))
        self.ax.set_xlim(0, x_data.max())
        self.ax.set_ylim(0, y_data.max())

    def set2(self, x_data, y_data):
        self.lines2.set_data(x_data, y_data)
        # self.ax.set_xlim(0, x_data.max())
        # self.ax.set_ylim(0, y_data.max())

    def set3(self, x_data, y_data):
        self.lines3.set_data(x_data, y_data)
        # self.ax.set_xlim(0, x_data.max())
        # self.ax.set_ylim(0, y_data.max())


    def set_points(self, x_data, y_data):
        self.points.set_data(x_data, y_data)

    def set_targets(self, x_data, y_data):
        self.targets(x_data, y_data)

    def pause(self):
        plt.pause(.01)

    def close(self):
        plt.close()


class AudioFilter():
    def __init__(self):
        # オーディオに関する設定
        self.p = pyaudio.PyAudio()
        self.channels = 1  # モノラル
        self.format = pyaudio.paFloat32
        self.voice_data = deque([], maxlen=int(sampling_rate * record_seconds))
        self.filtered_data = deque([], maxlen=int(sampling_rate * record_seconds))
        self.noise_data = deque([], maxlen=int(sampling_rate * record_seconds))
        self.rate = sampling_rate
        self.chunk = CHUNK
        self.idt = ''
        self.fe1 = 100/(sampling_rate/2)
        self.fe2 = 10000/(sampling_rate/2)
        self.min_id = []
        self.minimum = []
        #self.filter1 = signal.firwin(numtaps=255, cutoff=[self.fe1,self.fe2], pass_zero=False)
        self.audio_data = ''
        # self.time = {}
        self.stock_sec = record_seconds
        self.buf = np.array([])

        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            output=True,
            input=True,
            frames_per_buffer=self.chunk,  # バッファごとのフレーム長を指定
            input_device_index=input_device,
            output_device_index=output_device,
            stream_callback=self.callback  # コールバック関数の指定
        )

    # コールバック関数（chunk貯まるたびに呼び出される。長い処理を書くと再帰が深くなる）
    def callback(self, in_data, frame_count, time_info, status):
        filter1 = signal.firwin(numtaps=255, cutoff=[self.fe1, self.fe2], pass_zero=False)#フィルタの定義

        #min_idに値が入ったとき、それに合わせカットオフ周波数を変更
        if len(self.minimum) >= 1:
            j = 0
            #サンプリングレートの1/2以上の値を除外
            for i in self.minimum:
                if i > 20000 or i < 100:
                    j += 1
                else:
                    break
            #カットオフ周波数の変更
            self.fe1 = (self.minimum[j]-100)/ (sampling_rate / 2)
            self.fe2 = (self.minimum[j]+100)/ (sampling_rate / 2)
            print('fe1 and fe2 is',self.minimum[j]-100,self.minimum[j]+100)


        self.buf = np.frombuffer(in_data, dtype="float32")
        filt = signal.lfilter(filter1, 1, self.buf)
        self.noise_data.extend(self.buf)  # 環境音データ
        # self.voice_data.extend(self.buf)  # 加工前の音声データ
        self.filtered_data.extend(filt)  # 加工後の音声データ
        out_data = filt.astype("float32").tostring()  # 加工した音声データを出力
        return (out_data, pyaudio.paContinue)

    def filtering(self):
        return 0

    def close(self):
        self.p.terminate()


if __name__ == '__main__':

    freqList = np.fft.fftfreq(int(sampling_rate * record_seconds), d=1.0 / sampling_rate)
    pt = Plot()  # プロット用

    af = AudioFilter()  # AudioFilterのインスタンス
    af.stream.start_stream()  # ストリーミングを始める

    #  ノンブロッキングなので好きなことをしていていい場所
    while af.stream.is_active():
        if (len(af.noise_data) >= int(sampling_rate * record_seconds)):

            data = np.array(af.noise_data)
            af.noise_data.clear()
            x = np.fft.fft(data)

            filtered_data = np.array(af.filtered_data)
            af.filtered_data.clear()
            fft_filtered_data = np.fft.fft(filtered_data)

            amplitude = np.array([np.sqrt(c.real ** 2 + c.imag ** 2) for c in x])  # 振幅スペクト
            amplitude_filtered_data = np.array([np.sqrt(c.real ** 2 + c.imag ** 2) for c in fft_filtered_data])
            pt.set(freqList[:int(len(freqList) / 2)], amplitude[:int(len(freqList) / 2)])  # 環境音プロット
            pt.set2(freqList[:int(len(freqList) / 2)], amplitude_filtered_data[:int(len(freqList) / 2)])  # 加工後音声プロット

            # 下限ピーク検出
            af.min_id = signal.argrelmin(amplitude, order=1000)  # small peaks
            ary = amplitude[af.min_id]
            pt.set_points(af.min_id, ary)
            targets = np.sort(ary)
            pt.pause()
            #print(ary)

            # 下限ピークを昇順に並び替え
            af.minimum = af.min_id[0][ary.argsort()]
            print(af.minimum)

    pt.close()

    # ストリーミングを止める場所
    af.stream.stop_stream()
    af.stream.close()
    af.close()
