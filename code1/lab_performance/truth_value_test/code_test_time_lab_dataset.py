import dis,time
import lxml
from lxml import html
import numpy as np
def extract_url(xpath_results, base_url):
    print(xpath_results.__class__,type(xpath_results))

    total_time = 0
    for i in range(1000000):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()

        if xpath_results == []:
            pass
        # if inter != 0:
        #     pass
        # if inter != 0.0:
        #     pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time)

    total_time_pythonic = 0
    for i in range(1000000):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        if not xpath_results:
            pass
        # if inter:
        #     pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time_pythonic, total_time / total_time_pythonic)
    lxml.html.HtmlElement().find()
    # if xpath_results == []:
    #     raise ValueError('Empty url resultset')
def fun_html():
    def f(html_str, search_url):
        return extract_url(lxml.html.fromstring(html_str), search_url)


    f('<span id="42">https://example.com</span>', 'http://example.com/')
    f('https://example.com', 'http://example.com/')
    f('//example.com', 'http://example.com/')
    f('//example.com', 'https://example.com/')
    f('/path?a=1', 'https://example.com')

    f('', 'https://example.com')

    extract_url([], 'https://example.com')
def fun_html_2():
    # xpath_results='https://example.com'
    bool(lxml.html.HtmlElement)
    xpath_results=html.fromstring('https://example.com')
    xpath_results
    # bool(xpath_results)
    print(xpath_results,xpath_results.__class__,xpath_results.__bool__)
    total_time = 0
    for i in range(1000000):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        if xpath_results == []:
            pass
        # if inter != 0:
        #     pass
        # if inter != 0.0:
        #     pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time)

    total_time_pythonic = 0
    for i in range(1000000):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        if not xpath_results:
            pass
        # if inter:
        #     pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time_pythonic, total_time / total_time_pythonic)

def fun_len():
    # xpath_results='https://example.com'
    xpath_results="上海"#'https://example.com'#[1]
    total_time = 0
    for i in range(1000000):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        if len(xpath_results) == 0:
            pass
        # if inter != 0:
        #     pass
        # if inter != 0.0:
        #     pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time)

    total_time_pythonic = 0
    for i in range(1000000):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        if not len(xpath_results):
            pass
        # if inter:
        #     pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time_pythonic, total_time / total_time_pythonic)
import numpy as np
def fun_add_op():
    np.ndarray.__lt__
    # xpath_results='https://example.com'
    value = 429496716  # 'https://example.com'#[1]
    total_time = 0
    for i in range(1000000):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        # if value & 4294967168 != 0:
        if value % 2 == 0:
            pass
        # if inter != 0:
        #     pass
        # if inter != 0.0:
        #     pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time)

    total_time_pythonic = 0
    for i in range(1000000):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        # if value & 4294967168:
        if  not value % 2:
            pass
        # if inter:
        #     pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time_pythonic, total_time / total_time_pythonic)
def fun_subscriot():
    graph = {1: {4: 1},2: {2: 2, 3: 2, 4: 2},
    3: {2: 2, 4: 1},4: {1: 1, 2: 2, 3: 1}}
    start = 1
    # graph = {
    #     'A': ['B', 'C', 'E'],
    #     'B': ['A', 'D', 'F'],
    #     'C': ['A', 'G'],
    #     'D': ['B'],
    #     'F': ['B'],
    #     'E': ['A'],
    #     'G': ['C']
    # }
    # start='A'

    total_time = 0
    for i in range(10000000):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        # if graph[start] == []:
        #     pass
        if graph[start] == 0:
            pass
        # if inter != 0:
        #     pass
        # if inter != 0.0:
        #     pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('fun_subscriot func code is finished: ', total_time)

    total_time_pythonic = 0
    for i in range(10000000):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        if not graph[start]:
            pass
        # if inter:
        #     pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time_pythonic, total_time / total_time_pythonic)


def fun_mpint(inter):
    print(inter,inter.__class__,type(inter))
    import time
    total_time = 0
    for i in range(1000000):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        if inter == 0:
            pass
        # if inter != 0:
        #     pass
        # if inter != 0.0:
        #     pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time)

    total_time_pythonic = 0
    for i in range(1000000):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        if not inter:
            pass
        # if inter:
        #     pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time_pythonic, total_time / total_time_pythonic)


def func_a_numpy():
    losses=[-1,1]
    inter = np.mean(losses[:])
    print(inter.__class__,inter.dtype,type(inter))
    # mpints = {int(0): binascii.unhexlify('00000000'),
    #           int(0x9a378f9b2e332a7): binascii.unhexlify('0000000809a378f9b2e332a7'),
    #           int(0x80): binascii.unhexlify('000000020080'), int(-0x1234): binascii.unhexlify('00000002edcc'),
    #           int(-0xdeadbeef): binascii.unhexlify('00000005ff21524111')}
    inter=1
    inter = np.array(inter)
    print(inter.__class__,inter.dtype,type(inter))

    import time
    total_time = 0
    for i in range(1000000):
        if i<3:
            continue
        start_time_zejun = time.perf_counter()
        if inter == 0:
            pass
        # if inter != 0:
        #     pass
        # if inter != 0.0:
        #     pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ',total_time)

    total_time_pythonic = 0
    for i in range(1000000):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        if not inter:
            pass
        # if inter:
        #     pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time_pythonic,total_time/total_time_pythonic)
def fun_1():
    a = 0j
    repeat=10000000
    total_time = 0
    for i in range(repeat):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        if a == 0j:
            pass
        # if inter != 0:
        #     pass
        # if inter != 0.0:
        #     pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time)
    total_time_pythonic = 0

    for i in range(repeat):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        if not a:
            pass

        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time_pythonic, total_time / total_time_pythonic)


if __name__ == '__main__':
    func_a_numpy()
    # fun_len()
    # fun_html_2()
    # fun_subscriot()
    # fun_add_op()
    # fun_html_2()
    fun_html_2()
    fun_len()
    # fun_1()
    # fun_html()
    # fun_subscriot()

    # dis.dis(func_a_numpy)
    # inter = 1
    # inter = np.array(inter)
    # import time
    #
    # total_time = 0
    # for i in range(1000000):
    #     if i < 3:
    #         continue
    #     start_time_zejun = time.perf_counter()
    #     if inter == 0:
    #         pass

    # dis.dis(fun_subscriot)
    # func_a_numpy()
    # fun_mpint(int(0x9a378f9b2e332a7))
    # func_a()
    # dis.dis(func_a)
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