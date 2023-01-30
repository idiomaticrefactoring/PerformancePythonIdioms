import dis
import time
# import numpy as np
# def func_arg(*e):
#     pass
def func_arg(*a):
    pass

def call_func():
    def f(x, y):
        return x ** 2 + y ** 2

    x = y = np.linspace(-10, 10, 10)

    x, y = np.meshgrid(x, y)

    z = f(x, y)

    e_list = [i for i in range(10)]
    points = np.asarray([x, y, z,y,x,y,x,y])
    print(points.__class__)
    # points = [i for i in range(10)]

    func_a_part(points)
import re
import dns,re
import dns.exception
import dns.ipv4
_v4_ending = re.compile(rb"(.*):(\d+\.\d+\.\d+\.\d+)$")
def func_test_ipv6(text,ignore_scope=False):
    if not isinstance(text, bytes):
        btext = text.encode()
    else:
        btext = text

    if ignore_scope:
        parts = btext.split(b"%")
        l = len(parts)
        if l == 2:
            btext = parts[0]
        elif l > 2:
            raise dns.exception.SyntaxError

    if btext == b"":
        raise dns.exception.SyntaxError
    elif btext.endswith(b":") and not btext.endswith(b"::"):
        raise dns.exception.SyntaxError
    elif btext.startswith(b":") and not btext.startswith(b"::"):
        raise dns.exception.SyntaxError
    elif btext == b"::":
        btext = b"0::"
        #
        # Get rid of the icky dot-quad syntax if we have it.
        #
    print("btext: ", btext)
    m = _v4_ending.match(btext)
    print("m: ",m)
    if m is not None:
        b = dns.ipv4.inet_aton(m.group(2))
        print("b: ",b)
        repeat = 10 ** 6
        total_time_zejun = 0
        for i in range(repeat):
            if i < 3:
                continue
            start_time_zejun = time.perf_counter()
            func_arg(b[0], b[1], b[2], b[3])
            end_time_zejun = time.perf_counter()
            total_time_zejun += end_time_zejun - start_time_zejun
        total_time_zejun_pythonic = 0
        for i in range(repeat):
            if i < 3:
                continue
            start_time_zejun = time.perf_counter()
            func_arg(*b)
            end_time_zejun = time.perf_counter()
            total_time_zejun_pythonic += end_time_zejun - start_time_zejun
        print('变量 perf_change: ', total_time_zejun, total_time_zejun_pythonic, total_time_zejun / total_time_zejun_pythonic)


def func_a_part():

    repeat=10**6
    e_list=[1,2,3,4]
    e_list = [1, 2]
    i_s = 0
    total_time_zejun = 0
    for i in range(repeat):
        if i<3:
            continue
        start_time_zejun = time.perf_counter()
        # func_arg(e_list[0],e_list[1], e_list[2])
        # func_arg(points[0], points[1], points[2], points[3])
        func_arg(e_list[0],e_list[1])
        # e_list[0]
        # func_arg(e_list[:2])

        # func_arg(points[0], points[1], points[2], points[3], points[4], points[5], points[6], points[7])

        # func_arg(e_list[0], e_list[1])
        # func_arg(*e_list[:2])
        # func_arg(e_list[i_s], e_list[i_s+1])
        # func_arg(e_list[i_s], e_list[i_s + 1],e_list[i_s + 2])
        # func_arg(e_list[i_s], e_list[i_s + 1],e_list[i_s + 2],e_list[i_s + 3])
        # func_arg(e_list[0], e_list[1], e_list[2], e_list[3], e_list[4],e_list[5])

        # func_arg(e_list[0], e_list[1], e_list[2], e_list[3], e_list[4],e_list[5],e_list[6])
        # func_arg(e_list[0], e_list[1])
        # func_arg(e_list[0], e_list[1])
        end_time_zejun = time.perf_counter()
        total_time_zejun += end_time_zejun - start_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)

    total_time_zejun_pythonic = 0
    for i in range(repeat):
        if i<3:
            continue
        start_time_zejun = time.perf_counter()
        # func_arg(*e_list[1:3:1])
        # func_arg(*points[:4])
        # func_arg(*points[:8])
        # func_arg(*points)
        # e_list[:2]
        # func_arg(*e_list[:2])

        func_arg(*e_list)
        # func_arg(*e_list[i_s:i_s+2:1])
        # func_arg(*e_list[i_s:i_s + 3])
        # func_arg(*e_list[i_s:i_s + 4])
        # func_arg(*e_list[0:2])
        # func_arg(*e_list[0:6])
        # func_arg(*e_list[0:7])

        end_time_zejun = time.perf_counter()
        total_time_zejun_pythonic += end_time_zejun - start_time_zejun
    print('变量 perf_change: ', total_time_zejun, total_time_zejun_pythonic, total_time_zejun / total_time_zejun_pythonic)


def func_a():
    import time
    e_list=[0,1]
    i_s=0
    total_time_zejun=0
    for i in range(10**5):

        start_time_zejun = time.perf_counter()
        # func_arg(e_list[i_s], e_list[i_s+1])
        # func_arg(e_list[0], e_list[1])
        func_arg(1,e_list[0], e_list[1], e_list[1])
        end_time_zejun = time.perf_counter()
        total_time_zejun+= end_time_zejun - start_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)

    total_time_zejun_pythonic = 0
    for i in range(10 ** 5):
        start_time_zejun = time.perf_counter()
        func_arg(*e_list)
        func_arg(1,*e_list)
        end_time_zejun = time.perf_counter()
        total_time_zejun_pythonic += end_time_zejun - start_time_zejun
    print('变量 perf_change: ',total_time_zejun, total_time_zejun_pythonic,total_time_zejun/total_time_zejun_pythonic)
import numpy as np
def array():
    repeat=10**6
    def f(x, y):
        return x ** 2 + y ** 2
    x = y = np.linspace(-10, 10, 10)

    x, y = np.meshgrid(x, y)

    z = f(x, y)

    points = np.asarray([x, y, z])
    # print(points.__class__)
    # points=list(points)
    # points = np.asarray([x, y, z]*14)
    a,*b,c=points
    # print(a,b.__class__,c)
    import time
    e_list = [0, 1]
    i_s = 0
    total_time_zejun = 0
    for i in range(repeat):
        start_time_zejun = time.perf_counter()
        # func_arg(*points)
        # func_arg(e_list[i_s], e_list[i_s+1])
        # func_arg(e_list[0], e_list[1])
        func_arg(points[0], points[1], points[2])
        # func_arg(points[0], points[1], points[2],points[3], points[4], points[5],points[6], points[7], points[8],
        #          points[9], points[10], points[11],points[12], points[13], points[14],
        #          points[15], points[16], points[17],points[18], points[19], points[20],points[21], points[22], points[23],
        #          points[24], points[25], points[26],points[27], points[28], points[29],points[30], points[31], points[32],
        #          points[33], points[34], points[35], points[36], points[37], points[38], points[39], points[40],points[41] )

        # func_arg(points[0], points[1], points[2],points[3], points[4], points[5])
        end_time_zejun = time.perf_counter()
        total_time_zejun += end_time_zejun - start_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)

    total_time_zejun_pythonic = 0
    for i in range(repeat):
        start_time_zejun = time.perf_counter()
        func_arg(*tuple(points))
        # tuple(points)
        # func_arg(1, *points)
        end_time_zejun = time.perf_counter()
        total_time_zejun_pythonic += end_time_zejun - start_time_zejun
    print('array 变量 perf_change: ', total_time_zejun, total_time_zejun_pythonic, total_time_zejun / total_time_zejun_pythonic)

    import time
    points=[1,2,2]
    e_list = [0, 1]
    i_s = 0
    total_time_zejun = 0
    for i in range(repeat):
        start_time_zejun = time.perf_counter()
        # func_arg(e_list[i_s], e_list[i_s+1])
        # func_arg(e_list[0], e_list[1])
        func_arg(points[0], points[1], points[2])
        end_time_zejun = time.perf_counter()
        total_time_zejun += end_time_zejun - start_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)

    total_time_zejun_pythonic = 0
    for i in range(repeat):
        start_time_zejun = time.perf_counter()
        func_arg(*tuple(points))
        # func_arg(1, *points)
        end_time_zejun = time.perf_counter()
        total_time_zejun_pythonic += end_time_zejun - start_time_zejun
    print('变量 perf_change: ', total_time_zejun, total_time_zejun_pythonic, total_time_zejun / total_time_zejun_pythonic)

if __name__ == '__main__':
    array()
    # func_a_part()
    # dis.dis(func_a)
    valid = (
        "::1",
        "::",
        "0:0:0:0:0:0:0:1",
        "0:0:0:0:0:0:0:0",
        "2001:DB8:0:0:8:800:200C:417A",
        "FF01:0:0:0:0:0:0:101",
        "2001:DB8::8:800:200C:417A",
        "FF01::101",
        "fe80::217:f2ff:fe07:ed62",
        "2001:0000:1234:0000:0000:C1C0:ABCD:0876",
        "3ffe:0b00:0000:0000:0001:0000:0000:000a",
        "FF02:0000:0000:0000:0000:0000:0000:0001",
        "0000:0000:0000:0000:0000:0000:0000:0001",
        "0000:0000:0000:0000:0000:0000:0000:0000",
        "2::10",
        "ff02::1",
        "fe80::",
        "2002::",
        "2001:db8::",
        "2001:0db8:1234::",
        "::ffff:0:0",
        "1:2:3:4:5:6:7:8",
        "1:2:3:4:5:6::8",
        "1:2:3:4:5::8",
        "1:2:3:4::8",
        "1:2:3::8",
        "1:2::8",
        "1::8",
        "1::2:3:4:5:6:7",
        "1::2:3:4:5:6",
        "1::2:3:4:5",
        "1::2:3:4",
        "1::2:3",
        "::2:3:4:5:6:7:8",
        "::2:3:4:5:6:7",
        "::2:3:4:5:6",
        "::2:3:4:5",
        "::2:3:4",
        "::2:3",
        "::8",
        "1:2:3:4:5:6::",
        "1:2:3:4:5::",
        "1:2:3:4::",
        "1:2:3::",
        "1:2::",
        "1::",
        "1:2:3:4:5::7:8",
        "1:2:3:4::7:8",
        "1:2:3::7:8",
        "1:2::7:8",
        "1::7:8",
        "1:2:3:4:5:6:1.2.3.4",
        "1:2:3:4:5::1.2.3.4",
        "1:2:3:4::1.2.3.4",
        "1:2:3::1.2.3.4",
        "1:2::1.2.3.4",
        "1::1.2.3.4",
        "1:2:3:4::5:1.2.3.4",
        "1:2:3::5:1.2.3.4",
        "1:2:3::5:1.2.3.4",
        "1:2::5:1.2.3.4",
        "1::5:1.2.3.4",
        "1::5:11.22.33.44",
        "fe80::217:f2ff:254.7.237.98",
        "::ffff:192.168.1.26",
        "::ffff:192.168.1.1",
        "0:0:0:0:0:0:13.1.68.3",
        "0:0:0:0:0:FFFF:129.144.52.38",
        "::13.1.68.3",
        "::FFFF:129.144.52.38",
        "fe80:0:0:0:204:61ff:254.157.241.86",
        "fe80::204:61ff:254.157.241.86",
        "::ffff:12.34.56.78",
        "::ffff:192.0.2.128",
        "fe80:0000:0000:0000:0204:61ff:fe9d:f156",
        "fe80:0:0:0:204:61ff:fe9d:f156",
        "fe80::204:61ff:fe9d:f156",
        "fe80::1",
        "::ffff:c000:280",
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "2001:db8:85a3:0:0:8a2e:370:7334",
        "2001:db8:85a3::8a2e:370:7334",
        "2001:0db8:0000:0000:0000:0000:1428:57ab",
        "2001:0db8:0000:0000:0000::1428:57ab",
        "2001:0db8:0:0:0:0:1428:57ab",
        "2001:0db8:0:0::1428:57ab",
        "2001:0db8::1428:57ab",
        "2001:db8::1428:57ab",
        "::ffff:0c22:384e",
        "2001:0db8:1234:0000:0000:0000:0000:0000",
        "2001:0db8:1234:ffff:ffff:ffff:ffff:ffff",
        "2001:db8:a::123",
        "1111:2222:3333:4444:5555:6666:7777:8888",
        "1111:2222:3333:4444:5555:6666:7777::",
        "1111:2222:3333:4444:5555:6666::",
        "1111:2222:3333:4444:5555::",
        "1111:2222:3333:4444::",
        "1111:2222:3333::",
        "1111:2222::",
        "1111::",
        "1111:2222:3333:4444:5555:6666::8888",
        "1111:2222:3333:4444:5555::8888",
        "1111:2222:3333:4444::8888",
        "1111:2222:3333::8888",
        "1111:2222::8888",
        "1111::8888",
        "::8888",
        "1111:2222:3333:4444:5555::7777:8888",
        "1111:2222:3333:4444::7777:8888",
        "1111:2222:3333::7777:8888",
        "1111:2222::7777:8888",
        "1111::7777:8888",
        "::7777:8888",
        "1111:2222:3333:4444::6666:7777:8888",
        "1111:2222:3333::6666:7777:8888",
        "1111:2222::6666:7777:8888",
        "1111::6666:7777:8888",
        "::6666:7777:8888",
        "1111:2222:3333::5555:6666:7777:8888",
        "1111:2222::5555:6666:7777:8888",
        "1111::5555:6666:7777:8888",
        "::5555:6666:7777:8888",
        "1111:2222::4444:5555:6666:7777:8888",
        "1111::4444:5555:6666:7777:8888",
        "::4444:5555:6666:7777:8888",
        "1111::3333:4444:5555:6666:7777:8888",
        "::3333:4444:5555:6666:7777:8888",
        "::2222:3333:4444:5555:6666:7777:8888",
        "1111:2222:3333:4444:5555:6666:123.123.123.123",
        "1111:2222:3333:4444:5555::123.123.123.123",
        "1111:2222:3333:4444::123.123.123.123",
        "1111:2222:3333::123.123.123.123",
        "1111:2222::123.123.123.123",
        "1111::123.123.123.123",
        "::123.123.123.123",
        "1111:2222:3333:4444::6666:123.123.123.123",
        "1111:2222:3333::6666:123.123.123.123",
        "1111:2222::6666:123.123.123.123",
        "1111::6666:123.123.123.123",
        "::6666:123.123.123.123",
        "1111:2222:3333::5555:6666:123.123.123.123",
        "1111:2222::5555:6666:123.123.123.123",
        "1111::5555:6666:123.123.123.123",
        "::5555:6666:123.123.123.123",
        "1111:2222::4444:5555:6666:123.123.123.123",
        "1111::4444:5555:6666:123.123.123.123",
        "::4444:5555:6666:123.123.123.123",
        "1111::3333:4444:5555:6666:123.123.123.123",
        "::2222:3333:4444:5555:6666:123.123.123.123",
        "::0:0:0:0:0:0:0",
        "::0:0:0:0:0:0",
        "::0:0:0:0:0",
        "::0:0:0:0",
        "::0:0:0",
        "::0:0",
        "::0",
        "0:0:0:0:0:0:0::",
        "0:0:0:0:0:0::",
        "0:0:0:0:0::",
        "0:0:0:0::",
        "0:0:0::",
        "0:0::",
        "0::",
        "0:a:b:c:d:e:f::",
        "::0:a:b:c:d:e:f",
        "a:b:c:d:e:f:0::",
    )
    text="00.00.00.00"#".."#"255Z255X255Y255"#"1.2.."#"256.256.256.256"#"400.2.3.4"
    # for text in valid:
    #     try:
    #         func_test_ipv6(text,ignore_scope=True)
    #     except:
    #         continue
    # func_a_part()
    import sys
    # sys.exc_info()
    # dis.dis(func_a)
    # call_func()
    # func_a_part()
    # dis.dis(func_a_part)
'''
    func_a_part()
    # print('code is finished')
    e_list = [i for i in range(2)]
    i_s = 0
    total_time_zejun = 0
    for i in range(10 ** 7):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        func_arg(e_list[0], e_list[1])
        # func_arg(e_list[1], e_list[2])
        # func_arg(e_list[i_s], e_list[i_s + 1])
        # func_arg(e_list[i_s], e_list[i_s + 1],e_list[i_s + 2])
        # func_arg(e_list[i_s], e_list[i_s + 1],e_list[i_s + 2],e_list[i_s + 3])
        # func_arg(e_list[0], e_list[1], e_list[2], e_list[3], e_list[4],e_list[5])

        # func_arg(e_list[0], e_list[1], e_list[2], e_list[3], e_list[4],e_list[5],e_list[6])
        # func_arg(e_list[0], e_list[1])
        # func_arg(e_list[0], e_list[1])
        end_time_zejun = time.perf_counter()
        total_time_zejun += end_time_zejun - start_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)

    total_time_zejun_pythonic = 0
    for i in range(10 ** 7):
        if i < 3:
            continue
        start_time_zejun = time.perf_counter()
        func_arg(*e_list)
        # func_arg(*e_list[1:3:1])
        # func_arg(*e_list[i_s:i_s + 2:1])
        # func_arg(*e_list[i_s:i_s + 3])
        # func_arg(*e_list[i_s:i_s + 4])
        # func_arg(*e_list[0:2])
        # func_arg(*e_list[0:6])
        # func_arg(*e_list[0:7])

        end_time_zejun = time.perf_counter()
        total_time_zejun_pythonic += end_time_zejun - start_time_zejun
    print('变量 perf_change: ', total_time_zejun, total_time_zejun_pythonic, total_time_zejun / total_time_zejun_pythonic)
'''