def func_a():
    from fractions import Fraction
    a = Fraction(1, 1)
    try:
        assert not a
    except:
        pass
if __name__ == '__main__':
    func_a()
    print('code is finished')