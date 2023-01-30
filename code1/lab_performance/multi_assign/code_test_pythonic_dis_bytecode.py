import dis
import time
def func_a():
    five = 5
    e_1 = 5
    five_2 = 5
    e = 5
    three = 3
    three_3 = 3
    ten = 10
    b_list = [4, 5, 6]
    a_list_list = [[1, 2, 3]]

    total_time = 0
    for i in range(100000000):
        if i<3:
            continue
        start_time_zejun = time.perf_counter()
        (lines, optional) = ([], False)
        # malicious_type, blacklist_type = 'MALICIOUS_IPADDR', 'BLACKLISTED_IPADDR'
        # item_header, item_values, value_list, item, header, key, val, attribute, values, key_data, raw_output = False, False, False, None, None, None, None, None, None, None, []
        # options.dryrun, fmt = True, config_file.rsplit('.', 1)[-1]
        # lines, optional = [], False
        # five_2, e, three = 0,'1','2'
        # five_2, e, three = 0, 1.2, 3
        # five_2, e, three = 0, [1], True
        # five_2, e, three = [1],[2],[3]
        # five_2,e,three = five,e_1,three_3
        # five_2,e,three,ten = 5,5,3,10
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ',total_time)

    total_time_complicate = 0
    for i in range(100000000):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        lines=[]
        optional=False

        # malicious_type, blacklist_type = 'MALICIOUS_IPADDR', 'BLACKLISTED_IPADDR'
        # item_header, item_values, value_list, item, header, key, val, attribute, values, key_data, raw_output = False, False, False, None, None, None, None, None, None, None, []
        # options.dryrun, fmt = True, config_file.rsplit('.', 1)[-1]
        # lines, optional = [], False
        # five_2, e, three = 0,'1','2'
        # five_2, e, three = 0, 1.2, 3
        # five_2, e, three = 0, [1], True
        # five_2, e, three = [1],[2],[3]
        # five_2,e,three = five,e_1,three_3
        # five_2,e,three,ten = 5,5,3,10
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_complicate += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time_complicate,total_time_complicate/total_time)

if __name__ == '__main__':
    # func_a()
    # func_a()
    dis.dis(func_a)
    # print('code is finished')
    '''
    five_2 = 5
    e = 5
    three = 3
    ten = 10
    '''
    five = 5
    e_1 = 5
    three_3 = 3
    ten_2 = 10
    # five_2,e,three,ten = five,e_1,three_3,ten_2
    five_2,e,three,ten,ten_3 = five,e_1,three_3,ten_2,ten_2

    # five_2,e,three = five,e_1,three_3
    # five_2, e= five,e_1

    # five_2, e, three, ten = 5, 5, 3, 10

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