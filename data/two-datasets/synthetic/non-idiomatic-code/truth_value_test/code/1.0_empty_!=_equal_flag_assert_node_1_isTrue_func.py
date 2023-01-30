def func_a():
    a = 1.0
    try:
        assert a != 0.0
    except:
        pass
if __name__ == '__main__':
    func_a()
    print('code is finished')