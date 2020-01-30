import sys

"""
どうやって使えばいい?
import read_header_latest
read_header_latest.main(受信データ[0:52?])
"""

### 拡張時になるべく計算式を変えずに済むように
code_len = 8                                       # 送信元/先 no.のbit数
seq_ack_len = 16                                    # seq/ack no.のbit数
flag_head = code_len*2 + seq_ack_len*2              # flagまでのbit数(書くと読みにくいから変数化)
flag_len = 4                                        # flagのbit数
bef_par_len = code_len*2 + seq_ack_len*2+flag_len   # パリティまでのbit数(書くと読みにくいから変数化)
par_len = 4                                         # パリティのbit数


### (16進4桁 -> 2進16桁)
def read_code(code: str) :
    return format(int(code, 2),"x")
    

### Seq No.(16 -> 8bit)
def read_no(no) :
    return int(no, 2)
  

### flag　(2進 -> ) 上位から(ack, rst, syn, fin)
def read_flag(flag_bin) :
    flag_bin = int(flag_bin, 2)
    flags = []
    if flag_bin/8 >= 1 :
        flags.append("ACK")
        flag_bin -= 8
    if flag_bin/4 >= 1 :
        flags.append("RST")
        flag_bin -= 4
    if flag_bin/2 >= 1 :
        flags.append("SYN")
        flag_bin -= 2
    if flag_bin/1 >= 1 :
        flags.append("FIN")
        flag_bin -= 1
    return flags


### パリティ計算
def calc_parity(recv_bin) :
    par_str = ""
    header_split = [0, code_len, code_len*2, code_len*2+seq_ack_len, code_len*2+seq_ack_len*2]      # 送信先, 送信元, seq/ack no., flagでsplitしてパリティ計算
    for i in range(0,len(header_split)-1) :
        par = 0
        for j in recv_bin[header_split[i]: header_split[i+1]] : 
            par = par ^ int(j)
        par_str += str(par ^ int(recv_bin[flag_head + i]))
    return par_str


### 送信bitからのパリティとパリティbitとの比較
def match_par(recv_par: str, calc_par: str) :
    match_par = format(int(recv_par, 2) ^ int(calc_par, 2), "b").zfill(par_len)
    check_par = format(0, "b").zfill(par_len)

    if match_par == check_par : #送信データが正しいなら1,違う場合は0を返す -> 0を返した場合はパケットを送り返さない
        return 1
    else :
        return 0
    
    
### main(bit列を受け取る -> 読める形におこす)
def main(recv_bin):
    recv_bin = format(int(recv_bin, 16), "b")
    recver_code = read_code(recv_bin[0: code_len])
    sender_code = read_code(recv_bin[code_len: code_len*2])
    recv_seq = read_no(recv_bin[code_len*2: (code_len*2 + seq_ack_len)])
    recv_ack = read_no(recv_bin[(code_len*2 + seq_ack_len): (code_len*2 + seq_ack_len*2)])
    recv_flag = read_flag(recv_bin[(code_len*2 + seq_ack_len*2): (code_len*2 + seq_ack_len*2+flag_len)])
    
    recv_par = recv_bin[(bef_par_len): (bef_par_len+par_len)]
    calc_par = calc_parity(recv_bin)
    
    check_par = match_par(recv_par, calc_par) 
    
    print("recv_code, sender_code, recv_seq, recv_ack, recv_flag, recv_par，calc_par, match?")
    print(recver_code, sender_code, recv_seq, recv_ack, recv_flag, recv_par, calc_par, check_par)
    return recver_code, sender_code, recv_seq, recv_ack, recv_flag, recv_par, calc_par, check_par