import dis
import time


def f1():
    x_0=[i for i in range(4)]
    l=set()
    for e_0 in x_0:
        for e_0 in x_0:
            if e_0 % 2:
                l.add(e_0)
            else:
                l.add(e_0)
def f2():
    x_0=[i for i in range(4)]
    l=[e_0 if e_0 % 2 else e_0 for e_0 in x_0 ]
def f_if():
    x_0=[i for i in range(4)]
    l=set()
    for e_0 in x_0:
        if e_0 % 2:
            l.add(e_0)
def f_if_tuple_1():
    x_0=[i for i in range(4)]
    x_1 = [i for i in range(4)]

    l=[]
    for e_0 in x_0:
        for e_1 in x_1:
            # if e_0 % 2:
            #     l.add((e_0,))
                l.add((e_0,))
def f_if_tuple():
    x_0=[i for i in range(4)]
    x_1 = [i for i in range(4)]
    l=set()
    for e_0 in x_0:
        for e_1 in x_1:
            # if e_0 % 2:
                l.add((e_0,e_1))
def f_if_tuple_Complicated():
    x_0=[i for i in range(4)]
    x_1 = [i for i in range(4)]
    l=set()
    for e_0 in x_0:
        l.add((e_0,e_0))
def f_if_tuple_simple():
    x_0=[i for i in range(4)]
    x_1 = [i for i in range(4)]
    l= {(e_0,e_0) for e_0 in x_0}
    # for e_0 in x_0:
    #     for e_1 in x_1:
    #         # if e_0 % 2:
    #             l.add((e_0,e_1))

#     a = [1, 2, 3, 4]
#     l = [i for i in a]
#
# print(dis.dis(f1) )
# print(dis.dis(f2) )
def func_set_compre_complicate_nest():
    a = set([])
    for e_0 in input_list:
        a.add((e_0, e_0, e_0, e_0))
def func_set_compre_nest():
    a = {(e_0, e_0, e_0, e_0) for e_0 in input_list}
def func_complicated_time():
    input_list = list(range(10 ** 6))
    start = time.time()
    a = set()
    for e_0 in input_list:
        a.add((e_0,))
    end = time.time()
    print("complicated code total_time: ", end - start)

def func_simple_time():
    input_list = list(range(10 ** 6))
    start = time.time()
    a = {(e_0,) for e_0 in input_list}
    end = time.time()
    print("simple code total_time: ", end - start)
def func_complicated_time_4():
    input_list = list(range(10 ** 6))
    total_time=0
    for i in range(100):
        start = time.time()
        a = set()
        for e_0 in input_list:
            a.add((e_0, e_0, e_0, e_0))
        end = time.time()
        total_time+=end - start
    print("complicated code total_time: ", total_time)

def func_simple_time_4_basic_ele():
    input_list = list(range(10 ** 6))
    total_time = 0
    for i in range(100):
        start = time.time()
        a = {e_0 for e_0 in input_list}
        end = time.time()
        total_time += end - start
    print("simple code total_time: ", total_time)
def func_complicated_time_4_basic_ele():
    input_list = list(range(10 ** 6))
    total_time=0
    for i in range(100):
        start = time.time()
        a = set()
        for e_0 in input_list:
            a.add(e_0)
        end = time.time()
        total_time+=end - start
    print("complicated code total_time: ", total_time)

def func_simple_time_4():
    input_list = list(range(10 ** 6))
    total_time = 0
    for i in range(100):
        start = time.time()
        a = {(e_0, e_0, e_0, e_0) for e_0 in input_list}
        end = time.time()
        total_time += end - start
    print("simple code total_time: ", total_time)
if __name__ == '__main__':
    '''
    func_simple_time_4_basic_ele()
    func_complicated_time_4_basic_ele()
    func_complicated_time()
    func_simple_time()
    func_complicated_time_4()
    func_simple_time_4()
    '''
    # dis.dis(f_if)
    # dis.dis(f1)

    # dis.dis(f_if_tuple_1)
    # dis.dis(f_if_tuple_Complicated)
    # func_simple_time_4
    dis.dis(f_if_tuple_simple)
    input_list = list(range(10 ** 6))
    total_time = 0
    for i in range(100):
        start = time.time()
        a = set()
        for e_0 in input_list:
            a.add(e_0)
        end = time.time()
        total_time += end - start
    print("e_0 complicated code total_time: ", total_time)

    input_list = list(range(10 ** 6))
    total_time = 0
    for i in range(100):
        start = time.time()
        a = {e_0 for e_0 in input_list}
        end = time.time()
        total_time += end - start
    print("e_0 simple code total_time: ", total_time)
    input_list = list(range(10 ** 6))
    total_time = 0
    for i in range(10):
        start = time.time()
        a = set()
        for e_0 in input_list:
            a.add(f"{e_0}{e_0}{e_0}{e_0}")
        end = time.time()
        total_time += end - start
    print("{e_0}{e_0}{e_0}{e_0}complicated code total_time: ", total_time)

    input_list = list(range(10 ** 6))
    total_time = 0
    for i in range(10):
        start = time.time()
        a = {f"{e_0}{e_0}{e_0}{e_0}" for e_0 in input_list}
        end = time.time()
        total_time += end - start
    print("{e_0}{e_0}{e_0}{e_0}simple code total_time: ", total_time)
    # input_list = list(range(10 ** 6))
    # total_time = 0
    # for i in range(10):
    #     start = time.time()
    #     a = set()
    #     for e_0 in input_list:
    #         a.add(e_0 << 3 + e_0 << 2 + e_0 << 1 + e_0)
    #     end = time.time()
    #     total_time += end - start
    # print("complicated code total_time: ", total_time)
    #
    # input_list = list(range(10 ** 6))
    # total_time = 0
    # for i in range(10):
    #     start = time.time()
    #     a = {e_0 << 3 + e_0 << 2 + e_0 << 1 + e_0 for e_0 in input_list}
    #     end = time.time()
    #     total_time += end - start
    # print("simple code total_time: ", total_time)

    input_list = list(range(10 ** 6))
    total_time = 0
    for i in range(100):
        start = time.time()
        a = set()
        for e_0 in input_list:
            a.add(e_0*1000000+e_0*100000+e_0*10000+e_0)
        end = time.time()
        total_time += end - start
    print("e_0*1000000+e_0*100000+e_0*10000+e_0complicated code total_time: ", total_time)

    input_list = list(range(10 ** 6))
    total_time = 0
    for i in range(100):
        start = time.time()
        a = {e_0*1000000+e_0*100000+e_0*10000+e_0 for e_0 in input_list}
        end = time.time()
        total_time += end - start
    print("e_0*1000+e_0*100+e_0*10+e_0simple code total_time: ", total_time)

    input_list = list(range(10 ** 6))

    total_time = 0
    for i in range(100):
        start = time.time()
        a = set()
        for e_0 in input_list:
            a.add((e_0,))
        end = time.time()
        total_time += end - start
    print("complicated code total_time: ", total_time)

    input_list = list(range(10 ** 6))
    total_time = 0
    for i in range(100):
        start = time.time()
        a = {(e_0,) for e_0 in input_list}
        end = time.time()
        total_time += end - start
    print("simple code total_time: ",total_time)

    input_list = list(range(10 ** 6))
    total_time = 0
    for i in range(100):
        start = time.time()
        a = set()
        for e_0 in input_list:
            a.add((e_0, e_0, e_0, e_0))
        end = time.time()
        total_time += end - start
    print("complicated code total_time: ", total_time)

    input_list = list(range(10 ** 6))
    total_time = 0
    for i in range(100):
        start = time.time()
        a = {(e_0, e_0, e_0, e_0) for e_0 in input_list}
        end = time.time()
        total_time += end - start
    print("simple code total_time: ", total_time)



    '''
    dis.dis(func_set_compre_nest)
    dis.dis(func_set_compre_complicate_nest)
    input_list=list(range(10 ** 6))
    start = time.time()
    a = set()
    for e_0 in input_list:
        a.add(e_0)
    end = time.time()
    print("total_time: ",end-start)

    start = time.time()
    a = {e_0 for e_0 in input_list}
    end = time.time()
    print("total_time: ", end - start)
    input_list = list(range(10 ** 6))
    start = time.time()
    a = set()
    for e_0 in input_list:
        a.add((e_0,))
    end = time.time()
    print("complicated code total_time: ", end - start)

    start = time.time()
    a = {(e_0,) for e_0 in input_list}
    end = time.time()
    print("simple code total_time: ", end - start)
    
    start = time.time()
    a = set([])
    for e_0 in input_list:
        a.add((e_0, e_0, e_0, e_0))
    end = time.time()
    print("total_time: ", end - start, len(a))

    start = time.time()
    a = {(e_0, e_0, e_0, e_0) for e_0 in input_list}
    end = time.time()
    print("total_time: ", end - start, len(a))
    
    start = time.time()
    a = []
    for e_0 in input_list:
        a.append((e_0, e_0, e_0, e_0))
    end = time.time()
    print("list complicated code total_time: ", end - start)

    start = time.time()
    a = [(e_0, e_0, e_0, e_0) for e_0 in input_list]
    end = time.time()
    print("list simple code total_time: ", end - start)
    '''


    #'''
    # dis.dis(f_if_tuple)
    # dis.dis(f2)
    # a = [1, 2, 3, 4]
    # l = []
    # for i in a:
    #     l.append(i)
    # a = [1, 2, 3, 4]
    # l = [i for i in a]
