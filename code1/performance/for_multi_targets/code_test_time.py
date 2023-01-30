import dis,inspect
import time,os,re
from shlex import quote
import networkx as nx
all_combo = [
        [
            "test-{title}-{service}-{ext}-{episode}-{id}-{season}-{episodename}",
            {"title": "title", "season": 99, "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "test-title-service-mp4-21-0xdeadface-99-episodename",
        ],
        [
            "test-{title}-{service}-{ext}-{episode}-{id}-{season}-{episodename}",
            {"title": "title", "season": 99, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "test-title-service-mp4-0xdeadface-99-episodename",
        ],
        [
            "test-{title}-{service}-{ext}-{episode}-{id}-{season}-{episodename}",
            {"title": "title", "season": 99, "id": "0xdeadface", "ext": "ext"},
            "test-title-service-mp4-0xdeadface-99",
        ],
        [
            "test-{title}-{service}-{ext}-{episode}-{id}-{season}-{episodename}",
            {"title": "title", "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "test-title-service-mp4-21-0xdeadface-episodename",
        ],
        [
            "test-{title}-{service}-{ext}-{episode}-{id}-{season}-{episodename}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "test-title-service-mp4-0xdeadface-episodename",
        ],
        [
            "test-{title}-{service}-{ext}-{episode}-{id}-{season}-{episodename}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface"},
            "test-title-service-mp4-0xdeadface-episodename",
        ],
        [
            "test-{title}-{episode}-{season}-{service}-{episodename}-{id}-{ext}",
            {"title": "title", "season": 99, "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "test-title-21-99-service-episodename-0xdeadface-mp4",
        ],
        [
            "test-{title}-{episode}-{season}-{service}-{episodename}-{id}-{ext}",
            {"title": "title", "season": 99, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "test-title-99-service-episodename-0xdeadface-mp4",
        ],
        [
            "test-{title}-{episode}-{season}-{service}-{episodename}-{id}-{ext}",
            {"title": "title", "season": 99, "id": "0xdeadface", "ext": "ext"},
            "test-title-99-service-0xdeadface-mp4",
        ],
        [
            "test-{title}-{episode}-{season}-{service}-{episodename}-{id}-{ext}",
            {"title": "title", "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "test-title-21-service-episodename-0xdeadface-mp4",
        ],
        [
            "test-{title}-{episode}-{season}-{service}-{episodename}-{id}-{ext}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "test-title-service-episodename-0xdeadface-mp4",
        ],
        [
            "test-{title}-{episode}-{season}-{service}-{episodename}-{id}-{ext}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface"},
            "test-title-service-episodename-0xdeadface-mp4",
        ],
        [
            "{id}-{season}-{ext}-{episode}-{episodename}-{title}-{service}",
            {"title": "title", "season": 99, "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "0xdeadface-99-mp4-21-episodename-title-service",
        ],
        [
            "{id}-{season}-{ext}-{episode}-{episodename}-{title}-{service}",
            {"title": "title", "season": 99, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "0xdeadface-99-mp4-episodename-title-service",
        ],
        [
            "{id}-{season}-{ext}-{episode}-{episodename}-{title}-{service}",
            {"title": "title", "season": 99, "id": "0xdeadface", "ext": "ext"},
            "0xdeadface-99-mp4-title-service",
        ],
        [
            "{id}-{season}-{ext}-{episode}-{episodename}-{title}-{service}",
            {"title": "title", "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "0xdeadface-mp4-21-episodename-title-service",
        ],
        [
            "{id}-{season}-{ext}-{episode}-{episodename}-{title}-{service}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "0xdeadface-mp4-episodename-title-service",
        ],
        [
            "{id}-{season}-{ext}-{episode}-{episodename}-{title}-{service}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface"},
            "0xdeadface-mp4-episodename-title-service",
        ],
        [
            "{service}-{ext}-{season}-{id}-{title}-{episodename}-{episode}",
            {"title": "title", "season": 99, "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "service-mp4-99-0xdeadface-title-episodename-21",
        ],
        [
            "{service}-{ext}-{season}-{id}-{title}-{episodename}-{episode}",
            {"title": "title", "season": 99, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "service-mp4-99-0xdeadface-title-episodename",
        ],
        [
            "{service}-{ext}-{season}-{id}-{title}-{episodename}-{episode}",
            {"title": "title", "season": 99, "id": "0xdeadface", "ext": "ext"},
            "service-mp4-99-0xdeadface-title",
        ],
        [
            "{service}-{ext}-{season}-{id}-{title}-{episodename}-{episode}",
            {"title": "title", "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "service-mp4-0xdeadface-title-episodename-21",
        ],
        [
            "{service}-{ext}-{season}-{id}-{title}-{episodename}-{episode}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "service-mp4-0xdeadface-title-episodename",
        ],
        [
            "{service}-{ext}-{season}-{id}-{title}-{episodename}-{episode}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface"},
            "service-mp4-0xdeadface-title-episodename",
        ],
        [
            "test-{title}-{service}-{ext}-{episode}-{id}-{season}",
            {"title": "title", "season": 99, "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "test-title-service-mp4-21-0xdeadface-99",
        ],
        [
            "test-{title}-{service}-{ext}-{episode}-{id}-{season}",
            {"title": "title", "season": 99, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "test-title-service-mp4-0xdeadface-99",
        ],
        [
            "test-{title}-{service}-{ext}-{episode}-{id}-{season}",
            {"title": "title", "season": 99, "id": "0xdeadface", "ext": "ext"},
            "test-title-service-mp4-0xdeadface-99",
        ],
        [
            "test-{title}-{service}-{ext}-{episode}-{id}-{season}",
            {"title": "title", "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "test-title-service-mp4-21-0xdeadface",
        ],
        [
            "test-{title}-{service}-{ext}-{episode}-{id}-{season}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "test-title-service-mp4-0xdeadface",
        ],
        [
            "test-{title}-{service}-{ext}-{episode}-{id}-{season}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface"},
            "test-title-service-mp4-0xdeadface",
        ],
        [
            "{title}-{ext}-{episode}-{id}-{season}",
            {"title": "title", "season": 99, "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "title-mp4-21-0xdeadface-99",
        ],
        [
            "{title}-{ext}-{episode}-{id}-{season}",
            {"title": "title", "season": 99, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "title-mp4-0xdeadface-99",
        ],
        ["{title}-{ext}-{episode}-{id}-{season}", {"title": "title", "season": 99, "id": "0xdeadface", "ext": "ext"}, "title-mp4-0xdeadface-99"],
        [
            "{title}-{ext}-{episode}-{id}-{season}",
            {"title": "title", "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "title-mp4-21-0xdeadface",
        ],
        [
            "{title}-{ext}-{episode}-{id}-{season}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "title-mp4-0xdeadface",
        ],
        ["{title}-{ext}-{episode}-{id}-{season}", {"title": "title", "episodename": "episodename", "id": "0xdeadface"}, "title-mp4-0xdeadface"],
        [
            "{title}-{ext}.{episode}-{id}.{season}",
            {"title": "title", "season": 99, "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "title-mp4.21-0xdeadface.99",
        ],
        [
            "{title}-{ext}.{episode}-{id}.{season}",
            {"title": "title", "season": 99, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "title-mp4-0xdeadface.99",
        ],
        ["{title}-{ext}.{episode}-{id}.{season}", {"title": "title", "season": 99, "id": "0xdeadface", "ext": "ext"}, "title-mp4-0xdeadface.99"],
        [
            "{title}-{ext}.{episode}-{id}.{season}",
            {"title": "title", "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "title-mp4.21-0xdeadface",
        ],
        [
            "{title}-{ext}.{episode}-{id}.{season}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "title-mp4-0xdeadface",
        ],
        ["{title}-{ext}.{episode}-{id}.{season}", {"title": "title", "episodename": "episodename", "id": "0xdeadface"}, "title-mp4-0xdeadface"],
        [
            "{id}-{season}{ext}-{episode}{episodename}-{title}-{service}",
            {"title": "title", "season": 99, "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "0xdeadface-99mp4-21episodename-title-service",
        ],
        [
            "{id}-{season}{ext}-{episode}{episodename}-{title}-{service}",
            {"title": "title", "season": 99, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "0xdeadface-99mp4episodename-title-service",
        ],
        [
            "{id}-{season}{ext}-{episode}{episodename}-{title}-{service}",
            {"title": "title", "season": 99, "id": "0xdeadface", "ext": "ext"},
            "0xdeadface-99mp4-title-service",
        ],
        [
            "{id}-{season}{ext}-{episode}{episodename}-{title}-{service}",
            {"title": "title", "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "0xdeadfacemp4-21episodename-title-service",
        ],
        [
            "{id}-{season}{ext}-{episode}{episodename}-{title}-{service}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "0xdeadfacemp4episodename-title-service",
        ],
        [
            "{id}-{season}{ext}-{episode}{episodename}-{title}-{service}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface"},
            "0xdeadfacemp4episodename-title-service",
        ],
        [
            "{episodename}a{title}-{service}",
            {"title": "title", "season": 99, "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "episodenameatitle-service",
        ],
        [
            "{episodename}a{title}-{service}",
            {"title": "title", "season": 99, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "episodenameatitle-service",
        ],
        ["{episodename}a{title}-{service}", {"title": "title", "season": 99, "id": "0xdeadface", "ext": "ext"}, "atitle-service"],
        [
            "{episodename}a{title}-{service}",
            {"title": "title", "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "episodenameatitle-service",
        ],
        [
            "{episodename}a{title}-{service}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "episodenameatitle-service",
        ],
        ["{episodename}a{title}-{service}", {"title": "title", "episodename": "episodename", "id": "0xdeadface"}, "episodenameatitle-service"],
        [
            "{title}.{episode}.{episodename}-{id}-{service}.{ext}",
            {"title": "title", "season": 99, "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "title.21.episodename-0xdeadface-service.mp4",
        ],
        [
            "{title}.{episode}.{episodename}-{id}-{service}.{ext}",
            {"title": "title", "season": 99, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "title.episodename-0xdeadface-service.mp4",
        ],
        [
            "{title}.{episode}.{episodename}-{id}-{service}.{ext}",
            {"title": "title", "season": 99, "id": "0xdeadface", "ext": "ext"},
            "title-0xdeadface-service.mp4",
        ],
        [
            "{title}.{episode}.{episodename}-{id}-{service}.{ext}",
            {"title": "title", "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "title.21.episodename-0xdeadface-service.mp4",
        ],
        [
            "{title}.{episode}.{episodename}-{id}-{service}.{ext}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "title.episodename-0xdeadface-service.mp4",
        ],
        [
            "{title}.{episode}.{episodename}-{id}-{service}.{ext}",
            {"title": "title", "episodename": "episodename", "id": "0xdeadface"},
            "title.episodename-0xdeadface-service.mp4",
        ],
        [
            "{title}.s{season}e{episode}.{episodename}-{id}-{service}.{ext}",
            {"title": "title", "season": 99, "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "title.s99e21.episodename-0xdeadface-service.mp4",
        ],
        [
            "{title}.s{season}e{episode}.{episodename}-{id}-{service}.{ext}",
            {"title": "title", "season": 99, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
            "title.s99.episodename-0xdeadface-service.mp4",
        ],
    ]
def func_c():
    repeat=10**7
    dot_path_pairs = []
    installed_dotfile_path = quote(os.path.join("~", "shallow-backup/dotfiles"))
    backup_dotfile_path = quote(os.path.join("~", "shallow-backup/dotfiles"))
    print(installed_dotfile_path.__class__)
    dot_path_pairs.append((installed_dotfile_path, backup_dotfile_path))
    dotfolders_mp_in = []
    dotfiles_mp_in = []
    print("dot_path_pairs: ",dot_path_pairs)
    for path_pair in dot_path_pairs:
        installed_path = path_pair[0]
        if os.path.isdir(installed_path):
            print(path_pair.__class__)
            dotfolders_mp_in.append(path_pair)
        else:
            print(path_pair.__class__,path_pair)
            dotfiles_mp_in.append(path_pair)
            dotfolders_mp_in.append(path_pair)

    print("dotfolders_mp_in",dotfolders_mp_in)
    total_time = 0
    for i in range(repeat):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        for x in dotfolders_mp_in:
            x[0]
            x[1]
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time,dotfolders_mp_in)
    total_time_pythonic = 0
    for i in range(repeat):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        for  (x_0, x_1, *x_len)  in dotfolders_mp_in:
            x_0
            x_1
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time_pythonic, total_time,total_time / total_time_pythonic)
    # inspect.getmembers()

def func_a():


    a={'series': [{
            'columns': ['key'],
            'values': [['cpu'], ['memory'], ['iops'], ['network']]
        }]}


    total_time = 0
    for i in range(10**4):
        if i<3:
            continue
        start_time_zejun = time.perf_counter()
        for item in a.items():
            item[0]
            item[1]
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ',total_time)

    total_time_pythonic = 0
    for i in range(10 ** 4):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        for (item_0, item_1, *item_len)  in a.items():
            item_0
            item_1
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time_pythonic,total_time,total_time/total_time_pythonic)
def func_b():
    repeat=10**7
    input_seq=[[j for j in range(3)] for i in range(1)]


    total_time = 0
    for i in range(repeat):
        if i<3:
            continue
        start_time_zejun = time.perf_counter()
        for e in input_seq:
            e[0]
            e[1]

        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ',total_time)

    total_time_pythonic = 0
    for i in range(repeat):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        for (e_0, e_1, *e_len) in input_seq:
            e_0
            e_1
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time_pythonic,total_time,total_time/total_time_pythonic)

def func_b_2():
    repeat=10**7
    input_seq=[[j for j in range(2)] for i in range(1)]


    total_time = 0
    for i in range(repeat):
        if i<3:
            continue
        start_time_zejun = time.perf_counter()
        for e in input_seq:
            e[0]
            e[1]

        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ',total_time)

    total_time_pythonic = 0
    for i in range(repeat):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        for (e_0, e_1, *e_len) in input_seq:
            e_0
            e_1
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time_pythonic,total_time,total_time/total_time_pythonic)
def func_b_3():
    repeat=10**7
    input_seq=[(1,2) for i in range(1)]

    def one_fun(s):
        return "'" + s.replace("'", "'\"'\"'") + "'"

    # new_s=quote(os.path.join("~", "shallow-backup/dotfiles"))
    # new_s_1 = quote(os.path.join("~", "shallow-backup/dotfiles"))
    # input_seq_1=[]
    # input_seq_1.append((new_s,new_s_1))
    # input_seq=[]
    # for e in input_seq_1:
    #     input_seq.append(e)
    print(input_seq)
    print("is generator: ",iter(input_seq))
    total_time = 0
    for i in range(repeat):
        if i<3:
            continue
        start_time_zejun = time.perf_counter()
        for e in input_seq:
            e[0]
            # e[1]

        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ',total_time)

    total_time_pythonic = 0
    for i in range(repeat):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        for (e_0, *e_len) in input_seq:
            e_0
            # e_1
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time_pythonic,total_time,total_time/total_time_pythonic)
def func_w():
    repeat=10**5
    G = nx.LFR_benchmark_graph(
        250, 3, 1.5, 0.009, average_degree=5, min_community=20, seed=10
    )
    w=G.edges()
    k=list(w)
    start_time_zejun = time.perf_counter()
    for i in range(repeat):
        for e in w:
            e
    end_time_zejun = time.perf_counter()
    print("total time: ",end_time_zejun-start_time_zejun)

    # print('xxxx',w)
    start_time_zejun = time.perf_counter()
    for i in range(repeat):
        for e in k:
            e
    end_time_zejun = time.perf_counter()
    print("total time: ", end_time_zejun - start_time_zejun)

    print(G.edges().__class__,iter(G.edges()))
    print(isinstance(G.edges(),Iterable))
    print(isinstance(iter(G.edges()), Iterator))
from sympy.core.singleton import S
def SumQ(expr):
    return expr.is_Add
def ProductQ(expr):
    return S(expr).is_Mul
def Sort(u, r=False):
    return sorted(u, key=lambda x: x.sort_key(), reverse=r)
def Rest(expr):

    if isinstance(expr, list):
        return expr[1:]
    else:
        if SumQ(expr) or ProductQ(expr):
            l = Sort(expr.args)
            return expr.func(*l[1:])
        else:
            return expr.args[1]
from sympy.integrals.rubi.utility_function import MonomialFactor
from sympy.core.symbol import (symbols, Symbol, Wild)
def Smallest(num1, num2=None):
    A, B, a, b, c, d, e, f, g, h, y, z, m, n, p, q, u, v, w, F = symbols('A B a b c d e f g h y z m n p q u v w F',
                                                                         real=True, imaginary=False)
    x = Symbol('x')
    MonomialFactor(a, x)
    if num2 is None:
        lst = num1
        num = lst[0]
        for i in Rest(lst):
            num = Smallest(num, i)
        return num
    # return Min(num1, num2)
def func_rest():
    pass
def func_inspect():
    # =SomeVariables(), SomeActions()
    from inspect import operators
    actions_data = actions.get_all_actions()
    variables_data = variables.get_all_variables()
    variable_type_operators = {}
    for variable_class in inspect.getmembers(operators, lambda x: getattr(x, 'export_in_rule_data', False)):
        variable_type = variable_class[1]  # getmembers returns (name, value)
        variable_type_operators[variable_type.name] = variable_type.get_all_operators()
from svtplay_dl.service import Service
from svtplay_dl.utils.parser import setup_defaults
from svtplay_dl.utils.text import filenamify
def _formatname(output, config):
    name = config.get("filename")
    for key in output:
        if key == "title" and output[key]:
            name = name.replace("{title}", filenamify(output[key]))
        if key == "season" and output[key]:
            number = f"{int(output[key]):02d}"
            name = name.replace("{season}", number)
        if key == "episode" and output[key]:
            number = f"{int(output[key]):02d}"
            name = name.replace("{episode}", number)
        if key == "episodename" and output[key]:
            name = name.replace("{episodename}", filenamify(output[key]))
        if key == "id" and output[key]:
            name = name.replace("{id}", output[key])
        if key == "service" and output[key]:
            name = name.replace("{service}", output[key])
        if key == "ext" and output[key]:
            name = name.replace("{ext}", output[key])
    repeat=10**5
    total_time_pythonic = 0
    print(re.findall(r"([\.\-]?(([^\.\-]+\w+)?\{[\w\-]+\}))", name))
    for i in range(repeat):
        # Remove all {text} we cant replace with something
        start_time_zejun = time.perf_counter()
        for item_0,*other in re.findall(r"([\.\-]?(([^\.\-]+\w+)?\{[\w\-]+\}))", name)*100:
            item_0
            # print(item)
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
    print("name: ",name)
    total_time=0
    for i in range(repeat):
    # Remove all {text} we cant replace with something
        start_time_zejun = time.perf_counter()
        for item in re.findall(r"([\.\-]?(([^\.\-]+\w+)?\{[\w\-]+\}))", name)*100:
            item[0]
            # print(item)
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
    # print('\n*********zejun test total time************** ', total_time_zejun)
    print('func code is finished: ', total_time_pythonic, total_time, total_time / total_time_pythonic)

    # if "season" in output and output["season"] and re.search(r"(e\{[\w\-]+\})", name):
        #     name = name.replace(re.search(r"(e\{[\w\-]+\})", name).group(1), "")
        # else:
        #     name = name.replace(item[0], "")

    return name

def func_re():
    item=[
        "test-{title}-{service}-{ext}-{episode}-{id}-{season}-{episodename}",
        {"title": "title", "season": 99, "episode": 21, "episodename": "episodename", "id": "0xdeadface", "ext": "ext"},
        "test-title-service-mp4-21-0xdeadface-99-episodename",
    ]
    item=all_combo[41]
    config = setup_defaults()
    config.set("filename", item[0])
    service = Service(config, "localhost")
    service.output.update(item[1])
    service.output["ext"] = "mp4"
    _formatname(service.output, config)
    # for item in re.findall(r"([\.\-]?(([^\.\-]+\w+)?\{[\w\-]+\}))", name):
    #     item[0]
if __name__ == '__main__':
    from collections.abc import *
    import ast
    var=[[1]]
    print_len_stmt = f"try:\n    print('len: ',len({var}[0]))\nexcept:\n    print('len: ',0)"
    print(print_len_stmt)
    for e in ast.walk(ast.parse(print_len_stmt)):
        if isinstance(e, ast.stmt):
            print_len_stmt_node = e
            break
    # func_b()
    # func_b_3()
    # func_re()
    # all_data = export_rule_data(SomeVariables(), SomeActions())
    # func_w()
    # func_b_3()
    # dis.dis(func_w)
    func_c()
    # func_b_2()
    # func_b_3()
