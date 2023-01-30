def func_arg(*e):
    pass
def func_a():
    i_s=0
    e_list=[i for i in range(19)]
    func_arg(e_list[i_s],e_list[i_s+2],e_list[i_s+4],e_list[i_s+6],e_list[i_s+8],e_list[i_s+10],e_list[i_s+12],e_list[i_s+14])
if __name__ == '__main__':
    func_a()
    print('code is finished')