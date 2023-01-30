import time

total_time=0
for i in range(1000):
    start=time.perf_counter()
    a=[]
    for i in range(11766):
        a.append(i)
    end = time.perf_counter()
    total_time+=end-start
print("total time: ",total_time)


total_time_2=0
for i in range(1000):
    start=time.perf_counter()
    a=[i for i in range(11766)]
    end = time.perf_counter()
    total_time_2+=end-start
print("total pythonic time: ",total_time_2)

print("ratio: ",total_time/total_time_2)