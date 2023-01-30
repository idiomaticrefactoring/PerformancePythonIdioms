def func_a():
    a = None
    try:
        assert a == None
    except:
        pass
if __name__ == '__main__':
    func_a()
    print('code is finished')