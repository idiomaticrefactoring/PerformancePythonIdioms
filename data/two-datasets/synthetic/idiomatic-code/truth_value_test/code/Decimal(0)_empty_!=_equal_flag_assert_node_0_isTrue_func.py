def func_a():
    from decimal import Decimal
    a = Decimal(0)
    try:
        assert a
    except:
        pass
if __name__ == '__main__':
    func_a()
    print('code is finished')