if __name__ == '__main__':
    from fractions import Fraction
    a = Fraction(1, 1)
    try:
        assert not a
    except:
        pass
    print('code is finished')