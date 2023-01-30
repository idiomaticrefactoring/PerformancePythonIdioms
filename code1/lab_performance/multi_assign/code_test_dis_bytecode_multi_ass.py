import dis
def func_a():
    repeat=10**6
    var_1, var_2,var_3,var_4=0,1,2,0
    var_1_copy, var_2_copy, var_3_copy, var_4_copy= 0, 1, 2, 0
    five=5
    e_1 = 5
    three_3 = 3
    ten = 10
    b_list = [4, 5, 6]
    a_list_list = [[1, 2, 3]]
    import time
    total_time = 0
    for i in range(repeat):
        if i<3:
            continue
        start_time_zejun = time.perf_counter()
        var_1, var_2, var_3, var_4 = 0, 1, 2, 0
        # var_1, var_2,var_3 = var_3,var_1,var_2
        # var_1, var_2, var_3, var_4 = var_4, var_1, var_2, var_3
        var_1, var_2, var_3, var_4 = var_1_copy, var_2_copy, var_3_copy, var_4_copy

        # (lines, optional) = ([], False)
        # cfgstr, dpath, fname, verbose = self._rectify_cfgstr(cfgstr), self.dpath, self.fname, self.verbose
        #
        # (lines, optional) = ([], False)
        # options.dryrun= True
        # fmt =config_file.rsplit('.', 1)[-1]
        #
        # lines = []
        # optional = False
        # five_2 = five
        # e = e_1
        # three = three_3
        # # ten = 10
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    total_time_old = 0
    for i in range(repeat):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        var_1=0
        var_2=1
        var_3=2
        var_4 = 0

        # var_1 = var_1_copy,
        # var_2 = var_2_copy,
        # var_3 = var_3_copy,
        # var_4 = var_4_copy

        # lines = []
        # optional = False
        # tmp_1 = var_1
        # tmp_2 = var_2
        # tmp_3 = var_3
        # var_1 = var_4
        # var_2 = tmp_1
        # var_3=tmp_2
        # var_4 = tmp_3

        # tmp_1 = var_1
        # tmp_2 = var_2
        # var_1 = var_3
        # var_2 = tmp_1
        # var_3=tmp_2

        # tmp=var_1
        # var_1=var_2
        # var_2 = tmp
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_old += total_time_zejun

    print('func code is finished: ',total_time_old,total_time,total_time_old/total_time)
if __name__ == '__main__':
    func_a()
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
    ten_2=10

    five_2 = five
    e = e_1
    three = three_3
    ten=ten_2


    '''
    e = 5
    ten=10
    b_list=[4,5,6]
    a_list_list=[[1,2,3]]
    five_2 = 5
    three_3 = 3
    three = 3
    import time

    total_time = 0
    for i in range(100000000):
        start_time_zejun = time.perf_counter()
        # e >= three and five_2 == e and three == three_3
        e != ten and e in b_list and b_list not in a_list_list
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('code is finished: ',total_time)
    '''