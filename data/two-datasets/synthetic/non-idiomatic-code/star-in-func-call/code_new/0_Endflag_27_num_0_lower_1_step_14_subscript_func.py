def func_arg(*e):
    pass
def func_a():
    e_list=[i for i in range(27)]
    func_arg(e_list[0],e_list[1],e_list[2],e_list[3],e_list[4],e_list[5],e_list[6],e_list[7],e_list[8],e_list[9],e_list[10],e_list[11],e_list[12],e_list[13])
if __name__ == '__main__':
    func_a()
    print('code is finished')