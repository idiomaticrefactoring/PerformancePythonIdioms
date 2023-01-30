import operator
import collections
import dis
def identity(x):
    # """ Identity function. Return x
    # >>> identity(3)
    # 3
    # """
    return x
def getter(index):
    if isinstance(index, list):
        if len(index) == 1:
            index = index[0]
            return lambda x: (x[index],)
        elif index:
            return operator.itemgetter(*index)
        else:
            return lambda x: ()
    else:
        return operator.itemgetter(index)
def groupby(key, seq):
    """ Group a collection by a key function
    # >>> names = ['Alice', 'Bob', 'Charlie', 'Dan', 'Edith', 'Frank']
    # >>> groupby(len, names)  # doctest: +SKIP
    # {3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}
    # >>> iseven = lambda x: x % 2 == 0
    # >>> groupby(iseven, [1, 2, 3, 4, 5, 6, 7, 8])  # doctest: +SKIP
    # {False: [1, 3, 5, 7], True: [2, 4, 6, 8]}
    # Non-callable keys imply grouping on a member.
    # >>> groupby('gender', [{'name': 'Alice', 'gender': 'F'},
    # ...                    {'name': 'Bob', 'gender': 'M'},
    # ...                    {'name': 'Charlie', 'gender': 'M'}]) # doctest:+SKIP
    {'F': [{'gender': 'F', 'name': 'Alice'}],
     'M': [{'gender': 'M', 'name': 'Bob'},
           {'gender': 'M', 'name': 'Charlie'}]}
    Not to be confused with ``itertools.groupby``
    See Also:
        countby
    """
    if not callable(key):
        key = getter(key)
    d = collections.defaultdict(lambda: [].append)
    print(d)
    for item in seq:
        d[key(item)](item)
        # print(d[key(item)])
    print(d)
    rv = {}
    for k, v in d.items():
        rv[k] = v.__self__
    rv = {k: v.__self__ for (k, v) in d.items()}
    return rv
def ele_0():
    self._collaborators = {}
    for collaborator in collaborators_raw:
        self._collaborators[collaborator['email']] = RoleValue(collaborator['role'])

    self._collaborators = {collaborator['email']: RoleValue(collaborator['role']) for collaborator in collaborators_raw}
from pmf import PMF
import numpy as np
import time
def func_zip():
    a = np.zeros([2, 2, 2, 2], dtype=np.float)
    a[0, 1, 1, 1] = 1.0
    pmf = PMF({'Flu': [False, True], 'Meningitis': [False, True], 'Light Sensitivity': [False, True],
               'Fever': [False, True]}, a)
    repeat=10**6
    choice = pmf.select()
    chosen_index=(0, 1, 1, 1)
    vars={'Flu': [False, True], 'Meningitis': [False, True], 'Light Sensitivity': [False, True], 'Fever': [False, True]}
    total_time = 0
    total_time_pythonic=0
    # dict_items
    print(vars.items().__class__)
    print(zip(chosen_index, vars.items()),iter(zip()))
    for i in range(repeat):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()

        answer = {}
        for index, (variable, discrete_values) in zip(chosen_index, vars.items()):
            answer[variable] = discrete_values[index]
        end_time_zejun = time.perf_counter()

        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
    print("answer ",answer)
    # print('\n*********zejun test total time************** ', total_time_zejun)


    for i in range(repeat):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        answer = {variable:discrete_values[index] for index, (variable, discrete_values) in zip(chosen_index, vars.items())}
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
    print('func code is finished: ', total_time_pythonic, total_time, total_time / total_time_pythonic)
    total_time=0
    total_time_pythonic=0
    vars=vars.items()
    for i in range(repeat):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()

        answer = {}
        for index, (variable, discrete_values) in zip(chosen_index, vars):
            answer[variable] = discrete_values[index]
        end_time_zejun = time.perf_counter()

        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
    # print('\n*********zejun test total time************** ', total_time_zejun)


    for i in range(repeat):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        answer = {variable:discrete_values[index] for index, (variable, discrete_values) in zip(chosen_index, vars)}
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
    print('func code is finished: ', total_time_pythonic, total_time, total_time / total_time_pythonic)
    total_time=0
    total_time_pythonic=0

    # vars=vars.items()
    a=[i for i in range(4)]
    for i in range(repeat):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()

        answer = {}
        for i in a:
            answer[i]=a[i]
        # for index, (variable, discrete_values) in zip(chosen_index, vars):
        #     answer[variable] = discrete_values[index]
        end_time_zejun = time.perf_counter()

        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
    # print('\n*********zejun test total time************** ', total_time_zejun)


    for i in range(repeat):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        # answer = {variable:discrete_values[index] for index, (variable, discrete_values) in zip(chosen_index, vars)}
        answer = {i:a[i] for i in a}

        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
    print('func code is finished: ', total_time_pythonic, total_time, total_time / total_time_pythonic)

# flattened = pmf._pmf_array.flatten()
    #
    # answer = {}
    #
    # indices = list(np.ndindex(pmf._pmf_array.shape))
    # int_index = list(range(len(indices)))
    # chosen_int = np.random.choice(int_index, p=flattened)
    # chosen_index = indices[chosen_int]
    # for index, (variable, discrete_values) in zip(chosen_index, pmf._variables.items()):
    #     answer[variable] = discrete_values[index]
from zlib import compress, decompress
from urllib.parse import parse_qs, urlencode
from base64 import urlsafe_b64encode, urlsafe_b64decode
import copy
def test_decode(input_data):
    decoded_data = decompress(urlsafe_b64decode(input_data.encode()))
    dict_data = {}
    for x, y in parse_qs(decoded_data.decode()).items():
        dict_data[x] = y[0]
    copy.copy()
def parse_qs():
    from urllib.parse import parse_qs

if __name__ == '__main__':
    dis.dis(groupby)
    dis.dis(ele_0)
    func_zip()
    # data = list(range(10)) * 10
    # print(data)
    # data = list(range(10)) * 10#list(range(1000)) * 1000
    # print(groupby(identity, data))