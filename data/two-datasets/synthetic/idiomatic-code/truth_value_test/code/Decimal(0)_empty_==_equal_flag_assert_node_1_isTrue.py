if __name__ == '__main__':
    from decimal import Decimal
    a = Decimal(0)
    try:
        assert not a
    except:
        pass
    print('code is finished')