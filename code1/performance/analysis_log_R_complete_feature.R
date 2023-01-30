library(mgcv)
library(car)
data1<- read.csv(file="performance_listcomprehension_complete_feature_corr.csv", header=T)
# data1
cor(data1)
alias( lm(log(perf_change) ~ log(num_ele+1)+log(num_loop+1)+log(num_if+1)+log(num_if_else+1)+log(num_func_call+1)+log(num_List+1)+log(num_Dict+1)+log(num_Tuple+1)+log(num_Subscript+1)+log(num_Attr+1)+log(num_constant+1)+log(num_line+1)+log(num_Keywords+1)+log(num_Operators+1)
           , data=data1) )
vif_test <- lm(log(perf_change) ~ log(num_ele+1)+log(num_loop+1)+log(num_if+1)+log(num_if_else+1)+log(num_func_call+1)+log(num_List+1)+log(num_Dict+1)+log(num_Tuple+1)+log(num_Subscript+1)+log(num_Attr+1)+log(num_constant+1)+log(num_line+1)+log(num_Keywords+1)+log(num_Operators+1) 
                , data=data1)
vif(vif_test)
#+log(num_loop+1)+log(num_if+1)+log(num_if_else+1)+log(num_line+1)

g <- gam(log(perf_change) ~ log(num_ele+1)+log(num_func_call+1)+log(num_List+1)+log(num_Dict+1)+log(num_Tuple+1)+log(num_Subscript+1)+log(num_Attr+1)+log(num_constant+1)+log(num_Keywords+1)+log(num_Operators+1)
, data=data1, method = 'REML')

summary(g)
# g <- gam(log(perf_change) ~ log(num_ele+1)+log(num_List+1)+log(num_Dict+1)+log(num_Tuple+1)+log(num_Subscript+1)+log(num_Attr+1)+log(num_constant+1)+log(num_Keywords+1)+log(num_Operators+1)
# , data=data1, method = 'REML')
#
# summary(g)

# g <- gam(log(perf_change) ~ log(num_ele+1)+log(num_Dict+1)+log(num_Tuple+1)+log(num_Subscript+1)+log(num_Attr+1)+log(num_constant+1)+log(num_Keywords+1)+log(num_Operators+1)
# , data=data1, method = 'REML')
#
# summary(g)

# g <- gam(log(perf_change) ~ log(num_ele+1)+log(num_Tuple+1)+log(num_Subscript+1)+log(num_Attr+1)+log(num_constant+1)+log(num_Keywords+1)+log(num_Operators+1)
# , data=data1, method = 'REML')
#
# summary(g)

# g <- gam(log(perf_change) ~ log(num_ele+1)+log(num_Tuple+1)+log(num_Subscript+1)+log(num_Attr+1)+log(num_constant+1)+log(num_Operators+1)
# , data=data1, method = 'REML')
#
# summary(g)

g <- gam(log(perf_change) ~ log(num_ele+1)+log(num_Tuple+1)+log(num_Subscript+1)+log(num_constant+1)+log(num_Operators+1)
, data=data1, method = 'REML')

summary(g)
# g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(num_loop+1))+s(log(num_if+1))+s(log(num_if_else+1))+s(log(num_func_call+1))+s(log(num_List+1))+s(log(num_Dict+1))+s(log(num_Tuple+1))+s(log(num_Subscript+1))+s(log(num_Attr+1))+s(log(num_constant+1))+s(log(num_line+1))+s(log(num_Keywords+1))+s(log(num_Operators+1)), data=data1, method = 'REML')
#     ,data=data1, method = 'REML')
#+s(log(num_loop+1),k=3)+s(log(num_if+1),k=3)+s(log(num_if_else+1),k=3)+s(log(num_line+1),k=4)
#+s(log(num_if+1))+s(log(num_if_else+1))
g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(num_loop+1),k=3)+s(log(num_if+1),k=3)+s(log(num_if_else+1),k=3)+s(log(num_Subscript+1),k=6)+s(log(num_Tuple+1),k=4)+s(log(num_constant+1),k=6)+s(log(num_Operators+1),k=4), data=data1, method = 'REML')

summary(g)

g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(num_Subscript+1),k=6)+s(log(num_Tuple+1),k=4)+s(log(num_constant+1),k=6)+s(log(num_Operators+1),k=4), data=data1, method = 'REML')

summary(g)

g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(num_func_call+1),k=6)+log(num_List+1)+log(num_Dict+1)+s(log(num_Tuple+1),k=4)+s(log(num_Subscript+1),k=6)+s(log(num_Attr+1),k=8)+s(log(num_constant+1),k=7)+s(log(num_Keywords+1),k=9)+s(log(num_Operators+1),k=3)+s(log(num_line+1),k=4), data=data1, method = 'REML')

summary(g)

g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(num_func_call+1),k=6)+log(num_List+1)+log(num_Dict+1)+s(log(num_Tuple+1),k=4)+s(log(num_Subscript+1),k=6)+s(log(num_Attr+1),k=8)+s(log(num_constant+1),k=7)+s(log(num_Keywords+1),k=9)+s(log(num_line+1),k=4), data=data1, method = 'REML')

summary(g)

g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(num_func_call+1),k=6)+log(num_List+1)+log(num_Dict+1)+s(log(num_Tuple+1),k=4)+s(log(num_Subscript+1),k=6)+s(log(num_Attr+1),k=8)+s(log(num_constant+1),k=7)+s(log(num_line+1),k=4), data=data1, method = 'REML')

summary(g)

g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(num_func_call+1),k=6)+log(num_List+1)+log(num_Dict+1)+s(log(num_Subscript+1),k=6)+s(log(num_Attr+1),k=8)+s(log(num_constant+1),k=7)+s(log(num_line+1),k=4), data=data1, method = 'REML')

summary(g)

g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(num_func_call+1),k=6)+log(num_List+1)+log(num_Dict+1)+s(log(num_Subscript+1),k=6)+s(log(num_Attr+1),k=8)+s(log(num_line+1),k=4), data=data1, method = 'REML')

summary(g)

g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(num_Subscript+1),k=6)+s(log(num_Attr+1),k=8)+s(log(num_line+1),k=4), data=data1, method = 'REML')

summary(g)

#+s(log(num_if+1))+s(log(num_if_else+1))+
g <- gam(log(perf_change) ~ s(log(num_ele+1))+s(log(num_loop+1),k=3)+s(log(num_if+1),k=3)+s(log(num_if_else+1),k=3)+s(log(num_func_call+1),k=6)+log(num_List+1)+log(num_Dict+1)+s(log(num_Tuple+1),k=4)+s(log(num_Subscript+1),k=6)+s(log(num_Attr+1),k=8)+s(log(num_constant+1),k=7)+s(log(num_Keywords+1),k=9)+s(log(num_Operators+1),k=3)+s(log(num_line+1),k=4), data=data1, method = 'REML')

summary(g)
layout(matrix(1:1, nrow = 1))
plot(g, shade = TRUE)
plot(g, select = 2, pch = 20, shade = TRUE, residuals = TRUE)

# AIC(g)