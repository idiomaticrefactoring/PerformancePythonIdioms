def func_arg(*e):
    pass

def func_a():
    e_list = [i for i in range(23)]
    func_arg(
    *e_list)
if __name__ == '__main__':
    func_a()
    print('code is finished')