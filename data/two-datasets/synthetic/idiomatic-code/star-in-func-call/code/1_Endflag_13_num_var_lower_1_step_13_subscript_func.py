def func_arg(*e):
    pass

def func_a():
    i_s = 0
    e_list = [i for i in range(13)]
    func_arg(
    *e_list[i_s:])
if __name__ == '__main__':
    func_a()
    print('code is finished')