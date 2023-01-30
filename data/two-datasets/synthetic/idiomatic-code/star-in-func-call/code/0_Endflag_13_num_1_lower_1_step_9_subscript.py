def func_arg(*e):
    pass
if __name__ == '__main__':
    e_list = [i for i in range(13)]
    func_arg(
    *e_list[1:10])
    print('code is finished')