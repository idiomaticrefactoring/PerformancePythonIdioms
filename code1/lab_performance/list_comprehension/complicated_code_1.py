import ast
import time,sys
import inspect
from inspect import getmembers, isfunction

class ListComprehensions():
    def __init__(self,iterations=10):
        self.iterations=iterations
    def get_all_instances(self):
        functions_list = [o for o in getmembers(ListComprehensions) if isfunction(o[1]) and o[0].startswith("code_")]

        print("functions_list: ",functions_list)

        for name,value in functions_list:
            value(self)
        return functions_list
    # 1 for
    def code_0(self):
        n_list=[[],list(range(1,2)),list(range(1,11)),list(range(1,11)) * 10,list(range(1,11)) * 100]
        all_total_time_list=[]
        all_total_idiomatic_time_list=[]
        for n in n_list:

            total_time_list=[]
            total_idiomatic_time_list = []
            for _ in range(self.iterations):
                start=time.perf_counter()
                l = []
                for x in n:
                    l.append(x)
                end = time.perf_counter()
                total_time_list.append(end-start)
                start = time.perf_counter()
                l = [x for x in n]
                end = time.perf_counter()
                total_idiomatic_time_list.append(end - start)
            all_total_time_list.append(total_time_list)
            all_total_idiomatic_time_list.append(total_idiomatic_time_list)
            # print("n,l: ", n, l)
        print(inspect.currentframe().f_code.co_name,len(l))
        return all_total_time_list,all_total_idiomatic_time_list
    # 1 for 1 if
    def code_1(self):
        n_list=[[],list(range(1,2)),list(range(1,11)),list(range(1,11)) * 10,list(range(1,11)) * 100]
        # n_list = [[], list(range(1)), list(range(10)), list(range(10)) * 10, list(range(10)) * 100]
        all_total_time_list = []
        all_total_idiomatic_time_list = []
        for n in n_list:

            total_time_list = []
            total_idiomatic_time_list = []
            for _ in range(self.iterations):
                start = time.perf_counter()
                l = []
                for x in n:
                    if x:
                        l.append(x)
                end = time.perf_counter()
                total_time_list.append(end - start)
                start = time.perf_counter()
                l = [x for x in n if x]
                end = time.perf_counter()
                total_idiomatic_time_list.append(end - start)
            all_total_time_list.append(total_time_list)
            all_total_idiomatic_time_list.append(total_idiomatic_time_list)
            # print("n,l: ", n, l)
        print(inspect.currentframe().f_code.co_name,len(l))
        return all_total_time_list, all_total_idiomatic_time_list
    ## 2 for
    def code_2(self):
        n_list=[[],list(range(1,2)),list(range(1,11)),list(range(1,11)) * 10,list(range(1,11)) * 100]
        m_list=[[],list(range(1,2)),list(range(1,11)),list(range(1,11)) * 10,list(range(1,11)) * 100]
        # n_list = [[], list(range(1)), list(range(10)), list(range(10)) * 10, list(range(10)) * 100]
        # m_list = [[], list(range(1)), list(range(10)), list(range(10)) * 10, list(range(10)) * 100]
        all_total_time_list = []
        all_total_idiomatic_time_list = []
        for ind,n in enumerate(n_list):
            m=m_list[ind]

            total_time_list = []
            total_idiomatic_time_list = []
            for _ in range(self.iterations):
                start = time.perf_counter()
                l = []
                for x in n:
                    for y in m:
                        l.append(x)
                end = time.perf_counter()
                total_time_list.append(end - start)
                start = time.perf_counter()
                l = [x for x in n for y in m]
                end = time.perf_counter()
                total_idiomatic_time_list.append(end - start)
            all_total_time_list.append(total_time_list)
            all_total_idiomatic_time_list.append(total_idiomatic_time_list)
            # print("n,l: ", n, l)
        print(inspect.currentframe().f_code.co_name,len(l))
        return all_total_time_list, all_total_idiomatic_time_list
    # 2 for 1 if
    def code_3(self):
        n_list = [[], list(range(1, 2)), list(range(1, 11)), list(range(1, 11)) * 10, list(range(1, 11)) * 100]
        m_list = [[], list(range(1, 2)), list(range(1, 11)), list(range(1, 11)) * 10, list(range(1, 11)) * 100]
        # n_list = [[], list(range(1)), list(range(10)), list(range(10)) * 10, list(range(10)) * 100]
        # m_list = [[], list(range(1)), list(range(10)), list(range(10)) * 10, list(range(10)) * 100]
        all_total_time_list = []
        all_total_idiomatic_time_list = []
        for ind, n in enumerate(n_list):
            m = m_list[ind]

            total_time_list = []
            total_idiomatic_time_list = []
            for _ in range(self.iterations):
                start = time.perf_counter()
                l = []
                for x in n:
                    for y in m:
                        if x:
                            l.append(x)
                end = time.perf_counter()
                total_time_list.append(end - start)
                start = time.perf_counter()
                l = [x for x in n for y in m if x]
                end = time.perf_counter()
                total_idiomatic_time_list.append(end - start)
            all_total_time_list.append(total_time_list)
            all_total_idiomatic_time_list.append(total_idiomatic_time_list)
            # print("n,l: ", n, l)
        print(inspect.currentframe().f_code.co_name,len(l))
        return all_total_time_list, all_total_idiomatic_time_list
    #3 for
    def code_4(self):
        n_list = [[], list(range(1, 2)), list(range(1, 11)), list(range(1, 11)) * 10, list(range(1, 11)) * 100]
        all_total_time_list = []
        all_total_idiomatic_time_list = []
        for ind, n in enumerate(n_list):

            total_time_list = []
            total_idiomatic_time_list = []
            for _ in range(self.iterations):
                start = time.perf_counter()
                l = []
                for x in n:
                    for y in n:
                        for z in n:
                            l.append(x)
                end = time.perf_counter()
                total_time_list.append(end - start)
                start = time.perf_counter()
                l = [x for x in n for y in n for z in n]
                end = time.perf_counter()
                total_idiomatic_time_list.append(end - start)
            all_total_time_list.append(total_time_list)
            all_total_idiomatic_time_list.append(total_idiomatic_time_list)
            # print("n,l: ", n, l)
        print(inspect.currentframe().f_code.co_name,len(l))
        return all_total_time_list, all_total_idiomatic_time_list

    # 3 for
    def code_4(self):
        n_list = [[], list(range(1, 2)), list(range(1, 11)), list(range(1, 11)) * 10, list(range(1, 11)) * 100]
        all_total_time_list = []
        all_total_idiomatic_time_list = []
        for ind, n in enumerate(n_list):

            total_time_list = []
            total_idiomatic_time_list = []
            for _ in range(self.iterations):
                start = time.perf_counter()
                l = []
                for x in n:
                    for y in n:
                        for z in n:
                            if x:
                                l.append(x)
                end = time.perf_counter()
                total_time_list.append(end - start)
                start = time.perf_counter()
                l = [x for x in n for y in n for z in n if x]
                end = time.perf_counter()
                total_idiomatic_time_list.append(end - start)
            all_total_time_list.append(total_time_list)
            all_total_idiomatic_time_list.append(total_idiomatic_time_list)
            # print("n,l: ", n, l)
        print(inspect.currentframe().f_code.co_name, len(l))
        return all_total_time_list, all_total_idiomatic_time_list

if __name__ == '__main__':
    slc=ListComprehensions()
    # print(dir(slc))
    slc.get_all_instances()
    iterations=10
    total_time_list=[]
    n=[]
    for i in range(iterations):
        start=time.perf_counter()
        l=[]
        for x in n:
            l.append(x)
        end = time.perf_counter()
        total_time_list.append(end-start)
    module_name = sys.modules['__main__']
    func = "code_10"
    # getattr(module_name,func)()
    #
    # from operator import methodcaller
    # methodcaller(func)()

