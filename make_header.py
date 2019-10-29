"""
TCPヘッダ...
送信元ポートNo.(16bit),宛先ポートNo.(16bit)
シーケンスNo.(32bit)
確認応答(ack)No.(32bit)
データオフセット(4bit),予約(6bit),コントロールフラグ(6bit),ウインドウサイズ(16bit)
チェックサム(16bit),緊急ポインタ(16bit)
オプション(可変),パディング(可変)

→シーケンスNo./確認応答No.くらいは実装してみよう

実行 : make_binary.py <受信シーケンスNo.> <受信ack No.>　<受信データ長> #更新
      make_binary.py                                            　#初回実行(3wayハンドシェイク時の初期値決定)
"""

#coding:utf-8
import random
import sys

#　初期値設定用 : 最大値(2^32-1)を超えた場合,0に戻ってループ(オーバーフローが正常)
initial_min = 0
initial_max = pow(2, 32)-1

# シーケンスNo.の更新/決定
def make_sequence_number(receive_sequence: int, receive_ack: int) -> int :
    print(type(receive_sequence))
    if receive_sequence == -1 :                              #3ウェイハンドシェイク時(?)
        return random.randint(initial_min, initial_max)
    else :                                                  #受信ack No. -> 送信シーケンスNo.
        return int(receive_ack)

# 確認応答(ack)No.の更新/決定
def make_ack_number(receive_ack: int, receive_data_length: int, before_ack: int) -> int :
    if receive_ack == -1 :                                   #3ウェイハンドシェイク時(?)
        return random.randint(initial_min, initial_max)
    else :
        if receive_data_length == 0 :                       #分割制御時(ackだけ帰ってきてデータなし)
            return before_ack
        else :                                              #通常制御時(ack No.の更新)
            send_ack = int(receive_sequence) + int(receive_data_length)
            
            return send_ack % (initial_max+1)

# 前回送信時の確認応答(ack)No.
before_ack = 0

# 各種受信情報 : -1 = 未設定
if len(sys.argv) == 1 :     #初回起動(3wayハンドシェイクの開始)?
    receive_sequence = -1   #シーケンスNo.
    receive_ack = -1        #確認応答(ack)No.
    receive_data_length = 0 #データ長ype() -- 別関数から持ってこよう
else :                      #2回目以降の通信
    receive_sequence = int(sys.argv[1])
    receive_ack = int(sys.argv[2])
    receive_data_length = int(sys.argv[3])

sequence_number = format(make_sequence_number(receive_sequence, 
                                                  receive_ack  ), 'b').zfill(32)
ack_number = format(make_ack_number(receive_ack, 
                                    receive_data_length, 
                                    before_ack         ), 'b').zfill(32)
print(sequence_number+ack_number)     #純粋に繋ぎ合わせる(出力向け)