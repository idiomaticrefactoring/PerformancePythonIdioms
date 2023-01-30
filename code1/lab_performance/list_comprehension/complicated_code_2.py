import time,sys
def code_0():
    n = []
    l = []
    for x in n:
        l.append(x)
    print("n,l: ",n,l)
def code_1():
    n = list(range(1))
    l = []
    for x in n:
        l.append(x)
    print("n,l: ",n,l)
def code_10():
    n = list(range(10))
    l = []
    for x in n:
        l.append(x)
    print("n,l: ",n,l)
def code_100():
    n = list(range(10)) * 10
    l = []
    for x in n:
        l.append(x)
    print("n,l: ",n,l)
def code_1000():
    iterations=10
    num=10**6
    C={i:i for i in range(num)}
    B={i:i for i in range(num)}
    A_cal=[0 for i in range(5)]
    excluded_colors=[0 for i in range(5)]
    marked=[0 for i in range(5)]
    total_time=0
    for i in range(iterations):
        s_t=time.time()
        next_layer = []
        for i in C.keys():
            if B[i]>0 and i not in A_cal and i not in excluded_colors and i not in marked:
                next_layer.append(i)
        e_t = time.time()
        total_time+=e_t-s_t

    total_time_pythonic = 0
    for i in range(iterations):
        s_t = time.time()
        next_layer=[i for i in C.keys()
     if B[i]>0 and i not in A_cal and i not in excluded_colors and i not in marked]
        e_t = time.time()
        total_time_pythonic += e_t - s_t
    print("ratio: ",total_time,total_time_pythonic,total_time/total_time_pythonic)

    num = 10 ** 5
    iterations=1
    C = {i: i for i in range(num)}
    B = {i: i for i in range(num)}
    A_cal = [i*2 for i in range(num)]
    excluded_colors = [i*2 for i in range(num)]
    marked = [i*2 for i in range(num)]
    total_time = 0
    for i in range(iterations):
        s_t = time.time()
        next_layer = []
        for i in C.keys():
            if B[i] > 0 and i not in A_cal and i not in excluded_colors and i not in marked:
                next_layer.append(i)
        e_t = time.time()
        total_time += e_t - s_t

    total_time_pythonic = 0
    for i in range(iterations):
        s_t = time.time()
        next_layer = [i for i in C.keys()
                      if B[i] > 0 and i not in A_cal and i not in excluded_colors and i not in marked]
        e_t = time.time()
        total_time_pythonic += e_t - s_t
    print("ratio: ", total_time, total_time_pythonic, total_time / total_time_pythonic,len(next_layer))
def code_power():
    p = 10**5
    total_time = 0
    for i in range(iterations):
        s_t = time.time()
        next_layer = []
        for i in range(p// 2 + 1):
            next_layer.append(pow(i,2,p))
        e_t = time.time()
        total_time += e_t - s_t

    total_time_pythonic = 0
    for i in range(iterations):
        s_t = time.time()
        next_layer = {pow(i,2,p) for i in range(p//2+1)}
        e_t = time.time()
        total_time_pythonic += e_t - s_t
    print("ratio: ", total_time, total_time_pythonic, total_time / total_time_pythonic, len(next_layer))


if __name__ == '__main__':
    iterations=10**1
    # code_1000()
    code_power()
    # total_time_list=[]
    # n=[]
    # for i in range(iterations):
    #     start=time.perf_counter()
    #     l=[]
    #     for x in n:
    #         l.append(x)
    #     end = time.perf_counter()
    #     total_time_list.append(end-start)
    # module_name = sys.modules['__main__']
    # func = "code_10"
    # getattr(module_name,func)()

    # code_1000()
    #
    # from operator import methodcaller
    # methodcaller(func)()

