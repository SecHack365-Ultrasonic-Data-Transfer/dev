#なにこれ? : 入力した文字列を配列の何番目にあるやつなのかを出す
#何がしたいの? : これ+周波数を割り当てた配列使って、音を出させる
#coding:utf-8

input = "hogehoge"
sp_len = 0
sp_input = {}

if __name__ == '__main__':
    sp_len = len(input)
    sp_input = list(input)  #input -> 1文字ずつ
    for i in range(sp_len) :
        print(ord(sp_input[i])) #受け取る側はchr(int(hoge, 16))で戻して