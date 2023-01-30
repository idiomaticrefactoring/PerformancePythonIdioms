import dis
def func_a():
    five_2 = 5
    e = 5
    three = 3
    three_3 = 3
    ten = 10
    b_list = [4, 5, 6]
    a_list_list = [[1, 2, 3]]
    import time
    total_time = 0
    for i in range(10000000):

        start_time_zejun = time.perf_counter()
        # e >= three and five_2 == e
        while a:
            pass
        while a:
            break
        else:
            a
        if a:
            pass
        if a:
            pass
        else:
            b=1
        if a:
            a=1
        else:
            b=1
        if a:
            pass
        assert a
         # 20 != len(b_list) and len(b_list) != 32
        # e >= three and five_2 == e and (three == three_3)
        # e != ten and e in b_list and b_list not in a_list_list
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ',total_time)
if __name__ == '__main__':
    # func_a()
    dis.dis(func_a)
    # print('code is finished')
    import time

    data=[1]
    start_time_zejun = time.perf_counter()
    if data is None or len(data) == 0:
        end_time_zejun = time.perf_counter()
    total_time_zejun = end_time_zejun - start_time_zejun
    print('\n*********zejun test total time************** ', total_time_zejun)
    '''
    e = 5
    ten=10
    b_list=[4,5,6]
    a_list_list=[[1,2,3]]
    five_2 = 5
    three_3 = 3
    three = 3
    ten_2=10
    two_3=2
    import time

    total_time = 0
    for i in range(100000000):
        if i<3:
            continue
        start_time_zejun = time.perf_counter()
        # e >= three and five_2 == e and three == three_3
        ten_2 >= e >= three > two_3
        # e != ten and e in b_list and b_list not in a_list_list
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('code is finished: ',total_time)
    '''