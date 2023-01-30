
if __name__ == '__main__':
    a = dict({1:1})
    try:
        assert a == dict()
    except:
        pass
    print('code is finished')