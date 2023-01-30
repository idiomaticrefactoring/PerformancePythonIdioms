import time

x_0 = list(range(1, 11)) * 100
x_1 = list(range(1, 11)) * 100
for i in range(100):
    start=time.perf_counter()
    l = []
    for e_0 in x_0:
        for e_1 in x_1:
            l.append(e_0)
    end = time.perf_counter()
    print("*********zejun test total time**************",end-start)
print("code is finished")