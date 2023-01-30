library(mgcv)
# install.packages("car",dependencies=TRUE)
# update.packages(checkBuilt=TRUE, ask=FALSE)#https://stackoverflow.com/questions/54669173/error-package-digest-was-installed-by-an-r-version-with-different-internals
# install.packages("car",dependencies=TRUE)
library(car)

pre_path="../../../data/performance/a_multi_assign/csv/train_data_multi_assign.csv"
data1<- read.csv(file=pre_path, header=T)#labperformance_listcomprehension_complete_feature
# data1
#        #dict_corr_num:  [('num_Keywords', 1), ('num_ele', 1), ('num_if', 1), ('num_if_else', 1), ('num_loop', 1), ('perf_change', 1)]

# check collineation 'num_for', 'num_if', 'num_if_else', 'num_ele' +log(num_func_call+1)
alias( lm(log(perf_change) ~ log(num_assign_node) + log(is_const+1)+log(is_swap+1)
           , data=data1) )

vif_test <- lm(log(perf_change) ~ log(num_assign_node) + log(is_const+1)+log(is_swap+1)
                , data=data1)
vif(vif_test)

g <- gam(log(perf_change) ~  log(num_assign_node) +  log(is_const+1)+log(is_swap+1) , data=data1,
         method = 'REML')

summary(g)


g <- gam(log(perf_change) ~  log(num_assign_node) +  log(is_const+1)+log(is_swap+1)  , data=data1,
         method = 'REML')

summary(g)

g <- gam(log(perf_change) ~  s(log(num_assign_node),k=6) +  log(is_const+1)+log(is_swap+1) , data=data1,
 method = 'REML')
#
summary(g)
g <- gam(log(perf_change) ~  s(log(num_assign_node),k=6) +  as.factor(is_const)+as.factor(is_swap) , data=data1,
 method = 'REML')
#
summary(g)
# g <- gam(log(perf_change) ~  s(log(num_assign_node+1), k = 8) +  log(type_data_input+1) +  context + swap_flag , data=data1,
#          method = 'REML')
#
# summary(g)
#
# g <- gam(log(perf_change) ~ s(log(num_loop+1), k = 4)+s(log(num_if+1), k = 5)+s(log(num_if_else+1), k = 5)+s(log(num_ele+1)), data=data1,
#          method = 'REML')
# summary(g)
#
# g <- gam(log(perf_change) ~ s(log(num_if+1), k = 5)+s(log(num_if_else+1), k = 5)+s(log(num_ele+1)), data=data1,
#          method = 'REML')
# summary(g)
#
# layout(matrix(1:1, nrow = 1))
# plot(g, shade = TRUE)
# plot(g, select = 2, pch = 20, shade = TRUE, residuals = TRUE)
#
# AIC(g)