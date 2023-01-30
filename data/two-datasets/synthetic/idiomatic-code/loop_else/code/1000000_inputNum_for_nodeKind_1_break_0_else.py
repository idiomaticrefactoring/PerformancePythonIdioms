if __name__ == '__main__':
    e_list = [i for i in range(1000000)]
    for i in e_list:
        if i == 999999:
            break
    else:
        pass
    print('code is finished')