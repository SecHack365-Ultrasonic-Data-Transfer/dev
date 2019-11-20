#coding:utf-8
import random
import sys

def read_flag(receive_flag):
    flag_name = []
    if receive_flag/32 >= 1 :
        flag_name.append("URG")
        receive_flag -= 32
    if receive_flag/16 >= 1 :
        flag_name.append("ACK")
        receive_flag -=  16
    if receive_flag/8  >= 1 :
        flag_name.append("PSH")
        receive_flag -=  8
    if receive_flag/4  >= 1 :
        flag_name.append("RST")
        receive_flag -=  4
    if receive_flag/2  >= 1 :
        flag_name.append("SYN")
        receive_flag -=  2
    if receive_flag/1  >= 1 :
        flag_name.append("FIN")
        receive_flag -=  1
    return flag_name

#　初期値設定用 : 最大値(2^32-1)を超えた場合,0に戻ってループ(オーバーフローが正常)
initial_digits = 16
initial_min = 0
initial_max = pow(2, initial_digits)-1
    
# 前回送信時の確認応答(ack)No.
receive_sequence = str(sys.argv[1][0:initial_digits])                   #先頭からシーケンスNo.取得
receive_ack  = str(sys.argv[1][initial_digits:initial_digits*2])        #ACK No.取得
receive_flag = str(sys.argv[1][initial_digits*2:initial_digits*2+6])    #flag取得

print(  "seq_num: "    + str(int(receive_sequence, 2))                  #出力情報
      + ", ack_num: "  + str(int(receive_ack, 2))
      + ", flag_num: " + str(read_flag(int(receive_flag, 2)))  )