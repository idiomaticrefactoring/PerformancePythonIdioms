
if __name__ == '__main__':
    from decimal import Decimal
    a = Decimal(1)
    try:
        assert a != Decimal(0)
    except:
        pass
    print('code is finished')