import timeit

code='''
l = [e_0 for e_0 in x_0]
'''
print("*********zejun test total time pythonic**************",
      timeit.timeit(code,setup="x_0 = list(range(1,11))*100000",number=100))
print("code is finished")