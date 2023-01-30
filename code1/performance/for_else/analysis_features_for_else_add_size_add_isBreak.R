library(mgcv)
# install.packages("car",dependencies=TRUE)
# update.packages(checkBuilt=TRUE, ask=FALSE)#https://stackoverflow.com/questions/54669173/error-package-digest-was-installed-by-an-r-version-with-different-internals
# install.packages("car",dependencies=TRUE)
library(car)

pre_path= "../../../data/performance/a_for_else/csv/train_data_a_for_else_add_size_add_isBreak.csv"

data1<- read.csv(file=pre_path, header=T)#labperformance_listcomprehension_complete_feature
# data1
#        #dict_corr_num:  [('num_Keywords', 1), ('num_ele', 1), ('num_if', 1), ('num_if_else', 1), ('num_loop', 1), ('perf_change', 1)]

# check collineation 'num_for', 'num_if', 'num_if_else', 'num_ele' +log(num_func_call+1)

alias( lm(log(perf_change) ~ node_kind  + log(has_else+1)+log(size_data+1)
           , data=data1) )

vif_test <- lm(log(perf_change) ~node_kind  + log(has_else+1)+log(size_data+1)
                , data=data1)
vif(vif_test)

g <- gam(log(perf_change) ~  node_kind  + log(has_else+1)+log(size_data+1)  , data=data1,
         method = 'REML')

summary(g)
g <- gam(log(perf_change) ~  node_kind  + log(has_else+1)+log(size_data+1) , data=data1,
         method = 'REML')

summary(g)
g <- gam(log(perf_change) ~  node_kind  + log(has_else+1) +s(log(size_data+1)) , data=data1,
         method = 'REML')

summary(g)

g <- gam(log(perf_change) ~  as.factor(node_kind)  + as.factor(has_else) +s(log(size_data+1))+as.factor(is_break) , data=data1,
         method = 'REML')

summary(g)


# alias( lm(log(perf_change) ~ node_kind + branch_through_break + log(num_ele) + context+ has_else
#            , data=data1) )
#
# vif_test <- lm(log(perf_change) ~ node_kind + branch_through_break + log(num_ele) + context+ has_else
#                 , data=data1)
# vif(vif_test)
#
# g <- gam(log(perf_change) ~  node_kind + branch_through_break + log(num_ele) + context+ has_else  , data=data1,
#          method = 'REML')
#
# summary(g)
# g <- gam(log(perf_change) ~  node_kind + branch_through_break + log(num_ele) + context+ has_else  , data=data1,
#          method = 'REML')
#
# summary(g)
# g <- gam(log(perf_change) ~  node_kind + branch_through_break + s(log(num_ele), k = 5) + context+ has_else  , data=data1,
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