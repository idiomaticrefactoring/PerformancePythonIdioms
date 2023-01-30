import time
def func_a():
    repeat=10**6
    x_0 = list(range(1,1000001))
    x_0 = list(range(1, 101))
    x_1 = list(range(1, 101))
    x_2 = list(range(1, 101))
    x_0 = list(range(1, 101))

    # x_0 = list(range(1, 1000001))
    # x_0 = [0 for i in list(range(1, 1000001))]
    total_time = 0
    for i in range(repeat):
        time_s = time.time()
        # l = set()
        # for e_0 in x_0:
        #     if e_0 // 1:
        #         l.add(e_0)
        l = dict()
        for e_0 in x_0:
            l[e_0] = e_0

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
        # l = {
        #     e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2
        #     for e_0 in x_0 for e_1 in x_1 for e_2 in x_2}
        l = {e_0: e_0 for e_0 in x_0}
        time_e = time.time()
        if i < 3:
            continue
        total_time_pythonic += time_e - time_s

    print('code is finished', total_time_pythonic, total_time, total_time / total_time_pythonic)
def func_len(in_degrees = [0, 1, 1, 2]):

    repeat = 10 ** 6
    h_degree_nodelist_in = {}
    for idx, i in enumerate(in_degrees):
        idx = int(idx)
        if i > 0:
            h_degree_nodelist_in.setdefault(i, [])
            h_degree_nodelist_in[i].append(idx)
    print("h_degree_nodelist_in:",h_degree_nodelist_in)
    total_time = 0
    for i in range(repeat):
        if i < 3:
            continue
        time_s = time.time()
        nk_in = {}
        for p in h_degree_nodelist_in:
            nk_in[p] = len(h_degree_nodelist_in[p])

        time_e = time.time()
        total_time += time_e - time_s
    print(nk_in)
    total_time_pythonic = 0
    for i in range(repeat):

        time_s = time.time()
        # l = {e_0 for e_0 in x_0}
        # l = {e_0 for e_0 in x_0 if e_0 // 1}
        # l = {
        #     e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2
        #     for e_0 in x_0 for e_1 in x_1 for e_2 in x_2}
        # l = {e_0: len(x_0[e_0]) for e_0 in x_0}
        nk_in = {p:len(h_degree_nodelist_in[p]) for p in h_degree_nodelist_in}
        time_e = time.time()
        if i < 3:
            continue
        total_time_pythonic += time_e - time_s

    print('code is finished', total_time_pythonic, total_time, total_time / total_time_pythonic)
def read_index(f):
    for i in f:
        yield i
def func_generator():

    repeat = 10 ** 6
    x_0 = [(i,i) for i in list(range(1, 101))]
    x_0 = [(i,i) for i in list(range(1, 2))]

    total_time = 0
    for i in range(repeat):
        if i < 3:
            continue
        time_s = time.time()
        nk_in = {}
        for name,value in read_index(x_0):
            nk_in[name] = value

        time_e = time.time()
        total_time += time_e - time_s
    # print(nk_in)
    total_time_pythonic = 0
    for i in range(repeat):

        time_s = time.time()
        # l = {e_0 for e_0 in x_0}
        # l = {e_0 for e_0 in x_0 if e_0 // 1}
        # l = {
        #     e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2
        #     for e_0 in x_0 for e_1 in x_1 for e_2 in x_2}
        # l = {e_0: len(x_0[e_0]) for e_0 in x_0}
        nk_in = {name:value for name,value in read_index(x_0)}
        time_e = time.time()
        if i < 3:
            continue
        total_time_pythonic += time_e - time_s

    print('code is finished', total_time_pythonic, total_time, total_time / total_time_pythonic)


def func_a():

    repeat=10**6
    x_0 = list(range(1,1000001))
    x_0 = list(range(1, 101))
    x_1 = list(range(1, 101))
    x_2 = list(range(1, 101))
    x_0 = list(range(1, 101))
    x_0 = list(range(1, 10))
    x_0 = list(range(1, 3))
    dict_x0=dict()
    for i in x_0:
        dict_x0[i]=[j for j in range(i)]
    x_0=dict_x0
    # x_0 = list(range(1, 1000001))
    # x_0 = [0 for i in list(range(1, 1000001))]
    total_time = 0
    for i in range(repeat):
        time_s = time.time()
        # l = set()
        # for e_0 in x_0:
        #     if e_0 // 1:
        #         l.add(e_0)
        l = dict()
        for e_0 in x_0:
            l[e_0] = len(x_0[e_0])

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
        # l = {
        #     e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2
        #     for e_0 in x_0 for e_1 in x_1 for e_2 in x_2}
        l = {e_0: len(x_0[e_0]) for e_0 in x_0}
        time_e = time.time()
        if i < 3:
            continue
        total_time_pythonic += time_e - time_s

    print('code is finished', total_time_pythonic, total_time, total_time / total_time_pythonic)

if __name__ == '__main__':
    from networkx.generators import gnm_random_graph, powerlaw_cluster_graph
    func_a()
    func_generator()
    # n, m=15,100
    # g = gnm_random_graph(n, m, None, directed=True)
    #
    # # in-degree seqeunce of g as a list of integers.
    # in_degrees = list(dict(g.in_degree()).values())
    # func_len(in_degrees)
# repeat=13**6
# # func_a()
# x_0 = list(range(1, 100001))#1.747
# x_0 = list(range(1, 10001))#1.934 1000001 101
# # x_0 = list(range(1, 1001))#1.913 2.942 10**5 1000001 101
# x_0 = list(range(1, 101))#1.913 1.748 10**5 1000001 101
# # x_0 = list(range(1, 11))#1.44952 10**5 1000001 101
#
# total_time = 0
# for i in range(repeat):
#     time_s = time.time()
#     # l = set()
#     # for e_0 in x_0:
#     #     if e_0 // 1:
#     #         l.add(e_0)
#     l = dict()
#     for e_0 in x_0:
#         l[e_0] = e_0
#
#     # l = set()
#     # for e_0 in x_0:
#     #     l.add(e_0)
#     time_e = time.time()
#     if i < 3:
#         continue
#     total_time += time_e - time_s
# total_time_pythonic = 0
# for i in range(repeat):
#
#     time_s = time.time()
#     # l = {e_0 for e_0 in x_0}
#     # l = {e_0 for e_0 in x_0 if e_0 // 1}
#     # l = {
#     #     e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2
#     #     for e_0 in x_0 for e_1 in x_1 for e_2 in x_2}
#     l = {e_0: e_0 for e_0 in x_0}
#     time_e = time.time()
#     if i < 3:
#         continue
#     total_time_pythonic += time_e - time_s
#
# print('code is finished', total_time_pythonic, total_time, total_time / total_time_pythonic)