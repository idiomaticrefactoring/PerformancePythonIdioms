library(mgcv)
# install.packages("car",dependencies=TRUE)
# update.packages(checkBuilt=TRUE, ask=FALSE)#https://stackoverflow.com/questions/54669173/error-package-digest-was-installed-by-an-r-version-with-different-internals
# install.packages("car",dependencies=TRUE)
library(car)

data1<- read.csv(file="../../../data/lab_performance/call_star_benchmarks/csv/train_data_call_star.csv", header=T)
# data1

# check collineation 'num_for', 'num_if', 'num_if_else', 'num_ele' +log(num_func_call+1)
alias( lm(log(perf_change) ~ log(num_ele) + log(num_subscript) + is_value_const + is_lower_0 + is_upper_len+is_step_1+context
           , data=data1) )

vif_test <- lm(log(perf_change) ~ log(num_ele) + log(num_subscript) + is_value_const + is_lower_0 + is_upper_len+is_step_1+context
                , data=data1)
vif(vif_test)

g <- gam(log(perf_change) ~   log(num_ele) + log(num_subscript) + is_value_const + is_lower_0 + is_upper_len+is_step_1+context, data=data1,
         method = 'REML')

summary(g)
plot(g,all.terms = TRUE)
# plot(g,all.terms = TRUE,trans = exp)
# plot_smooth(g,
#             transform = exp)
g <- gam(log(perf_change) ~   s(log(num_ele)) + s(log(num_subscript)) + is_value_const + is_lower_0 + is_upper_len+is_step_1+context, data=data1,
         method = 'REML')
summary(g)
# plot(g,all.terms = TRUE)
#
# summary(g)
# layout(matrix(1:1, nrow = 1))
# plot(g)
# plot(g, shade = TRUE)
# plot(g, select = 2, pch = 20, shade = TRUE, residuals = TRUE)


# #
# g <- gam(log(perf_change) ~ num_loop + num_if + num_if_else +s(log(num_ele+1))+ context, data=data1,
#          method = 'REML')
# summary(g)
#
# summary(g)


# AIC(g)