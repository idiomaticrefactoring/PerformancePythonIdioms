library(mgcv)
# library(mgcViz)
# library(tidyverse)
# install.packages("mgcViz",dependencies=TRUE)
# library(caret)
# install.packages("car",dependencies=TRUE)
# update.packages(checkBuilt=TRUE, ask=FALSE)#https://stackoverflow.com/questions/54669173/error-package-digest-was-installed-by-an-r-version-with-different-internals
# install.packages("car",dependencies=TRUE)
library(car)

data1<- read.csv(file="../../data/lab_performance/list_compre_benchmarks_fun_and_Nfunc_once_again/csv/train_data_list_compre.csv", header=T)
# data1
log(10)
log(10)

# check collineation 'num_for', 'num_if', 'num_if_else', 'num_ele' +log(num_func_call+1)
alias( lm(log(perf_change) ~ num_loop + num_if + num_if_else + log(num_ele+1) + context
           , data=data1) )

vif_test <- lm(log(perf_change) ~ num_loop + num_if + num_if_else + log(num_ele+1) + context
                , data=data1)
vif(vif_test)
# gam1 <- train(
#   log(perf_change) ~ num_loop+ num_if + num_if_else + log(num_ele+1)+context ,
#   data = data1,
#   method = 'gamSpline'
# )
# gbmImp <- varImp(gam1, scale=TRUE)
# gbmImp
# warnings()
g <- gam(perf_change ~   num_loop + num_if + num_if_else + log(num_ele+1)+ context, data=data1,
         method = 'REML')

summary(g)

g <- gam(log(perf_change) ~   num_loop + num_if + num_if_else + log(num_ele+1)+ context, data=data1,
         method = 'REML')

summary(g)
# b <- getViz(g)
# check(b,
#       a.qq = list(method = "tnorm",
#                   a.cipoly = list(fill = "light blue")))

# plot(g,all.terms = TRUE,trans = exp)
#
g <- gam(log(perf_change) ~ s(num_loop,k=3) + num_if + num_if_else +s(log(num_ele+1))+ context, data=data1,
         method = 'REML')
summary(g)
g <- gam(log(perf_change) ~ s(num_loop,k=3) + s(num_if+1,k=3) + s(num_if_else+1,k=3) +s(log(num_ele+1))+ as.factor(context), data=data1,
         method = 'REML')
summary(g)
# data1 %>%rename(context = scope,num_ele = size,num_loop=numFor)
# dev.new(width = 550, height = 330, unit = "px")
colnames(data1)
# colnames(data1)[6] <- "performance change"
colnames(data1)[8] <- "size"
colnames(data1)[9] <- "numFor"
colnames(data1)[10] <- "numIf"
colnames(data1)[11] <- "numIfElse"
colnames(data1)[12] <- "scope"
colnames(data1)
g <- gam(log(perf_change) ~ s(numFor,k=3) + s(numIf,k=3) + s(numIfElse,k=3) +s(log(size+1))+ as.factor(scope), data=data1,
         method = 'REML')
summary(g)
# all.terms

# par(mfrow=c(3,2))
#https://blog.csdn.net/tandelin/article/details/94769728
#https://r-coder.com/plot-r/#Change_axis_scale_in_R
# x11(width = 10, height = 5)
par(pin = c(3,2))
plot(g,all.terms = TRUE,trans = exp,ylab="performance change",tck = 0.02,nx = 5, ny = 3)#,2:1 ,pages=1,1:4 ,rug=FALSE
# ggsave("test.2.pdf",p, width=3, height=3, units="in", scale=3)
# plot(g,all.terms = TRUE,trans = exp,xlab="log(size+1)",ylab="performance change",rug=FALSE)#,2:1

# plot(g,all.terms = TRUE,trans = exp,xlab="log(size+1)",ylab="performance change",rug=FALSE)#,2:1
g <- gam(perf_change ~ num_if + num_if_else +s(log(num_ele+1))+ context, data=data1,
         method = 'REML')
summary(g)
g <- gam(log(perf_change) ~ num_if + num_if_else +s(log(num_ele+1))+ context, data=data1,
         method = 'REML')
summary(g)

summary(g)
g <- gam(perf_change ~ num_if + num_if_else +s(log(num_ele+1))+ context, data=data1,
         family = Gamma(link = "log"),method = 'REML')
summary(g)
# plot(g,all.terms = TRUE,trans = exp,ylab="performance change")#

# g <- gam(log(perf_change) ~ s(log(num_ele+1))+ context, data=data1,
#          method = 'REML')
# summary(g)
# g <- gam(log(perf_change) ~ s(log(num_ele+1))+ context, data=data1,
#          method = 'REML')
# summary(g)


#
# summary(g)
# layout(matrix(1:1, nrow = 1))
# plot(g, shade = TRUE)
# plot(g, select = 2, pch = 20, shade = TRUE, residuals = TRUE)

# AIC(g)
#https://stackoverflow.com/questions/71173468/how-do-you-plot-smooth-components-of-different-gams-in-same-panel
# library("mgcv")
#
# # Dataset
# data("swiss")
#
# # GAM models
# fit1 <- gam(Fertility ~ s(Examination) + s(Education),
#             data = swiss, method = "REML")
# fit2 <- gam(Agriculture ~ s(Examination) + s(Education),
#             data = swiss, method = "REML")
#
# # create and object that contains the info to compare smooths
# comp <- compare_smooths(fit1, fit2)
#
# # plot
# draw(comp)