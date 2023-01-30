import itertools
data=[i for i in range(120)]

for i in [1,2]:
    temp_list = []
    for line in itertools.islice(data, 100):
        temp_list.append(line)
    print("len of temp_list: ",len(temp_list))
a=itertools.islice(data, 100)
for i in [1,2]:
    len_a=0
    for e in a:
        pass
    print("len of len_a: ",len(temp_list))



