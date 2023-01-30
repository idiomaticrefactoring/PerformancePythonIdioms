
if __name__ == '__main__':
    a = range(1)
    try:
        assert a == range(0)
    except:
        pass
    print('code is finished')