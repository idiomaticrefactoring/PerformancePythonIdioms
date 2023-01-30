def func_arg(*e):
    pass

if __name__ == '__main__':
    i_s=0
    e_list=[i for i in range(15)]
    func_arg(e_list[i_s],e_list[i_s+2],e_list[i_s+4],e_list[i_s+6],e_list[i_s+8],e_list[i_s+10],e_list[i_s+12])
    print('code is finished')