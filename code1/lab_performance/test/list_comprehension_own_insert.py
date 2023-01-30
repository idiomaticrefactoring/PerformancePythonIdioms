import time
total_time=0
x_0 = list(range(1,11))*100000
for i in range(100):
    start=time.perf_counter()
    l = []
    for e_0 in x_0:
        l.append(e_0)
    end = time.perf_counter()
    print("*********zejun test total time pythonic**************",end-start)
    total_time += end - start
print("code is finished: ",total_time)
