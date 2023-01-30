import time
if __name__ == '__main__':
    input_seq = [[[k for k in range(5)] for j in range(5)] for i in range(1000)]
    import time

    for i in range(20):

        start_time_zejun = time.perf_counter()
        for ((e_0_0, e_0_1), (e_1_0, e_1_1)) in input_seq:
            e_0_0
            e_0_1
            e_1_0
            e_1_1
            e_0_0
            e_0_1
            e_1_0
            e_1_1
            e_0_0
            e_0_1
            e_1_0
            e_1_1
            e_0_0
            e_0_1
            e_1_0
    # time_s=time.time()
    # for i in range(35):
    #     input_seq=[[j for j in range(4)] for i in range(100000)]
    #     for e in input_seq:
    #         e[0]
    #         e[1]
    #         e[2]

    print('code is finished',time.time()-time_s)