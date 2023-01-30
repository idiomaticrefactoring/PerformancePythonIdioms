import csv,os,json
import time,dis
import sys, ast, os, csv, time, traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-4]) + "/"
sys.path.append(code_dir)
import util
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



    cleandata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, cleandata))

    if 1:

        dialect = 'excel'  # default in csv module
        try:
            dialect = csv.Sniffer().sniff(data[:1024])
            if '""' in data:
                dialect.doublequote = True
        except Exception:
            pass
        iter_time_list = []
        iter_time = 0
        for i in range(35):
            reader = csv.DictReader(cleandata, dialect=dialect)
            start = time.perf_counter()
            raw_output = []
            for row in reader:
                raw_output.append(row)
            end=time.perf_counter()
            print(">>>>time: ",end-start)
            if i < 2:
                continue
            iter_time += end - start
            iter_time_list.append(end-start)

        print(len(raw_output))
        return iter_time,iter_time_list

if __name__ == '__main__':
    # parse(data, raw=False, quiet=False)
    # with open(os.path.join(THIS_DIR, os.pardir, 'generic/csv-flyrna.json'), 'r', encoding='utf-8') as f:
    #     generic_csv_flyrna_json = json.loads(f.read())
    #, generic_csv_flyrna_json
    file_name ="/generic/csv-deniro.csv"#"/generic/csv-cities.csv"#"/generic/csv-insurance.csv"#"/generic/csv-flyrna2.tsv"#"/generic/csv-flyrna.tsv"  #"/generic/csv-flyrna2.tsv"#"/generic/systemctl-luf.out"
    total_time_list = []
    total_time = 0
    print("".join([THIS_DIR, file_name]))
    for i in range(50):
        with open("".join([THIS_DIR, file_name]), 'r', encoding='utf-8') as f:
            generic_csv_flyrna = f.read()
            total_time_1, iter_time_list = parse(generic_csv_flyrna, quiet=True)
            total_time += total_time_1
            total_time_list.append(iter_time_list)
    print(total_time)
    util.save_pkl(util.data_root+"performance/a_list_comprehension/test_some_test_cases_complicate/", file_name.split("/")[-1].split(".")[0], total_time_list)

    # dis.dis(parse)