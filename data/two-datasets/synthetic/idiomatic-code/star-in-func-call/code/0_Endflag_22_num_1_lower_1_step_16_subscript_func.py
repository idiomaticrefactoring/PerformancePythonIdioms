def func_arg(*e):
    pass

def func_a():
    e_list = [i for i in range(22)]
    func_arg(
    *e_list[1:17])
if __name__ == '__main__':
    func_a()
    print('code is finished')