import itertools
data=[i for i in range(120)]

for i in [1,2]:
    temp_list = []
    for line in itertools.islice(data, 100):
        temp_list.append(line)
    print("len of temp_list: ",len(temp_list))
