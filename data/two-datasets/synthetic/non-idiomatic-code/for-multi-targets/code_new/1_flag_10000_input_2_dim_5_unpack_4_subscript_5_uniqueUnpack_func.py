def func_a():
    input_seq=[[j for j in range(5)] for i in range(10000)]
    for e in input_seq:
        e[0]
        e[1]
        e[2]
        e[3]

if __name__ == '__main__':
    func_a()
    print('code is finished')