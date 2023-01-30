import time
import sys,ast,os,csv,time,copy
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"wrap_refactoring/")

import util,performance_util

feature_info_dir = util.data_root + "lab_performance/feature/list_compre_benchmarks/"
feature_file_name = "list_comprehension_original_complete_features"
dict_pd = util.load_pkl(feature_info_dir, feature_file_name)
key_list=[]
for key in dict_pd:
    if len(set(dict_pd[key]))<=1 or key=="num_Keywords_diff":
        # print(key)
        continue
    print(">>>>>key: ",key)
    key_list.append(key)
    print(dict_pd[key])
feature_list=["log("+key+"+100)" for key in key_list if key!="perf_change"]
feature_str="+".join(feature_list)
s_feature_list=["s(log("+key+"+100))" for key in key_list if key!="perf_change"]
s_feature_str="+".join(s_feature_list)

content=f'library(mgcv)\n\
library(car)\n\
data1<- read.csv(file="labperformance_listcomprehension_complete_feature.csv", header=T)\n\
# data1\n\
alias( lm(log(perf_change) ~ {feature_str}\n\
           , data=data1) )\n\
vif_test <- lm(log(perf_change) ~ {feature_str} \n\
                , data=data1)\n\
vif(vif_test)\n\
g <- gam(log(perf_change) ~ {feature_str}\n\
, data=data1, method = \'REML\')\n\
\n\
summary(g)\n\
\n\
g <- gam(log(perf_change) ~ {s_feature_str}, data=data1, method = \'REML\')\n\
    ,data=data1, method = \'REML\')\n\
summary(g)\n\
layout(matrix(1:1, nrow = 1))\n\
plot(g, shade = TRUE)\n\
plot(g, select = 2, pch = 20, shade = TRUE, residuals = TRUE)\n\
\n\
# AIC(g)\
'
util.save_file(code_dir+"lab_performance/","analysis_log_R_complete_feature",content=content,format=".R")
print("save success")