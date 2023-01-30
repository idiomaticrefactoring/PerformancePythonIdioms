import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"test_case/")
import util,configure_pro_envir_util



for_num=4
if_num=5
if_else_num=5
# input_list=[[],[1],list(range(1,11)),list(range(1,11))*10,list(range(1,11))*100,list(range(1,11))*1000,
#             list(range(1,11))*10000,list(range(1,11))*100000]
input_list=['[]','[1]','list(range(1,11))','list(range(1,11))*10','list(range(1,11))*100','list(range(1,11))*1000',
            'list(range(1,11))*10000','list(range(1,11))*100000','list(range(1,11))*1000000']
dict_input_num={'[]':0,'[1]':1,'list(range(1,11))':10,'list(range(1,11))*10':100,
'list(range(1,11))*100':1000,'list(range(1,11))*1000':10000,
'list(range(1,11))*10000':100000,'list(range(1,11))*100000':1000000
}
# input_list=[['[]','[1]','list(range(1,11))','list(range(1,11))*10','list(range(1,11))*100','list(range(1,11))*1000',
#             'list(range(1,11))*10000','list(range(1,11))*100000','list(range(1,11))*1000000'],
# ['[]','[1]','list(range(1,4))','list(range(1,11))','list(range(1,9))*4','list(range(1,11))*10',
#             'list(range(1,5))*79','list(range(1,11))*100','list(range(1,7))*527'],
# ['[]', '[1]', 'list(range(1,3))', 'list(range(1,6))','list(range(1,11))', 'list(range(1,3))*11',
#              'list(range(1,3))*23', 'list(range(1,11))*10', 'list(range(1,6))*43'],
# ['[]', '[1]', 'list(range(1,3))', 'list(range(1,4))','list(range(1,7))', 'list(range(1,11))',
#              'list(range(1,10))*2', 'list(range(1,9))*4', 'list(range(1,9))*7']
#             ]


input_list=[['[]','[1]','list(range(1,11))','list(range(1,101))','list(range(1,1001))','list(range(1,10001))',
            'list(range(1,100001))','list(range(1,1000001))'],#,'list(range(1,10000001))'
['[]','[1]','list(range(1,4))','list(range(1,11))','list(range(1,33))','list(range(1,101))',
            'list(range(1,317))','list(range(1,1001))'],#,'list(range(1,3163))'
['[]', '[1]', 'list(range(1,3))', 'list(range(1,6))','list(range(1,11))', 'list(range(1,23))',
             'list(range(1,47))', 'list(range(1,101))'],#, 'list(range(1,216))'
['[]', '[1]', 'list(range(1,3))', 'list(range(1,4))','list(range(1,7))', 'list(range(1,11))',
             'list(range(1,19))', 'list(range(1,33))']#, 'list(range(1,57))'
            ]


# print(input_list_str)
# for_list=[''.join(['    '*j+'for e_'+str(j)+' in x_'+str(j)+':\n' for j in range(i+1)]) for i in range(4)]
# if_list=[''.join(['    '*j+'if e_'+str(j)+':\n' for j in range(i)]) for i in range(5)]
# if_else_list=[''.join(['    '*j+'if e_'+str(j)+'%2:\n'+'    '*(j+1)+'l.append(e_0)\n'+'    '*j+'else:\n'  for j in range(i)])+'    '*(i)+'l.append(e_0)'*(i>0) for i in range(5)]
for_list=[''.join(['    '*j+'for e_'+str(j)+' in x_'+str(j)+':\n' for j in range(i+1)]) for i in range(4)]
if_list=[''.join(['    '*j+'if e_'+str(0)+'//1:\n' for j in range(i)]) for i in range(5)]
if_else_list=[''.join(['    '*j+'if e_'+str(0)+'%2:\n'+'    '*(j+1)+'l.add(e_0)\n'+'    '*j+'else:\n'  for j in range(i)])+'    '*(i)+'l.add(e_0)'*(i>0) for i in range(5)]

'''
for e in if_list:
    print(e)

start=time.time()
l=[]
for i in range(10000000):
    l.append(i)
end = time.time()
print(end-start)
'''
'''
start=time.time()
l=[]
for i in range(100):
    for i in range(100):
        for i in range(100):
            for i in range(100):
                for i in range(100):
                    l.append(i)
end = time.time()
print(end-start)
'''
bench_dir=util.data_root_mv + "lab_performance/dict_compre_benchmarks/code/code/"
# for_list=['for e_'+str(i)+' in x_'+str(i)+':\n' for i in range(5)]
# if_else_list=['e_1 if e_'+str(i)+'%2 else ' for i in range(5)]
count=0
for i_for,e_for in enumerate(for_list[:]):
    # if i_for!=2:
    #     continue


    if i_for == 0:
        e_0_str = "e_0"
        pass
    elif i_for == 1:
        e_0_str = "e_0 * 10000 + e_1"
        pass
    elif i_for == 2:
        e_0_str = "e_0 * 100000 + e_1 * 1000 + e_2"
        pass
    elif i_for == 3:
        e_0_str = "e_0 * 1000000 + e_1 * 10000 + e_2 * 100 + e_3"
    if_else_list = [
        ''.join(
            ['    ' * j + 'if e_' + str(0) + '%2:\n' + '    ' * (j + 1) + f'l[{e_0_str}]=e_0\n' + '    ' * j + 'else:\n' for j
             in range(i)]
        ) + '    ' * (i) + f'l[{e_0_str}]=e_0' * (i > 0) for i in range(5)]
    for i_if,e_if in enumerate(if_list[:]):
        for i_if_else,e_if_else in enumerate(if_else_list[:]):
            for i_input,e_input in enumerate(input_list[i_for]):
                # if i_for<2 and i_if<2 and i_if_else<2:
                #     continue
                # if i_for<3 and i_if>1 and i_if_else>1:
                #     continue
                # if i_input>0:
                #     continue
                #'''
                # i_for=3
                # i_input=2
                # e_input=input_list[2]
                #'''
                # if i_for==1 and i_input==6:
                #     break
                # elif i_for==2 and i_input==4:# 事后可以改为4,这样就可以为8
                #     break
                # elif i_for==3 and i_input==3:# 事后可以改为4,这样就可以为8
                #     break
                # elif i_for==4 and i_input==3:
                #     break

                # print("e_for: ",e_for)
                # print("e_if: ",e_if)
                # print("e_if_else: ",e_if_else)
                code_complicated_str=e_for
                for_index=e_for.strip().split('\n')[-1].index('f')
                if e_if:
                    code_complicated_str+='\n'.join([' '*(for_index+4)+e for e in e_if.strip().split("\n")])+"\n"
                    if_index = code_complicated_str.strip().split('\n')[-1].index('if')
                else:
                    # code_complicated_str += ' ' * (for_index+4) + "l.append(e_0)\n"
                    if_index = for_index

                if e_if_else:
                    pass
                    code_complicated_str+='\n'.join([' '*(if_index+4)+e for e in e_if_else.strip().split("\n")])+"\n"
                else:
                    pass
                    code_complicated_str += ' ' * (if_index + 4) + f"l[{e_0_str}]=e_0"
                code_complicated_str=''.join(['x_'+str(i)+' = '+e_input+"\n" for i in range(i_for+1)])+"l = dict()\n"+code_complicated_str+"\nprint('len: ',len(l))\nprint('code is finished')"
                # print(code_complicated_str)
                # print("----------------------")
                save_path=bench_dir+"_".join([str(i_for+1),str(i_if),str(i_if_else),e_input])+'.py'
                # print(save_path)
                util.save_file_path(save_path, code_complicated_str)
                count+=1
                # break
        #     break
        # break
    # break
                # util.save_file_path(save_path,code_complicated_str)
                # print("save successfully! ",save_path)

# sequence_run(bench_dir,python_version='7',invocations=3)
print("count: ",count)