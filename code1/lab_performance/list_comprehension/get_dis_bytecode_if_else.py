import dis
def f1():
    x_0=[i for i in range(4)]
    l=[]
    for e_0 in x_0:
        for e_0 in x_0:
            if e_0 % 2:
                l.append(e_0)
            else:
                l.append(e_0)
def f2():
    x_0=[i for i in range(4)]
    l=[e_0 if e_0 % 2 else e_0 for e_0 in x_0 ]
def f_if():
    x_0=[i for i in range(4)]
    l=[]
    for e_0 in x_0:
        if e_0 % 2:
            l.append(e_0)
def f_if_not():
    x_0=[i*2 for i in range(4) if  i % 2]
    l=[]
    for e_0 in x_0:
        # if not e_0 % 2:
        #     l.append(e_0)
        if e_0 % 2:
            l.append(e_0)

#     a = [1, 2, 3, 4]
#     l = [i for i in a]
#
# print(dis.dis(f1) )
# print(dis.dis(f2) )
if __name__ == '__main__':
    # dis.dis(f_if)
    # dis.dis(f1)
    dis.dis(f_if_not)
    # dis.dis(f2)
    # a = [1, 2, 3, 4]
    # l = []
    # for i in a:
    #     l.append(i)
    # a = [1, 2, 3, 4]
    # l = [i for i in a]
