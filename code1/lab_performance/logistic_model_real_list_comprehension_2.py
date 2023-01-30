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
# pd.set_option('display.height', 1000)
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
import numpy as np

from math import log
import scipy as sp

from scipy import stats

from sklearn import preprocessing
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

#from sklearn.cross_validation import train_test_split

import statsmodels.formula.api as smf
import seaborn as sns

import warnings
if __name__ == '__main__':

        bench_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks/final_stable/"
        feature_info_dir=util.data_root + "lab_performance/feature/list_compre_benchmarks/"
        feature_file_name="list_comprehension"
        feature_file_name="list_comprehension_original"
        dict_pd= dict()
        #'''
        for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
                print("file_name: ", file_name)
                file_name_no_suffix = file_name[:-4]
                lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
                lab_code_info: LabCodeInfo
                # print("code path: ",lab_code_info.file_path)
                invocations, iterations, num_add_ele = lab_code_info.invocations, lab_code_info.iterations, lab_code_info.num_add_ele
                num_for, num_if, num_if_else, e_input = file_name_no_suffix.split("_")
                # print("num_for, num_if, num_if_else, e_input: ",num_for, num_if, num_if_else, e_input)
                dict_features = lab_code_info.get_features()
                mean_perf_change, left, right = lab_code_info.get_performance_info()
                for fea in dict_features:
                        ele = dict_features[fea]#np.log(dict_features[fea])
                        if fea not in dict_pd:

                                dict_pd[fea]=[ele]
                        else:
                                dict_pd[fea].append(ele)
                if "perf_change" not in dict_pd:
                        dict_pd["perf_change"]=[mean_perf_change]
                else:
                        dict_pd["perf_change"].append(mean_perf_change)
        # util.save_pkl(feature_info_dir, feature_file_name, dict_pd)
        util.save_pkl(feature_info_dir, feature_file_name, dict_pd)
        #'''

        dict_pd = util.load_pkl(feature_info_dir, feature_file_name)
        # dict_pd["perf_change"] = np.log(dict_pd["perf_change"])
        stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)
        # warnings.filterwarnings(action='once')
        warnings.filterwarnings(action='default')
        # load Data
        dataMain = pd.DataFrame(data=dict_pd)
        # Remove infinites and NAs
        dataMain = dataMain.replace([np.inf, -np.inf], np.nan)
        dataMain = dataMain.fillna(0)
        print(dataMain)
        #https://stackabuse.com/calculating-spearmans-rank-correlation-coefficient-in-python-with-pandas/
        my_r = dataMain.corr(method="spearman")
        print("spearman")
        print(my_r.to_string())#https://stackoverflow.com/questions/19124601/pretty-print-an-entire-pandas-series-dataframe
        dataMain.drop(columns=['num_func_call'])
        dataMain["perf_change"] = np.divide(dataMain["perf_change"] - dataMain["perf_change"].min(),
                                      dataMain["perf_change"].max() - dataMain["perf_change"].min())

        #'''
        # Shape of the data
        print(dataMain.shape)
        # Statistics on the data
        #print(dataMain.describe().T)

        # elect_lg.glm <- glm(Winner ~ lg_Population + lg_PovertyPercent + lg_EDU_HSDiploma +
        #      lg_EDU_SomeCollegeorAS + lg_EDU_BSorHigher + lg_UnemploymentRate +
        #      lg_Married + lg_HHMeanIncome + lg_Diabetes + lg_Inactivity +
        #      lg_OpioidRx, family = binomial, data = data.Main)
        #https://stackoverflow.com/questions/31322370/valueerror-endog-must-be-in-the-unit-interval
        results = smf.logit('perf_change ~ num_for \
                            + num_if \
                            + num_if_else \
                            + num_ele', data=dataMain).fit()
        print(results.summary())
        #'''