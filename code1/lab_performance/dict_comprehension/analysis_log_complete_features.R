library(mgcv)
# install.packages("car",dependencies=TRUE)
# update.packages(checkBuilt=TRUE, ask=FALSE)#https://stackoverflow.com/questions/54669173/error-package-digest-was-installed-by-an-r-version-with-different-internals
# install.packages("car",dependencies=TRUE)
library(car)
data1<- read.csv(file="../../../data/lab_performance/dict_compre_benchmarks/csv/train_data_dict_compre.csv", header=T)


# check collineation 'num_for', 'num_if', 'num_if_else', 'num_ele' +log(num_func_call+1)
alias( lm(log(perf_change) ~ num_loop + num_if + num_if_else + log(num_ele+1) + context
           , data=data1) )

vif_test <- lm(log(perf_change) ~ num_loop + num_if + num_if_else + log(num_ele+1) + context
                , data=data1)
vif(vif_test)

g <- gam(log(perf_change) ~   num_loop + num_if + num_if_else + log(num_ele+1)+ context, data=data1,
         method = 'REML')

summary(g)
#
g <- gam(log(perf_change) ~ num_loop + num_if + num_if_else +s(log(num_ele+1))+ context, data=data1,
         method = 'REML')
summary(g)
#  [1] "file_html"         "code_str"          "RCIW"
#  [4] "perf_change_right" "perf_change_left"  "perf_change"
#  [7] "kind"              "size"              "numFor"
# [10] "numIf"             "numIfElse"         "scope"

colnames(data1)[8] <- "size"
colnames(data1)[9] <- "numFor"
colnames(data1)[10] <- "numIf"
colnames(data1)[11] <- "numIfElse"
colnames(data1)[12] <- "scope"
colnames(data1)
g <- gam(log(perf_change) ~ s(numFor,k=3) + s(numIf,k=3) + s(numIfElse,k=3) +s(log(size+1))+ as.factor(scope), data=data1,
         method = 'REML')
# g <- gam(log(perf_change) ~ num_loop + num_if  +s(log(num_ele+1))+ context, data=data1,
#          method = 'REML')
# summary(g)
# g <- gam(log(perf_change) ~ s(numFor,k=3) + s(numIf,k=3) + s(numIfElse,k=3) +s(log(size+1))+ as.factor(scope), data=data1,
#          method = 'REML')
# summary(g)
par(pin = c(3,2))
plot(g,all.terms = TRUE,trans = exp,ylab="performance change",tck = 0.02,nx = 5, ny = 3)#,2:1 ,pages=1,1:4 ,rug=FALSE
# plot(g,all.terms = TRUE,trans = exp)
# plot(g,all.terms = TRUE,trans = exp)
#
# summary(g)
# layout(matrix(1:1, nrow = 1))
# plot(g, shade = TRUE)
# plot(g, select = 2, pch = 20, shade = TRUE, residuals = TRUE)

# AIC(g)