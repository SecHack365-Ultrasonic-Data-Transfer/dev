import sys
import random
"""
どうやって使えばいい?
import make_header_latest
make_header_latest.main(<送信元>, <送信先>, <受信seq>, <受信ack>, <受信データ長>, <["flag1","flag2"]>)
出力は64bit化(余った部分は一先ずパディング)
"""

init_digits = 16                        #seq/ack no.のbit数
init_min = 0                            #seq/ack no.の最小値(いらなくね?)
init_max = pow(2, init_digits) - 1      #seq/ack no.の最大値
flag_pos = 6                            #flag指定位置

code_len = 8
seq_ack_len = 16
flag_head = code_len*2 + seq_ack_len*2

### (16進4桁 -> 2進16桁)
def conv_code(code: str) :
    return format(int(code, base=16), "b").zfill(code_len)
    

### 3wayハンドシェイク(の初期値決め)
def make_3way_hand_shake() :
    return random.randint(initial_min, init_max)


### Seq No.(16 -> 8bit)
def update_seq_no(recv_seq: int, recv_ack: int) -> int :
    if recv_seq == -1 :     #3wayハンドシェイク開始時
        return make_3way_hand_shake().zfill(seq_ack_len)
    else :
        return format(int(recv_ack) % int(init_max + 1), "b").zfill(seq_ack_len)


### Ack No.(16 -> 16bit)
def update_ack_no(receive_ack, recv_seq, recv_data_len) :
    if receive_ack == -1 :  #3wayハンドシェイク開始時
        print("-> 3way(ack)")
        return make_3way_hand_shake().zfill(seq_ack_len)
    else :
        return format((int(recv_seq) + int(recv_data_len)) % int(init_max + 1), "b").zfill(seq_ack_len)


### flag　(10進 -> 2進) 上位から(ack, rst, syn, fin)
def make_send_flag(flag) -> int :
    flag_num = 0
    for i in flag : 
        if i == "ACK" : 
            flag_num += 8
        if i == "RST" : 
            flag_num += 4
        if i == "SYN" : 
            flag_num += 2
        if i == "FIN" : 
            flag_num += 1   
    return format(int(flag_num), "b").zfill(4)


### パリティチェックbitの生成
###生成ルール : 送信元 + flag[0](ack)，送信先 + flag[1]， ...
def make_parity(send_bin) :
    par_str = ""
    header_split = [0, code_len, code_len*2, code_len*2+seq_ack_len, code_len*2+seq_ack_len*2]      # 送信先, 送信元, seq/ack no., flagでsplitしてパリティ計算
    for i in range(0,len(header_split)-1) :
        par = 0
        for j in send_bin[header_split[i]: header_split[i+1]] : 
            par = par ^ int(j)
        par_str += str(par ^ int(send_bin[flag_head + i]))
    return par_str


### main
def main(my_code, oth_code, recv_seq, recv_ack, recv_data_len, flag):
    send_bin = ""            # 送信bin用(文字列ととして追加していく)
    par = 0
    # 送信用binの作成(別に16進で管理しても良いのでは…?)
    sender_code = conv_code(my_code)                                  # 送信元(16進 -> 2進)
    recver_code = conv_code(oth_code)                                 # 送信先(16進 -> 2進)
    send_seq = update_seq_no(recv_seq, recv_ack)                   # seq no.の更新
    send_ack = update_ack_no(recv_ack, recv_seq, recv_data_len)    # ack no.の更新
    send_flag = make_send_flag(flag)                           # flag
    send_bin += sender_code + recver_code + send_seq + send_ack + send_flag
    send_par = make_parity(send_bin)
    padding = str("0").zfill(64-len(send_bin))                    # 16 or 32の倍数にしよう ->　近かった64までパディングで埋める(今後の拡張・変更を見据えて)
 
    send_bin +=  send_par + padding

    return send_bin, sender_code, recver_code, send_seq, send_ack, send_flag, send_par, padding