a=1
b=2
str_1='''
for i in range(b):
    print(a)
    c=a+b
'''
a=exec(str_1)
print(a)