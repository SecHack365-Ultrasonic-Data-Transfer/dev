#coding:utf-8

"""
TCPヘッダ...
送信元ポートNo.(16bit),宛先ポートNo.(16bit)
シーケンスNo.(32bit)
確認応答(ack)No.(32bit)
データオフセット(4bit),予約(6bit),コントロールフラグ(6bit),ウインドウサイズ(16bit)
チェックサム(16bit),緊急ポインタ(16bit)
オプション(可変),パディング(可変)

→シーケンスNo./確認応答No.くらいは実装してみよう(桁数はinitial_digitsで変更可能)

import make_header
print(make_header.main("none", "none", "none", "none", "none"))
とかで実行。
def main(re_seq, re_ack, re_data_len, se_flag1, se_flag2):の順

"""

import random
import sys

#　初期値設定用 : 最大値(2^32-1)を超えた場合,0に戻ってループ(オーバーフローが正常)
initial_digits = 16
initial_min = 0
initial_max = pow(2, initial_digits)-1
print(initial_max)

# シーケンスNo.の更新/決定
def make_sequence_number(receive_sequence: int, receive_ack: int) -> int :
    if receive_sequence == -1 :                              #3ウェイハンドシェイク時(?)
        print(random.randint(initial_min, initial_max))
        return random.randint(initial_min, initial_max)
    else :                                                  #受信ack No. -> 送信シーケンスNo.
        print(int(receive_ack))
        return int(receive_ack) % (initial_max+1)

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

def make_flag_number(flag) -> int :
    flag_number = 0
    for i in flag :
        if i == "URG" :
            flag_number += 32
        elif i == "ACK" :
            flag_number += 16
        elif i == "PSH" :
            flag_number += 8
        elif i == "RST" :
            flag_number += 4
        elif i == "SYN" :
            flag_number += 2
        elif i == "FIN" :
            flag_number += 1
    return flag_number

"""
def make_checksum(sequence_number, ack_number):
	check = 0
	for i in range(0,int(initial_digits/4)):
		print(sequence_number[i*4:(i+1)*4])
		check += int(sequence_number[i*4:(i+1)*4], 2)
	print(check)
"""


def main(re_seq, re_ack, re_data_len, se_flag1, se_flag2):
	# 前回送信時の確認応答(ack)No.
	before_ack = 0
	send_flag = []
	# 各種受信情報 : -1 = 未設定
	if re_seq == "none" :     #初回起動(3wayハンドシェイクの開始)?
	    receive_sequence = -1   #シーケンスNo.
	    receive_ack = -1        #確認応答(ack)No.
	    receive_data_length = 0 #データ長ype() -- 別関数から持ってこよう
	    send_flag.append("SYN")
	else :                      #2回目以降の通信,おそらく最初数行はいらないけど保険(というかまた呼び出し方変えそうな予感)
	    receive_sequence = re_seq
	    receive_ack = re_ack
	    receive_data_length = re_data_len
	    #for i in range(4, len(sys.argv)):   #立てるflag
	    #    send_flag.append(sys.argv[i])
	    send_flag.append(se_flag1)
	    send_flag.append(se_flag2)
	sequence_number = format(make_sequence_number(receive_sequence, 
	                                              receive_ack       ), 'b').zfill(initial_digits)
	ack_number = format(make_ack_number(receive_ack, 
	                                    receive_data_length, 
	                                    before_ack           ), 'b').zfill(initial_digits)
	#make_checksum(sequence_number, ack_number)


	flag_number = format(make_flag_number(send_flag),'b').zfill(6)
	print(  "seq_num: "    + str(int(sequence_number, 2))   #出力情報
	      + ", ack_num: "  + str(int(ack_number, 2))     
	      + ", flag_num: " + str(send_flag) + " - " + str(int(flag_number, 2)) )
	
	return (sequence_number + ack_number + flag_number)     #純粋に繋ぎ合わせる(出力向け)