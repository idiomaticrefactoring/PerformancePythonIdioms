def func_arg(*e):
    pass

def func_a():
    e_list = [i for i in range(24)]
    func_arg(
    *e_list[:14:2])
if __name__ == '__main__':
    func_a()
    print('code is finished')