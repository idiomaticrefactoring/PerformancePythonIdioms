import csv,os,json
import time,dis
import sys, ast, os, csv, time, traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-4]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
import util
# import numpy as np
# import performance_util
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
THIS_DIR = '/mnt/zejun/smp/code1/performance/test/'
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function
    Parameters:
        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True
    Returns:
        List of Dictionaries. Raw or processed structured data.
    """

    # Clear any blank lines
    linedata = list(filter(None, data.splitlines()))
    iter_time_list = []
    iter_time = 0
    if 1:
        for i in range(35):
            # clean up non-ascii characters, if any
            start = time.perf_counter()
            cleandata = [entry.encode('ascii', errors='ignore').decode() for entry in linedata]
            end = time.perf_counter()
            iter_time_list.append(end-start)
            iter_time += end - start
        print(len(cleandata))
    return iter_time,iter_time_list
if __name__ == '__main__':
    # parse(data, raw=False, quiet=False)
    # with open(os.path.join(THIS_DIR, os.pardir, 'generic/csv-flyrna.json'), 'r', encoding='utf-8') as f:
    #     generic_csv_flyrna_json = json.loads(f.read())
    #, generic_csv_flyrna_json

    total_time_list=[]
    total_time = 0
    file_name="/centos-7.7/systemctl-luf.out"#"/ubuntu-18.04/systemctl-luf.out"##"/generic/csv-deniro.csv"#"/generic/csv-cities.csv"#"/generic/csv-insurance.csv"#"/generic/csv-flyrna2.tsv"#"/generic/csv-flyrna.tsv"#"/generic/csv-flyrna2.tsv"#"/generic/systemctl-luf.out"#'/generic/csv-flyrna.tsv'
    print("".join([THIS_DIR, file_name]))
    #'''
    for i in range(5000):
        with open("".join([THIS_DIR, file_name]), 'r', encoding='utf-8') as f:
            generic_csv_flyrna = f.read()
            total_time_1,iter_time_list=parse(generic_csv_flyrna, quiet=True)
            total_time+=total_time_1
            total_time_list.append(iter_time_list)
    print(total_time)

    util.save_pkl(util.data_root+"performance/a_list_comprehension/test_some_test_cases/", file_name.split("/")[-1].split(".")[0], total_time_list)
    #'''
