def parity_check(in_code) :
    out_code = ''
    for code in range(int(len(in_code)/2)):
        txt = (int(in_code[code*2:(code+1)*2], 16))
        if txt >= 128 :
            txt -= 128
        out_code += chr(txt)
        print(out_code)
    return out_code

def parity_checker(in_code) :
    out_code = ''
    vertical_parity = '0'
    parity_flg = True
    for code in range(int(len(in_code)/2)):
        txt = (int(in_code[code*2:(code+1)*2], 16))
        txt1 = (int(in_code[code*2], 16))
        txt2 = (int(in_code[code*2+1],16))

        #横のパリティチェック
        txt_str = list(bin(txt)[2:])
        side_checkbit_str = '0'
        for j in range(len(txt_str)) :
            int_bit = int(txt_str[j],16)
            side_checkbit_str = hex(int(side_checkbit_str,16) ^ int_bit)
        if side_checkbit_str != '0x0' :
            parity_flg = False
            print(side_checkbit_str,'残念')
        else :
            print(side_checkbit_str,'セーフ')

        
        
        print(txt_str)

        print('tex1:',txt1)
        print('txt2:',txt2)
        #パリティを外すとこ
        
        print(int(len(in_code)/2))
        if code != int(len(in_code)/2) :
            if txt >= 128 :
                txt -= 128
            out_code += chr(txt)
        else :
            vertical_parity = txt

        print(out_code)

    #縦にパリティチェック
    vertical_checkbit_str = '0'
    for code in range(int(len(in_code)/2)) : 
        if code != int(len(in_code)/2) :
            txt = (int(in_code[code*2:(code+1)*2], 16))
            vertical_checkbit_str = hex(int(vertical_checkbit_str,16) ^ txt)
            print(vertical_checkbit_str)

    if int(vertical_parity) != int(vertical_checkbit_str,16) :
        parity_flg = False
        print(vertical_checkbit_str)
        print(vertical_parity)

    print(parity_flg)
    return out_code,parity_flg
