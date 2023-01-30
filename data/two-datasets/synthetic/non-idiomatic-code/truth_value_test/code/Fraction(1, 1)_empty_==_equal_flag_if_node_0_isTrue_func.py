def func_a():
    from fractions import Fraction
    a = Fraction(1, 1)
    if a == Fraction(0, 1):
        pass

if __name__ == '__main__':
    func_a()
    print('code is finished')