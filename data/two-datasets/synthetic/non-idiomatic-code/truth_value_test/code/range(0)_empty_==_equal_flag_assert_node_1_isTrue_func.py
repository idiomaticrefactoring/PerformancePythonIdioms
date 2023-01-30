def func_a():
    a = range(0)
    try:
        assert a == range(0)
    except:
        pass
if __name__ == '__main__':
    func_a()
    print('code is finished')