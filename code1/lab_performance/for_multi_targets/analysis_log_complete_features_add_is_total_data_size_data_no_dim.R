library(mgcv)
# install.packages("car",dependencies=TRUE)
# update.packages(checkBuilt=TRUE, ask=FALSE)#https://stackoverflow.com/questions/54669173/error-package-digest-was-installed-by-an-r-version-with-different-internals
# install.packages("car",dependencies=TRUE)
library(car)
data1<- read.csv(file="../../../data/lab_performance/for_multi_targets_benchmarks/csv/for_multi_targets.csv", header=T)
# data1

# check collineation 'num_for', 'num_if', 'num_if_else', 'num_ele' +log(num_func_call+1)+log(subs_unpack_ratio)log(num_star+1)+log(num_iter_unpack)
alias( lm(log(perf_change) ~ log(size_data)+ log(num_unpack) + num_subscript + is_total_data+context
           , data=data1) )#+log(num_star+1)

vif_test <- lm(log(perf_change) ~ log(size_data)+ log(num_unpack) + num_subscript  + is_total_data+context
                , data=data1)##+log(num_star+1)
vif(vif_test)
g <- gam(log(perf_change) ~   log(size_data)+ log(num_unpack) + num_subscript  +context, data=data1,
         method = 'REML')#+log(num_star+1)

summary(g)
g <- gam(log(perf_change) ~   log(size_data)+ log(num_unpack) + num_subscript +context, data=data1,
         method = 'REML')#+log(num_star+1)

summary(g)
g <- gam(log(perf_change) ~   s(log(size_data),k=3)+ s(log(num_unpack),k=3) + num_subscript +context, data=data1,
         method = 'REML')#+log(num_star+1)

summary(g)
g <- gam(log(perf_change) ~   log(size_data)+ log(num_unpack) + num_subscript  + is_total_data+context, data=data1,
         method = 'REML')#+log(num_star+1)

summary(g)
g <- gam(log(perf_change) ~   log(size_data)+ log(num_unpack) + num_subscript  + is_total_data+context, data=data1,
         method = 'REML')#+log(num_star+1)

summary(g)
g <- gam(log(perf_change) ~   s(log(size_data),k=6)+ s(log(num_unpack),k=5 )+ s( log(num_subscript),k=5)  + as.factor(is_total_data)+as.factor(context), data=data1,
         method = 'REML')#+log(num_star+1)
summary(g)
g <- gam(log(perf_change) ~   s(log(size_data),k=6)+ s(log(num_unpack),k=5 )+ s( log(num_subscript),k=5) +as.factor(context), data=data1,
         method = 'REML')#+log(num_star+1)
summary(g)
g <- gam(log(perf_change) ~    s(log(num_unpack),k=5 )+ s( log(num_subscript),k=5)  + as.factor(is_total_data)+as.factor(context), data=data1,
         method = 'REML')#+log(num_star+1)
summary(g)
# colnames(data1)
# colnames(data1)[8] <- "numTarget"
# colnames(data1)[13] <- "size"
# colnames(data1)[12] <- "scope"
# g <- gam(log(perf_change) ~ s(log(size),k=6)+ s(log(numTarget),k=5 )+ s( log(num_subscript),k=5)  + as.factor(is_total_data)+as.factor(scope), data=data1,
#          method = 'REML')
# summary(g)
#
#
# data1<- read.csv(file="/data/zejun/smp/data/lab_performance/list_compre_benchmarks_fun_and_Nfunc_once_again/csv/train_data_list_compre.csv", header=T)
# colnames(data1)
# # colnames(data1)[6] <- "performance change"
# colnames(data1)[8] <- "size"analysis_log_complete_features_add_is_total_data_size_data_no_dim.R
# colnames(data1)[9] <- "numFor"
# colnames(data1)[10] <- "numIf"
# colnames(data1)[11] <- "numIfElse"
# colnames(data1)[12] <- "scope"
# colnames(data1)
# g <- gam(log(perf_change) ~ s(numFor,k=3) + s(numIf,k=3) + s(numIfElse,k=3) +s(log(size+1))+ as.factor(scope), data=data1,
#          method = 'REML')
# summary(g)
# #
# g <- gam(log(perf_change) ~ num_loop + num_if + num_if_else +s(log(num_ele+1))+ context, data=data1,
#          method = 'REML')
# summary(g)
#
# summary(g)
# layout(matrix(1:1, nrow = 1))
# plot(g,all.terms = TRUE,trans = exp)
par(pin = c(3,2))
plot(g,all.terms = TRUE,trans = exp,ylab="performance change",tck = 0.02,nx = 5, ny = 3)#,2:1 ,pages=1,1:4 ,rug=FALSE

# plot(g, shade = TRUE)
# plot(g, select = 2, pch = 20, shade = TRUE, residuals = TRUE)

# AIC(g)