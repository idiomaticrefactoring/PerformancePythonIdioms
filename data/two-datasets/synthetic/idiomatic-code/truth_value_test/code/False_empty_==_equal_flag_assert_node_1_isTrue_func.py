def func_a():
    a = False
    try:
        assert not a
    except:
        pass
if __name__ == '__main__':
    func_a()
    print('code is finished')