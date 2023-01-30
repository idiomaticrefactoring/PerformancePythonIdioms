def func_a():
    a = 0j
    try:
        assert a == 0j
    except:
        pass
if __name__ == '__main__':
    func_a()
    print('code is finished')