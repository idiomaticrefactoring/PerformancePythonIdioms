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
        five_2 == e >= three
        # 20 != len(b_list) != 32
        # five_2 == e  >= three == three_3
        # ten != e in b_list not in a_list_list
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ',total_time)

if __name__ == '__main__':
    #func_a()
    # dis.dis(func_a)
    # print('code is finished')
    #'''
    ten = 10
    b_list = [4, 5, 6]
    a_list_list = [[1, 2, 3]]
    e = 5
    five_2 = 5
    three_3 = 3
    three = 3
    ten_2 = 10
    two_3 = 2
    import time
    total_time=0
    for i in range(100000000):
        if i<3:
            continue
        start_time_zejun = time.perf_counter()
        # five_2 == e >= three == three_3
        ten_2 >= e and e>= three and three> two_3

        # ten != e in b_list not in a_list_list
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time +=total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('code is finished: ',total_time)
    #'''