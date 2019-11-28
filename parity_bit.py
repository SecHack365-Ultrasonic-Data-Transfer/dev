def parity_bit_height(ascii_out,sp_len):
    vertical_checkbit_str = '0'
    for i in range(sp_len) : #縦のパリティビット作る
        ascii_out[i] = int(ascii_out[i],16)
        vertical_checkbit_str = hex(int(vertical_checkbit_str,16) ^ ascii_out[i])
        print('対象',hex(ascii_out[i]))
        print('縦パリティ経過',vertical_checkbit_str)
    sp_out =  vertical_checkbit_str
    print(sp_out)
    sp_out = parity_bit_side(sp_out)
    return sp_out

def parity_bit_side(ascii_out):
    print("parity_bitを振るよ！")
    side_checkbit_str = '0'
    ascii_array_str = list(bin(int(ascii_out,0))[2:])
    for j in range(len(ascii_array_str)) :
        int_bit = int(ascii_array_str[j],16)
        side_checkbit_str = hex(int(side_checkbit_str,16) ^ int_bit)

    print(side_checkbit_str)
    print(ascii_out)
    if '0x0' in side_checkbit_str:
        sp_out = int(ascii_out,16) + 0x00
        
    else :
        sp_out = int(ascii_out,16) + 0x80
    sp_0x_out = hex(sp_out)
    sp_out = hex(sp_out)[2:4]
    if len(sp_out) == 1 :
        sp_out = '0' + sp_out
    print('sp_out:',sp_out)
    return sp_out,sp_0x_out
