import dis
def _a():
    five = 5
    e_1 = 5
    three_3 = 3
    ten = 10
    b_list = [4, 5, 6]
    a_list_list = [[1, 2, 3]]
    import time
    total_time = 0
    for i in range(100000000):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        # lines = []#12.4803
        # optional = False
        lines,optional = [],False#14.129

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
    print('func code is finished: ', total_time)
if __name__ == '__main__':
    _a()
    # dis.dis(_a)