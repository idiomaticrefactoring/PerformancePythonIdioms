def func_arg(*e):
    pass

if __name__ == '__main__':
    i_s=0
    e_list=[i for i in range(12)]
    func_arg(e_list[i_s],e_list[i_s+1],e_list[i_s+2],e_list[i_s+3],e_list[i_s+4],e_list[i_s+5],e_list[i_s+6])
    print('code is finished')