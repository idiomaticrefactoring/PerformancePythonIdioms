import os
import time
def run_test_cmd():
    cmd=f"nohup python3.9 run.py > run.log  2>&1 &"
    os.system(cmd)
    while True:
        if os.path.exists("run.log"):

            with open("run.log","r") as f:
                a=f.read()
                if a!="":
                    print(a)
                    cmd1 = f"nohup python3.9 run_1.py > run_1.log  2>&1 &"
                    os.system(cmd1)
                    break

    print("all python files have been executed")
if __name__ == '__main__':
    start_time=time.time()
    for i in range(5):
        i+=6
        path=f"list_compre_time_{str(i)}.log"
        cmd=f"nohup python3.9 list_compre_time.py > list_compre_time_{str(i)}.log  2>&1 &"
        os.system(cmd)
        while True:
            if os.path.exists(path):
                with open(path, "r") as f:
                    if "total running time of the program: " in f.read():
                        break
        time.sleep(10)
    print("total time: ",time.time()-start_time)
    print("Code is Over")

