def func_a():
    from decimal import Decimal
    a = Decimal(0)
    try:
        assert a != Decimal(0)
    except:
        pass
if __name__ == '__main__':
    func_a()
    print('code is finished')