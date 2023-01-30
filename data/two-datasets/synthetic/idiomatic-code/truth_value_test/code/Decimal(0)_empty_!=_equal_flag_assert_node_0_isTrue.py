if __name__ == '__main__':
    from decimal import Decimal
    a = Decimal(0)
    try:
        assert a
    except:
        pass
    print('code is finished')