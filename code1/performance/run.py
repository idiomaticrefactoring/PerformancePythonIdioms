import os
import time
with open("1.txt",'w') as f:
    a='1'*100
    f.write(a)
a=[]
for i in range(100000):
    a.append(i)
print(time.time())

    
