def func_a():
    a = dict({1:1})
    try:
        assert a != dict()
    except:
        pass
if __name__ == '__main__':
    func_a()
    print('code is finished')