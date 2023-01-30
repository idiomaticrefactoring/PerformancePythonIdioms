library(mgcv)
library(car)
#performance_listcomprehension_complete_feature_add_sizeof_corr_correct_perf_change_callNoAppend
#performance_listcomprehension_complete_feature_add_sizeof_corr_correct_perf_change
#performance_listcomprehension_complete_feature_add_sizeof_corr_correct_perf_change_callNoAppend_no_same_feature_vector
# data1<- read.csv(file="performance_listcomprehension_complete_feature_add_sizeof_corr_correct_perf_change_callNoAppend_no_same_feature_vector_add_FanIn_Call_ExpVa.csv", header=T)
# data1<- read.csv(file="performance_listcomprehension_complete_feature_add_sizeof_corr_correct_perf_change_callNoAppend_no_same_feature_vector.csv", header=T)
# performance_listcomprehension_complete_feature_add_sizeof_corr_correct_perf_change_callNoAppend_no_same_feature_vector_add_FanIn_Call_ExpVa_all
data1<- read.csv(file="performance_listcomprehension_complete_feature_add_sizeof_corr_correct_perf_change_callNoAppend_no_same_feature_vector_add_FanIn_Call_ExpVa_all.csv", header=T)
# data1
#cor(data1)+log(expVar+1)
alias( lm(log(perf_change) ~ log(num_ele+1)+log(Var+1)+log(num_param+1)+log(expVar_unique+1)+log(externalCall+1)+log(num_loop+1)+log(num_if+1)+log(num_if_else+1)+log(num_func_call+1)+log(num_var+1)+log(num_List+1)+log(num_Dict+1)+log(num_Tuple+1)+log(num_Subscript+1)+log(num_Attr+1)+log(num_constant+1)+log(num_line+1)+log(num_Operators+1)
           , data=data1) )
vif_test <- lm(log(perf_change) ~ log(num_ele+1)+log(Var+1)+log(num_param+1)+log(expVar_unique+1)+log(externalCall+1)+log(num_loop+1)+log(num_if+1)+log(num_if_else+1)+log(num_func_call+1)+log(num_var+1)+log(num_List+1)+log(num_Dict+1)+log(num_Tuple+1)+log(num_Subscript+1)+log(num_Attr+1)+log(num_constant+1)+log(num_line+1)+log(num_Operators+1)
                , data=data1)
vif(vif_test)
g <- gam(log(perf_change) ~ log(num_ele+1)+log(Var+1)+log(num_param+1)+log(expVar_unique+1)+log(externalCall+1)+log(num_loop+1)+log(num_if+1)+log(num_if_else+1)+log(num_func_call+1)+log(num_var+1)+log(num_List+1)+log(num_Dict+1)+log(num_Tuple+1)+log(num_Subscript+1)+log(num_Attr+1)+log(num_constant+1)+log(num_line+1)+log(num_Operators+1)
, data=data1, method = 'REML')

summary(g)
#+s(log(num_param+1))+s(log(expVar+1),k=6)+s(log(num_if+1),k=3)+s(log(num_if_else+1),k=3)+s(log(num_func_call+1),k=3)+s(log(num_var+1))+s(log(num_List+1))+s(log(num_Dict+1))+s(log(num_Tuple+1),k=4)+s(log(num_Subscript+1),k=6)+s(log(num_Attr+1),k=8)+s(log(num_constant+1),k=6)+s(log(num_line+1))+s(log(num_Operators+1),k=4)
g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(Var+1),k=8)+s(log(num_param+1),k=8)+s(log(expVar_unique+1),k=4)+s(log(externalCall+1),k=4)+s(log(num_loop+1),k=3)+s(log(num_if+1),k=3)+s(log(num_if_else+1),k=3)+s(log(num_func_call+1),k=5)+s(log(num_var+1))+log(num_List+1)+s(log(num_Subscript+1),k=6)+s(log(num_Attr+1),k=8)+s(log(num_constant+1),k=6)+s(log(num_line+1),k=4)+s(log(num_Operators+1),k=4), data=data1, method = 'REML')
summary(g)


g <- gam(log(perf_change) ~ log(num_ele+1)+log(Var+1)+log(num_param+1)+log(expVar_unique+1)+log(externalCall+1)+log(num_func_call+1)+log(num_var+1)+log(num_List+1)+log(num_Dict+1)+log(num_Tuple+1)+log(num_Subscript+1)+log(num_Attr+1)+log(num_constant+1)+log(num_line+1)+log(num_Operators+1)
, data=data1, method = 'REML')

summary(g)


g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(Var+1),k=8)+s(log(num_param+1),k=8)+s(log(expVar_unique+1),k=4)+s(log(externalCall+1),k=4)+s(log(num_func_call+1),k=5)+s(log(num_var+1))+log(num_List+1)+s(log(num_Subscript+1),k=6)+s(log(num_constant+1),k=6)+s(log(num_Attr+1),k=8)+s(log(num_line+1),k=4)+s(log(num_Operators+1),k=4), data=data1, method = 'REML')
summary(g)

g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(num_param+1),k=8)+s(log(expVar_unique+1),k=4)+s(log(num_func_call+1),k=5)+s(log(num_Subscript+1),k=6)+s(log(num_constant+1),k=6)+s(log(num_line+1),k=4)+s(log(num_Operators+1),k=4), data=data1, method = 'REML')
summary(g)
#no num_func_call
g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(num_param+1),k=8)+s(log(expVar_unique+1),k=4)+s(log(num_Subscript+1),k=6)+s(log(num_constant+1),k=6)+s(log(num_line+1),k=4)+s(log(num_Operators+1),k=4), data=data1, method = 'REML')
summary(g)
#

# g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(num_func_call+1),k=5)+s(log(num_var+1))+log(num_List+1)+s(log(num_Subscript+1),k=6)+s(log(num_Attr+1),k=8)+s(log(num_constant+1),k=6)+s(log(num_Operators+1),k=4), data=data1, method = 'REML')
# summary(g)

#+log(num_List+1)
# g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(num_func_call+1),k=5)+s(log(num_var+1))+s(log(num_Subscript+1),k=6)+s(log(num_Attr+1),k=8)+s(log(num_constant+1),k=6)+s(log(num_Operators+1),k=4), data=data1, method = 'REML')
# summary(g)

layout(matrix(1:1, nrow = 1))
plot(g, shade = TRUE)
plot(g, select = 2, pch = 20, shade = TRUE, residuals = TRUE)

# AIC(g)