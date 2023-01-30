import subprocess
import time

import psutil
total_cmd=" cd /mnt/zejun/smp/code1/performance/test/data_enlarge/ ;python3 file_is_repeat.py"
try:
        # result = subprocess.run(total_cmd, shell=True,timeout=5, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # result = subprocess.check_output(total_cmd, shell=True, start_new_session=True, kill_group=True, timeout=5)
        result = subprocess.Popen(total_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for _ in range(5):  # 30 seconds
                if result.poll() is not None:  # process just ended
                        break
                time.sleep(1)

        else:
                print("come here")
                # the for loop ended without break: timeout
                parent = psutil.Process(result.pid)
                for child in parent.children(recursive=True):  # or parent.children() for recursive=False
                        child.kill()
                parent.kill()
        # std_out_res = result.stdout.decode("utf-8")
        # # print("std_out_res: \n", std_out_res)
        # std_error = result.stderr.decode("utf-8") if result.stderr else ""
        # std_args = result.args
        # output = "\n".join([std_out_res, std_error, std_args])
        out, err = result.communicate()
        print("result: ",out,err)
        # print("std_out_res： ",std_out_res)
        #
        # print("std_error： ",std_error)
        print("std_args： ",result.args)
        # parent = psutil.Process(result.pid)
        # for child in parent.children(recursive=True):  # or parent.children() for recursive=False
        #         child.kill()
        # parent.kill()
# kill_group=True
except subprocess.TimeoutExpired:

        print("the command run more than 15*60s, please check: ", total_cmd)
        # raise
