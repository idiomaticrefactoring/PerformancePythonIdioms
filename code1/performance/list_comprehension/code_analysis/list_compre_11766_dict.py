import time,sys

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
print("total pythonic time: ",total_time_2,sys.getsizeof(a))

print("ratio: ",total_time/total_time_2)

total_time=0
for i in range(1000):
    start=time.perf_counter()
    a=[]
    for i in range(11766):
        a.append({i:i})
    end = time.perf_counter()
    total_time+=end-start
print("total time: ",total_time)


total_time_2=0
for i in range(1000):
    start=time.perf_counter()
    a=[{i:i} for i in range(11766)]
    end = time.perf_counter()
    total_time_2+=end-start
print("total pythonic time: ",total_time_2,sys.getsizeof(a))

print("ratio: ",total_time/total_time_2)

#{"ID": "FBgn0029994", "EGF_Baseline": "-1.25"}

total_time=0
for i in range(1000):
    start=time.perf_counter()
    a=[]
    for i in range(11766):
        a.append({"ID": "FBgn0029994", "EGF_Baseline": "-1.25"})
    end = time.perf_counter()
    total_time+=end-start
print("total time: ",total_time)


total_time_2=0
for i in range(1000):
    start=time.perf_counter()
    a=[{"ID": "FBgn0029994", "EGF_Baseline": "-1.25"} for i in range(11766)]
    end = time.perf_counter()
    total_time_2+=end-start
print("total pythonic time: ",total_time_2,sys.getsizeof(a))

print("ratio: ",total_time/total_time_2)