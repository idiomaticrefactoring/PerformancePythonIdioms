import dis
def func_a():
    var_1 = 1
    var_2 = 2
    var_3 = 3
    var_4 = 4
    var_5 = 5
    var_6 = 6
    import time
    total_time = 0
    for i in range(100000000):
        if i<3:
            continue
        start_time_zejun = time.perf_counter()
        var_1, var_2 =1,2
        # var_1 , var_2 = var_2, var_1
        # var_1, var_2 , var_3= var_3, var_1, var_2
        # var_1, var_2, var_3 , var_4 =  var_4,var_1, var_2,var_3
        # var_1 , var_2 , var_3 , var_4 , var_5 , var_6  = var_6, var_1, var_2, var_3, var_4, var_5
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ',total_time)

if __name__ == '__main__':
    # func_a()
    dis.dis(func_a)
    # print('code is finished')


    '''
    ten = 10
    b_list = [4, 5, 6]
    a_list_list = [[1, 2, 3]]
    e = 5
    five_2 = 5
    three_3 = 3
    three = 3
    import time
    total_time=0
    for i in range(100000000):
        start_time_zejun = time.perf_counter()
        # five_2 == e >= three == three_3
        ten != e in b_list not in a_list_list
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time +=total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('code is finished: ',total_time)
    '''