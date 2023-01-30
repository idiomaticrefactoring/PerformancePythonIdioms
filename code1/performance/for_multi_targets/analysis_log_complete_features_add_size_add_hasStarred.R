library(mgcv)
# install.packages("car",dependencies=TRUE)
# update.packages(checkBuilt=TRUE, ask=FALSE)#https://stackoverflow.com/questions/54669173/error-package-digest-was-installed-by-an-r-version-with-different-internals
# install.packages("car",dependencies=TRUE)
library(car)
data1<- read.csv(file="../../../data/performance/a_for_multi_tar_single_3_new/csv/train_data_for_multi_tar_add_size_data_add_hasStarred.csv", header=T)


# data1

# check collineation 'num_for', 'num_if', 'num_if_else', 'num_ele' +log(num_func_call+1)+log(subs_unpack_ratio)log(num_star+1)+log(num_iter_unpack)
alias( lm(log(perf_change) ~  log(num_unpack+1) +log( num_subscript+1)+log(size_data+1)+log(hasStarred+1)
           , data=data1) )# + dim_subscript log(num_star+1)+

vif_test <- lm(log(perf_change) ~  log(num_unpack+1) + log( num_subscript+1)+log(size_data+1)+log(hasStarred+1)
                , data=data1)#log(num_star+1)+
vif(vif_test)

g <- gam(log(perf_change) ~  log(num_unpack+1) + log( num_subscript+1)+log(size_data+1)+log(hasStarred+1) , data=data1,
         method = 'REML')#+ dim_subscript  log(num_star+1)+
summary(g)
g <- gam(log(perf_change) ~  log(num_unpack+1) + log( num_subscript+1) +log(size_data+1)+log(hasStarred+1) , data=data1,
         method = 'REML')#+ dim_subscript log(num_star+1)+

summary(g)

g <- gam(log(perf_change) ~  s(log(num_unpack+1),k=3) + s(log( num_subscript+1),k=3)+s(log(size_data+1),k=5)+log(hasStarred+1)  , data=data1,
         method = 'REML')#+ dim_subscript log(num_star+1)+

summary(g)

g <- gam(log(perf_change) ~  s(log(num_unpack+1),k=3) + s(log( num_subscript+1),k=3)+s(log(size_data+1),k=5)+as.factor(hasStarred)  , data=data1,
         method = 'REML')#+ dim_subscript log(num_star+1)+

summary(g)

# #
# g <- gam(log(perf_change) ~ num_loop + num_if + num_if_else +s(log(num_ele+1))+ context, data=data1,
#          method = 'REML')
# summary(g)
#
# summary(g)
layout(matrix(1:1, nrow = 1))
plot(g, shade = TRUE)
plot(g, select = 2, pch = 20, shade = TRUE, residuals = TRUE)

# AIC(g)