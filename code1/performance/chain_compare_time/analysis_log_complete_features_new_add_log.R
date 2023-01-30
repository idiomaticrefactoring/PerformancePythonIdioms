library(mgcv)
# install.packages("car",dependencies=TRUE)
# update.packages(checkBuilt=TRUE, ask=FALSE)#https://stackoverflow.com/questions/54669173/error-package-digest-was-installed-by-an-r-version-with-different-internals
# install.packages("car",dependencies=TRUE)
library(car)

data1<- read.csv(file="../../../data/performance/chain_compare/csv/sample_chain_compare_new_remove_reduandant.csv", header=T)

# data1

# check collineation 'num_for', 'num_if', 'num_if_else', 'num_ele' +log(num_func_call+1)
alias( lm(log(perf_change) ~ log(num_Eq+1) + log(num_NotEq+1) + log(num_Lt+1) + log(num_LtE+1) + log(num_Gt+1) + log(num_GtE+1) + log(num_Is+1) + log(num_IsNot+1) + log(num_In+1) + log(num_NotIn+1)
           , data=data1) )

vif_test <- lm(log(perf_change) ~log(num_Eq+1) + log(num_NotEq+1) + log(num_Lt+1) + log(num_LtE+1) + log(num_Gt+1) + log(num_GtE+1) + log(num_Is+1) + log(num_IsNot+1) + log(num_In+1) + log(num_NotIn+1)
                , data=data1)
vif(vif_test)

g <- gam(log(perf_change) ~  log(num_Eq+1) + log(num_NotEq+1) + log(num_Lt+1) + log(num_LtE+1) + log(num_Gt+1) + log(num_GtE+1) + log(num_Is+1) + log(num_IsNot+1) + log(num_In+1) + log(num_NotIn+1) , data=data1,
         method = 'REML')

summary(g)
g <- gam(log(perf_change) ~  log(num_Eq+1) + log(num_NotEq+1) + log(num_Lt+1) + log(num_LtE+1) + log(num_Gt+1) + log(num_GtE+1) + log(num_Is+1) + log(num_IsNot+1) + log(num_In+1) + log(num_NotIn+1) , data=data1,
         method = 'REML')

summary(g)
g <- gam(log(perf_change) ~  log(num_Eq+1) + log(num_NotEq+1) + log(num_Lt+1) + log(num_LtE+1) + log(num_Gt+1) + log(num_GtE+1) + log(num_Is+1) + log(num_IsNot+1) + s(log(num_In+1),k=3) + s(log(num_NotIn+1),k=3), data=data1,
         method = 'REML')

summary(g)
#+ s(log(num_NotEq+1), k = 4)+ s(log(num_Lt+1), k = 4)+ s(log(num_LtE+1), k = 4)+ s(log(num_Gt+1), k = 4)
#+ s(log(num_GtE+1), k = 4)+ s(log(num_Is+1), k = 4)+ s(log(num_IsNot+1), k = 4)+ s(log(num_In+1), k = 4)
#+ s(log(num_NotIn+1), k = 4)+ s(log(num_cmpop+1), k = 4)+
# + s(log(num_Lt+1), k = 3)+ s(log(num_LtE+1), k = 3)+ s(log(num_Gt+1), k = 3)
# + s(log(num_GtE+1), k = 3)+ s(log(num_Is+1), k = 3)+ s(log(num_IsNot+1), k = 3)+ s(log(num_In+1), k = 3)
# + s(log(num_NotIn+1), k = 3)
g <- gam(log(perf_change) ~ s(log(num_Eq+1), k = 4)+ s(log(num_NotEq+1), k = 4) + s(log(num_Lt+1), k = 4)+ s(log(num_LtE+1), k = 4)+ s(log(num_Gt+1), k = 4)
 + s(log(num_GtE+1), k = 4)+ s(log(num_Is+1), k = 4)+ s(log(num_IsNot+1), k = 4)+ s(log(num_In+1), k = 4)
 + s(log(num_NotIn+1), k = 4)+ s(log(num_cmpop+1),k=4)+ s(log(num_true+1),k=4)+context, data=data1,
         method = 'REML')
summary(g)
g <- gam(log(perf_change) ~ s(log(num_Eq+1), k = 3)+ s(log(num_NotEq+1), k = 3) + s(log(num_Lt+1), k = 3)+ s(log(num_LtE+1), k = 3)+ s(log(num_Gt+1), k = 3)
 + s(log(num_GtE+1), k = 3)+ s(log(num_Is+1), k = 3)+ s(log(num_IsNot+1), k = 3)+ s(log(num_In+1), k = 3)
 + s(log(num_NotIn+1), k = 3)+ s(log(num_cmpop),k=1)+ s(log(num_true+1))+context, data=data1,
         method = 'REML')
summary(g)
layout(matrix(1:1, nrow = 1))
plot(g, shade = TRUE)
plot(g, select = 2, pch = 20, shade = TRUE, residuals = TRUE)