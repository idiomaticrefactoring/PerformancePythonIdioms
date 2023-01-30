library(mgcv)
# install.packages("car",dependencies=TRUE)
# update.packages(checkBuilt=TRUE, ask=FALSE)#https://stackoverflow.com/questions/54669173/error-package-digest-was-installed-by-an-r-version-with-different-internals
# install.packages("car",dependencies=TRUE)
library(car)

pre_path="../../../data/lab_performance/for_else_benchmarks/csv/train_data_loop_else.csv"
data1<- read.csv(file=pre_path, header=T)#labperformance_listcomprehension_complete_feature
# data1
#        #dict_corr_num:  [('num_Keywords', 1), ('num_ele', 1), ('num_if', 1), ('num_if_else', 1), ('num_loop', 1), ('perf_change', 1)]

# check collineation 'num_for', 'num_if', 'num_if_else', 'num_ele' +log(num_func_call+1)
alias( lm(log(perf_change) ~ node_kind + branch_through_break + log(num_ele) + context+ has_else
           , data=data1) )

vif_test <- lm(log(perf_change) ~ node_kind + branch_through_break + log(num_ele) + context+ has_else
                , data=data1)
vif(vif_test)

g <- gam(log(perf_change) ~  node_kind + branch_through_break + log(num_ele) + context+ has_else  , data=data1,
         method = 'REML')

summary(g)
g <- gam(log(perf_change) ~  node_kind + branch_through_break + log(num_ele) + context+ has_else  , data=data1,
         method = 'REML')

summary(g)
g <- gam(log(perf_change) ~  node_kind + branch_through_break + s(log(num_ele), k = 5) + context+ has_else  , data=data1,
         method = 'REML')

summary(g)

#  [1] "file_html"            "code_str"             "RCIW"
#  [4] "perf_change_right"    "perf_change_left"     "perf_change"
#  [7] "kind"                 "node_kind"            "branch_through_break"
# [10] "has_else"             "num_ele"              "context"
colnames(data1)
# colnames(data1)[8] <- "size"
# colnames(data1)[9] <- "numFor"
colnames(data1)[9] <- "isBreak"
colnames(data1)[11] <- "size"
colnames(data1)[12] <- "scope"
g <- gam(log(perf_change) ~ as.factor(node_kind) + as.factor(isBreak) +s(log(size+1), k = 5)+ as.factor(scope)+ as.factor(has_else), data=data1,
         method = 'REML')
# g <- gam(log(perf_change) ~ num_loop + num_if  +s(log(num_ele+1))+ context, data=data1,
#          method = 'REML')
# summary(g)
# g <- gam(log(perf_change) ~ s(numFor,k=3) + s(numIf,k=3) + s(numIfElse,k=3) +s(log(size+1))+ as.factor(scope), data=data1,
#          method = 'REML')
# summary(g)
par(pin = c(3,2))
plot(g,all.terms = TRUE,trans = exp,ylab="performance change",tck = 0.02,nx = 5, ny = 3)#,2:1 ,pages=1,1:4 ,rug=FALSE

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