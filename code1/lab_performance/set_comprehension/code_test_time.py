import time
def func_a():
    x_0 = list(range(1,1000001))
    x_0 = list(range(1, 101))
    x_1 = list(range(1, 101))
    x_2 = list(range(1, 101))
    x_0 = []  #
    x_1 = []
    x_2 = []
    total_time = 0
    for i in range(repeat):
        time_s = time.perf_counter()

        l = set()
        for e_0 in x_0:
            for e_1 in x_1:
                for e_2 in x_2:
                    if e_0 % 2:
                        l.add(e_0 * 100000 + e_1 * 1000 + e_2)
                    elif e_0 % 2:
                        l.add(e_0 * 100000 + e_1 * 1000 + e_2)
                    else:
                        l.add(e_0 * 100000 + e_1 * 1000 + e_2)
        # l = set()
        # for e_0 in x_0:
        #     if e_0 // 1:
        #         if e_0 // 1:
        #             if e_0 // 1:
        #                 l.add(e_0)

        # l = set()
        # for e_0 in x_0:
        #     if e_0 // 1:
        #         l.add(e_0)


        # l = set()
        # for e_0 in x_0:
        #     for e_1 in x_1:
        #         for e_2 in x_2:
        #             if e_0 % 2:
        #                 l.add(e_0 * 100000 + e_1 * 1000 + e_2)
        #             else:
        #                 if e_0 % 2:
        #                     l.add(e_0 * 100000 + e_1 * 1000 + e_2)
        #                 else:
        #                     l.add(e_0 * 100000 + e_1 * 1000 + e_2)
        # l = set()
        # for e_0 in x_0:
        #     l.add(e_0)
        time_e = time.perf_counter()
        if i < 3:
            continue
        total_time += time_e - time_s
    total_time_pythonic = 0
    for i in range(repeat):

        time_s = time.perf_counter()
        # l = {e_0 for e_0 in x_0}
        # l = {e_0 for e_0 in x_0 if e_0 // 1}
        # l = {e_0 for e_0 in x_0 if e_0 // 1 if e_0 // 1 if e_0 // 1}
        l = {
            e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2
            for e_0 in x_0 for e_1 in x_1 for e_2 in x_2}
        # l = {
        #     e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2
        #     for e_0 in x_0 for e_1 in x_1 for e_2 in x_2}
        time_e = time.perf_counter()
        if i < 3:
            continue
        total_time_pythonic += time_e - time_s

    print('code is finished', total_time_pythonic, total_time, total_time / total_time_pythonic)

if __name__ == '__main__':
# repeat=10**2
    repeat=10**3

    x_0 = []#list(range(1, 100001))
    x_1=[]
    x_2=[]
    # x_0 = list(range(1, 1000001))

    total_time=0
    # func_a()
    #'''
    for i in range(repeat):

        time_s = time.perf_counter()

        # l = set()
        # for e_0 in x_0:
        #     if e_0 // 1:
        #         if e_0 // 1:
        #             if e_0 // 1:
        #                 l.add(e_0)
        l = set()
        for e_0 in x_0:
            for e_1 in x_1:
                for e_2 in x_2:
                    if e_0 % 2:
                        l.add(e_0 * 100000 + e_1 * 1000 + e_2)
                    elif e_0 % 2:
                        l.add(e_0 * 100000 + e_1 * 1000 + e_2)
                    else:
                        l.add(e_0 * 100000 + e_1 * 1000 + e_2)

        # l = set()
        # for e_0 in x_0:
        #     l.add(e_0)


        # l = set()
        # for e_0 in x_0:
        #     if e_0 // 1:
        #         l.add(e_0)
        time_e = time.perf_counter()
        if i<3:
            continue
        total_time+=time_e-time_s
    total_time_pythonic = 0
    for i in range(repeat):

        time_s = time.perf_counter()
        # l = {e_0 for e_0 in x_0}
        # l = {e_0 for e_0 in x_0 if e_0 // 1 if e_0 // 1 if e_0 // 1}
        l = {
            e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2
            for e_0 in x_0 for e_1 in x_1 for e_2 in x_2}
        # l = {e_0 for e_0 in x_0 if e_0 // 1}
        time_e = time.perf_counter()
        if i<3:
            continue
        total_time_pythonic += time_e - time_s

    print('code is finished',total_time_pythonic,total_time,total_time/total_time_pythonic)
#'''
'''
x_0 = list(range(1,1000001))
x_0 = list(range(1,101))
x_1 = list(range(1, 101))
x_2 = list(range(1, 101))
total_time = 0
for i in range(repeat):
    time_s = time.time()
    # l = set()
    # for e_0 in x_0:
    #     if e_0 // 1:
    #         l.add(e_0)


    l = set()
    for e_0 in x_0:
        for e_1 in x_1:
            for e_2 in x_2:
                if e_0 % 2:
                    l.add(e_0 * 100000 + e_1 * 1000 + e_2)
                else:
                    if e_0 % 2:
                        l.add(e_0 * 100000 + e_1 * 1000 + e_2)
                    else:
                        l.add(e_0 * 100000 + e_1 * 1000 + e_2)
    # l = set()
    # for e_0 in x_0:
    #     l.add(e_0)
    time_e = time.time()
    if i < 3:
        continue
    total_time += time_e - time_s
total_time_pythonic = 0
for i in range(repeat):

    time_s = time.time()
    # l = {e_0 for e_0 in x_0}
    # l = {e_0 for e_0 in x_0 if e_0 // 1}
    l = {
        e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2
        for e_0 in x_0 for e_1 in x_1 for e_2 in x_2}
    time_e = time.time()
    if i < 3:
        continue
    total_time_pythonic += time_e - time_s

print('code is finished', total_time_pythonic, total_time, total_time / total_time_pythonic)
'''