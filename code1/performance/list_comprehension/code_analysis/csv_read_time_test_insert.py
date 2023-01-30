import csv,os,json
import time,dis
import sys, ast, os, csv, time, traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-4]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
import util
import numpy as np
import performance_util
# code_dir = "/".join(os.path.abspath(__file__).split("/")[:-4]) + "/"
# sys.path.append(code_dir)
# sys.path.append(code_dir+"performance/")
# import util,performance_util
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
THIS_DIR = '/mnt/zejun/smp/code1/performance/test/'


def get_performance_info( total_time_list_info_dict=dict(), threshold=1, invocations=None, steps=1000,
                         remove_outlier=False, factor=1.5):
    # total_time_list_info_dict=self.total_time_list_info_dict
    ind_instance=0
    test_me=""
    if 1:
    # for test_me in total_time_list_info_dict:
    #     for ind_instance in total_time_list_info_dict[test_me]:
            if not invocations:
                invocations = len(total_time_list_info_dict["time_list"])
            valid_time_list = total_time_list_info_dict["time_list"][:invocations]
            valid_idiom_time_list = total_time_list_info_dict["pythonic_time_list"][:invocations]
            if len(valid_time_list) < threshold or len(valid_idiom_time_list) < threshold:
                print(
                    f"check time list of {ind_instance}th of {test_me} because its stable invocations is less than {threshold} ",
                    len(valid_time_list), len(valid_idiom_time_list))

            if remove_outlier:
                filter_time_list = performance_util.filter_outlier_2(valid_time_list, factor)
                filter_time_list_idiom = performance_util.filter_outlier_2(valid_idiom_time_list, factor)

                # filter_time_list=performance_util.filter_outlier(valid_time_list)
                # filter_time_list_idiom=performance_util.filter_outlier(valid_idiom_time_list)

                # flatten_time_list=[ee for e in valid_time_list for ee in e]
                # median=np.median(flatten_time_list)
                # mad=stats.median_abs_deviation(flatten_time_list)
                # filter_time_list=[e for e in flatten_time_list if median+3*mad>e>median-3*mad]
                # flatten_time_list_idiom = [ee for e in valid_idiom_time_list for ee in e]
                # median = np.median(flatten_time_list_idiom)
                # mad = stats.median_abs_deviation(flatten_time_list_idiom)
                # filter_time_list_idiom = [e for e in flatten_time_list_idiom if median + 3 * mad > e > median - 3 * mad]

                real_per_change = sum(filter_time_list) / sum(filter_time_list_idiom)
            else:
                real_per_change = sum([sum(e) for e in valid_time_list]) / sum(
                    [sum(e) for e in valid_idiom_time_list])

            all_boot_time_list = performance_util.num_bootstrap(valid_time_list, steps=steps)
            all_boot_idiom_time_list = performance_util.num_bootstrap(valid_idiom_time_list, steps=steps)

            '''
            get performance change and confidence interval
            '''
            prf_change_list = []
            for ind_step, boot_time_list in enumerate(all_boot_time_list):
                boot_idiom_time_list = all_boot_idiom_time_list[ind_step]
                if remove_outlier:
                    filter_time_list = performance_util.filter_outlier_2(boot_time_list, factor)
                    filter_time_list_idiom = performance_util.filter_outlier_2(boot_idiom_time_list, factor)
                    # filter_time_list = performance_util.filter_outlier(boot_time_list)
                    # filter_time_list_idiom = performance_util.filter_outlier(boot_idiom_time_list)
                    e_sum = sum(filter_time_list)
                    e_idiom_sum = sum(filter_time_list_idiom)
                else:
                    e_sum = sum([sum(e) for e in boot_time_list])
                    e_idiom_sum = sum([sum(e) for e in boot_idiom_time_list])
                # print("e_time_list: ",sum(e_time_list))
                # print(e_idiom_time_list)
                # print(np.mean(np.array(e_time_list,dtype=np.float64),None))
                per_change = e_sum / e_idiom_sum
                prf_change_list.append(per_change - real_per_change)
            left, right = np.percentile(prf_change_list, [2.5, 97.5])
            # self.mean_perf_change = real_per_change
            if left + real_per_change < 1 < right + real_per_change:
                # print("1 is in performance confidence interval, the file_name: ", self.file_html)
                print((left + real_per_change, right + real_per_change), real_per_change)
                # self.mean_perf_change = 1.0
            else:
                # print("file_name: ", file_name)
                # print(left+real_per_change, right+real_per_change,real_per_change)
                pass
            # self.stable_compli_time_list = valid_time_list
            # self.stable_simp_time = valid_idiom_time_list
            # self.interval = (left, right)
            total_time_list_info_dict["perf_change"] = [real_per_change,
                                                                                    left + real_per_change,
                                                                                    right + real_per_change]
            print(
                f"{len(valid_time_list)} and {len(valid_idiom_time_list)} stable num, {ind_instance}th instance of {test_me} test method's  performance change info: ",
                real_per_change,
                (left + real_per_change, right + real_per_change))
            # return real_per_change,(left+ real_per_change, right+ real_per_change)


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
        iter_time_list=[]
        iter_time=0
        for i in range(35):
            raw_output = []
            reader = csv.DictReader(cleandata, dialect=dialect)
            start = time.perf_counter()
            raw_output=[row for row in reader]
            end=time.perf_counter()
            print(">>>>time: ",end-start)
            if i<2:
                continue
            iter_time+=end-start
            iter_time_list.append(end-start)

        print(len(raw_output))
        return iter_time,iter_time_list

if __name__ == '__main__':
    # parse(data, raw=False, quiet=False)
    # with open(os.path.join(THIS_DIR, os.pardir, 'generic/csv-flyrna.json'), 'r', encoding='utf-8') as f:
    #     generic_csv_flyrna_json = json.loads(f.read())
    #, generic_csv_flyrna_json

    total_time_list=[]
    total_time = 0
    file_name="/generic/csv-deniro.csv"#"/generic/csv-cities.csv"#"/generic/csv-insurance.csv"#"/generic/csv-flyrna2.tsv"#"/generic/csv-flyrna.tsv"#"/generic/csv-flyrna2.tsv"#"/generic/systemctl-luf.out"#'/generic/csv-flyrna.tsv'
    print("".join([THIS_DIR, file_name]))
    '''
    for i in range(50):
        with open("".join([THIS_DIR, file_name]), 'r', encoding='utf-8') as f:
            generic_csv_flyrna = f.read()
            total_time_1,iter_time_list=parse(generic_csv_flyrna, quiet=True)
            total_time+=total_time_1
            total_time_list.append(iter_time_list)
    print(total_time)

    util.save_pkl(util.data_root+"performance/a_list_comprehension/test_some_test_cases/", file_name.split("/")[-1].split(".")[0], total_time_list)
    '''
    '''
    total_time_list = util.load_pkl(util.data_root+"performance/a_list_comprehension/test_some_test_cases/", file_name.split("/")[-1].split(".")[0])
    total_time_list_compli = util.load_pkl(util.data_root+"performance/a_list_comprehension/test_some_test_cases_complicate/", file_name.split("/")[-1].split(".")[0])
    total_time_list_info_dict={
        "time_list":[e[3:] for e in total_time_list_compli],"pythonic_time_list":[e[3:] for e in total_time_list]
    }
    get_performance_info(total_time_list_info_dict=total_time_list_info_dict, threshold=1, invocations=None, steps=100,
                         remove_outlier=False, factor=1.5)
    '''


    dis.dis(parse)
