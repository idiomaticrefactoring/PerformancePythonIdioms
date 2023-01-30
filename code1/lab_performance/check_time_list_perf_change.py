import time

import numpy as np, scipy.stats as st
import sys,ast,os,csv,time,copy

import subprocess

import scipy.stats

code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"wrap_refactoring/")
import refactor_list_comprehension
import performance_replace_content_by_ast_time_percounter
import lab_performance_util
import util
from lab_code_info import LabCodeInfo
import pandas as pd
import numpy as np

from math import log
import scipy as sp

from scipy import stats

#from sklearn import preprocessing
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

#from sklearn.cross_validation import train_test_split

import statsmodels.formula.api as smf
import seaborn as sns

import warnings


if __name__ == '__main__':
    bench_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks/final_stable/"
    bench_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks_mod/prefined_cpus_remain_code/"

    mean_perf_change_list=[]
    feature_list=[]
    for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
        print("file_name: ",file_name)
        file_name_no_suffix = file_name[:-4]
        lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
        lab_code_info: LabCodeInfo
        # print("code path: ",lab_code_info.file_path)
        invocations, iterations, num_add_ele = lab_code_info.invocations, lab_code_info.iterations, lab_code_info.num_add_ele
        num_for, num_if, num_if_else, e_input = file_name_no_suffix.split("_")
        # print("num_for, num_if, num_if_else, e_input: ",num_for, num_if, num_if_else, e_input)
        # dict_features=lab_code_info.get_features()

        # get number of iterations of each invocation reach at a stable state from 10 invocations
        lab_code_info.get_performance_stable_iter_invo_info()
        '''
        # get performance change and confidence interval
        mean_perf_change, left,right=lab_code_info.get_performance_info()
        # print(lab_code_info.get_features())
        # print(lab_code_info.get_performance_info())
        mean_perf_change_list.append(mean_perf_change)
        # feature_list.append(dict_features)
        # break
        '''



