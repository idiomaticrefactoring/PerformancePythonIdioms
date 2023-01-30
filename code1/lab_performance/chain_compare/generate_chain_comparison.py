#https://stackoverflow.com/questions/48375753/why-are-chained-operator-expressions-slower-than-their-expanded-equivalent
a=1
a_1=1
op1_1=2
op1_2=4
b=2
b_1=2
c=3
d=4
e=5
f=6
g=7
ten=10
five=5
one=1
a_list=[2,3,1]

c=1.1
op2_1=2
op2_2=4
d=3.1
a_2=1.1
op1_1=2
op1_2=4
b_2=2.1
c_2=3.1
e_2=4.1
f_2=5.1
g_2=6.1
a_2_list=[2.1,3.1,1.1]
'''
1. 不同操作符的全部组合 > >= < <=; ==; in; not in; is; is not
2. False和True的不同
3. 不是常量全是变量的比较
4. 多个操作符的组合
'''
# 全是True的chain compare的81种> >= < <=; !=; ==; in; not in; is; is not的操作符组合

b>1 and b<3
b>1 and b<=3
e>1 and e>3
e>1 and e>=3
b>1 and b!=10
b>1 and b==2
b>1 and b in a_list
e>1 and e not in a_list
e>1 and e is 5
e>1 and e is not 0



b>=1 and b<3
b>=1 and b<=3
# e>=1 and e>3
e>=1 and e>=3
b>=1 and b!=10
b>=1 and b==2
b>=1 and b in a_list
e>=1 and e not in a_list
b>=1 and b is 2
b>=1 and b is not 0


a<=2 and a<3
a<=2 and a<=3
# a<=2 and a>3
# a<=2 and a>=3
a<=2 and a!=10
a<=2 and a==1
a<=2 and a in a_list
e<=10 and e not in a_list
a<=2 and a is 1
a<=2 and a is not 2

a<2 and a<3
# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
a<2 and a!=10
a<2 and a==1
a<2 and a in a_list
e<10 and e not in a_list
a<2 and a is 1
a<2 and a is not 1

b==2 and b!=10
# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
b==2 and b in a_list
e==5 and e not in a_list
b==2 and b is 2
b==2 and b is not 10



# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
b!=10 and b in a_list
e!=10 and e not in a_list
b!=10 and b is 2
b!=10 and b is not 10


b in a_list and b is 2
b in a_list and b is not 10

e not in a_list and e is 5
e not in a_list and e is not 10

a is 1 and a is not 10


# 第一个是False的chain compare的16种>,>=,<,<=的操作符组合
b>10 and b<3
b>10 and b<=3
e>10 and e>3
e>10 and e>=3
b>10 and b!=10
b>10 and b==2
b>10 and b in a_list
e>10 and e not in a_list
e>10 and e is 5
e>10 and e is not 0



b>=10 and b<3
b>=10 and b<=3
# e>=1 and e>3
e>=10 and e>=3
b>=10 and b!=10
b>=10 and b==2
b>=10 and b in a_list
e>=10 and e not in a_list
b>=10 and b is 2
b>=10 and b is not 0


a<=0 and a<3
a<=0 and a<=3
# a<=2 and a>3
# a<=2 and a>=3
a<=0 and a!=10
a<=0 and a==1
a<=0 and a in a_list
e<=0 and e not in a_list
a<=0 and a is 1
a<=0 and a is not 2

a<0 and a<3
# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
a<0 and a!=10
a<0 and a==1
a<0 and a in a_list
e<0 and e not in a_list
a<0 and a is 1
a<0 and a is not 1

b==10 and b!=10
# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
b==10 and b in a_list
e==10 and e not in a_list
b==10 and b is 2
b==10 and b is not 10



# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
b!=2 and b in a_list
e!=5 and e not in a_list
b!=2 and b is 2
b!=2 and b is not 10


e in a_list and e is 5
e in a_list and e is not 10

b not in a_list and b is 2
b not in a_list and b is not 10

b is 1 and b is not 10

# 第二个是False的chain compare的16种>,>=,<,<=的操作符组合
b>1 and b<0
b>1 and b<=0
e>1 and e>10
e>1 and e>=10
b>1 and b!=2
b>1 and b==10
e>1 and e in a_list
b>1 and b not in a_list
e>1 and e is 3
e>1 and e is not 5



b>=1 and b<0
b>=1 and b<=0
# e>=1 and e>3
e>=1 and e>=10
b>=1 and b!=2
b>=1 and b==3
e>=1 and e in a_list
b>=1 and b not in a_list
b>=1 and b is 10
b>=1 and b is not 2


a<=2 and a<0
a<=2 and a<=0
# a<=2 and a>3
# a<=2 and a>=3
a<=2 and a!=1
a<=2 and a==3
e<=10 and e in a_list
a<=10 and a not in a_list
a<=2 and a is 10
a<=2 and a is not 1

a<2 and a<0
# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
a<2 and a!=1
a<2 and a==10
e<10 and e in a_list
a<2 and a not in a_list
a<2 and a is 10
a<2 and a is not 1

b==2 and b!=10
# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
e==5 and e in a_list
b==2 and b not in a_list
b==2 and b is 10
b==2 and b is not 2



# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
e!=10 and e in a_list
b!=10 and b not in a_list
b!=10 and b is 10
b!=10 and b is not 2


b in a_list and b is 10
b in a_list and b is not 2

e not in a_list and e is 10
e not in a_list and e is not 5

a is 1 and a is not 1

# 全是True的chain compare的81种> >= < <=; !=; ==; in; not in; is; is not的操作符组合

b>one and b<three
b>one and b<=three
e>one and e>three
e>one and e>=three
b>one and b!=ten
b>one and b==two
b>one and b in a_list
e>one and e not in a_list
e>one and e is five
e>one and e is not three



b>=one and b<three
b>=one and b<=three
# e>=1 and e>3
e>=one and e>=three
b>=one and b!=ten
b>=one and b==two
b>=one and b in a_list
e>=one and e not in a_list
b>=one and b is two
b>=one and b is not three


a<=two and a<three
a<=two and a<=three
# a<=2 and a>3
# a<=2 and a>=3
a<=two and a!=ten
a<=two and a==one
a<=two and a in a_list
e<=ten and e not in a_list
a<=two and a is one
a<=two and a is not two

a<two and a<three
# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
a<two and a!=ten
a<two and a==one
a<two and a in a_list
e<ten and e not in a_list
a<two and a is one
a<two and a is not one

b==two and b!=ten
# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
b==two and b in a_list
e==five and e not in a_list
b==two and b is two
b==two and b is not ten



# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
b!=ten and b in a_list
e!=ten and e not in a_list
b!=ten and b is two
b!=ten and b is not ten


b in a_list and b is two
b in a_list and b is not ten

e not in a_list and e is five
e not in a_list and e is not ten

a is one and a is not ten


# 第一个是False的chain compare的16种>,>=,<,<=的操作符组合
b>ten and b<three
b>ten and b<=three
e>ten and e>three
e>ten and e>=three
b>ten and b!=ten
b>ten and b==one
b>ten and b in a_list
e>ten and e not in a_list
e>ten and e is five
e>ten and e is not three



b>=ten and b<three
b>=ten and b<=three
# e>=1 and e>3
e>=ten and e>=three
b>=ten and b!=ten
b>=ten and b==two
b>=ten and b in a_list
e>=ten and e not in a_list
b>=ten and b is two
b>=ten and b is not three


a<=zero and a<three
a<=zero and a<=three
# a<=2 and a>3
# a<=2 and a>=3
a<=zero and a!=three
a<=zero and a==one
a<=zero and a in a_list
e<=zero and e not in a_list
a<=zero and a is one
a<=zero and a is not three

a<zero and a<three
# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
a<zero and a!=three
a<zero and a==one
a<zero and a in a_list
e<zero and e not in a_list
a<zero and a is one
a<zero and a is not one

b==ten and b!=ten
# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
b==ten and b in a_list
e==ten and e not in a_list
b==ten and b is two
b==ten and b is not ten



# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
b!=two and b in a_list
e!=five and e not in a_list
b!=two and b is two
b!=two and b is not five


e in a_list and e is five
e in a_list and e is not ten

b not in a_list and b is two
b not in a_list and b is not ten

b is one and b is not one

# 第二个是False的chain compare的16种>,>=,<,<=的操作符组合
b>one and b<zero
b>one and b<=zero
e>one and e>ten
e>one and e>=ten
b>one and b!=two
b>one and b==ten
e>one and e in a_list
b>one and b not in a_list
e>one and e is three
e>one and e is not five



b>=one and b<zero
b>=one and b<=zero
# e>=1 and e>3
e>=one and e>=ten
b>=one and b!=two
b>=one and b==three
e>=one and e in a_list
b>=one and b not in a_list
b>=one and b is ten
b>=one and b is not two


a<=two and a<zero
a<=two and a<=zero
# a<=2 and a>3
# a<=2 and a>=3
a<=two and a!=one
a<=two and a==three
e<=ten and e in a_list
a<=ten and a not in a_list
a<=two and a is ten
a<=two and a is not one

a<two and a<zero
# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
a<two and a!=one
a<two and a==ten
e<ten and e in a_list
a<two and a not in a_list
a<two and a is ten
a<two and a is not one

b==two and b!=two
# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
e==five and e in a_list
b==two and b not in a_list
b==two and b is ten
b==two and b is not two



# a<2 and a<=3
# a<2 and a>3
# a<2 and a>=3
e!=ten and e in a_list
b!=ten and b not in a_list
b!=ten and b is ten
b!=ten and b is not two


b in a_list and b is ten
b in a_list and b is not two

e not in a_list and e is ten
e not in a_list and e is not five

a is one and a is not one


# 3 operator ;全是True的chain compare的81种 2个一样的> >= < <=; !=; ==; in; not in; is; is not的操作符组合
b>one and b<three and one>zero
b>one and b<=three and one>zero
e>one and e>three and one>zero
e>one and e>=three and one>zero
b>one and b!=ten and one>zero
b>one and b==two and one>zero
b>one and b in a_list and one>zero
e>one and e not in a_list and one>zero
e>one and e is five and one>zero
e>one and e is not three and one>zero

b>one and b<three and one>zero
b>one and b<=three and one>zero
e>one and e>three and one>zero
e>one and e>=three and one>zero
b>one and b!=ten and one>zero
b>one and b==two and one>zero
b>one and b in a_list and one>zero
e>one and e not in a_list and one>zero
e>one and e is five and one>zero
e>one and e is not three and one>zero



b>=one and b<three and one>=zero
b>=one and b<=three and one>=zero
e>=one and e>three and one>=zero
e>=one and e>=three and one>=zero
b>=one and b!=ten and one>=zero
b>=one and b==two and one>=zero
b>=one and b in a_list and one>=zero
e>=one and e not in a_list and one>=zero
b>=one and b is two and one>=zero
b>=one and b is not three and one>=zero


a<=two and a<three and two<=twenty
a<=two and a<=three  and two<=twenty
a<=two and a>three  and two<=twenty
a<=two and a>=three  and two<=twenty
a<=two and a!=ten  and two<=twenty
a<=two and a==one  and two<=twenty
a<=two and a in a_list  and two<=twenty
e<=ten and e not in a_list  and two<=twenty
a<=two and a is one  and two<=twenty
a<=two and a is not two  and two<=twenty

a<two and a<three and two<twenty
a<two and a<=three and two<twenty
a<two and a>zero and two<twenty
a<two and a>=zero and two<twenty
a<two and a!=ten and two<twenty
a<two and a==one and two<twenty
a<two and a in a_list and two<twenty
e<ten and e not in a_list and ten<twenty
a<two and a is one and two<twenty
a<two and a is not one and two<twenty

b==two and b<ten and two==two_2
b==two and b<=ten and two==two_2
b==two and b>one and two==two_2
b==two and b>=one and two==two_2
b==two and b==two_2 and two==two_2
b==two and b!=ten and two==two_2
b==two and b in a_list and two==two_2
e==five and e not in a_list and five==five_2
b==two and b is two and two==two_2
b==two and b is not ten and two==two_2



b!=ten and b <ten and ten!=two
b!=ten and b <=ten and ten!=two
b!=ten and b >one and ten!=two
b!=ten and b >=one and ten!=two
b!=ten and b ==two and ten!=two
b!=ten and b !=one and ten!=two
b!=ten and b in a_list and ten!=two
e!=ten and e not in a_list and ten!=two
b!=ten and b is two and ten!=two
b!=ten and b is not ten and ten!=two


b in a_list and b is two
b in a_list and b is not ten

e not in a_list and e is five
e not in a_list and e is not ten

a is one and a<ten and one is one_1
a is one and a<=ten and one is one_1
a is one and a>zero and one is one_1
a is one and a>=zero and one is one_1
a is one and a ==one and one is one_1
a is one and a !=ten and one is one_1
a is one and a in a_list and one is one_1
e is five_1 and e not in a_list and five is five_5
a is one and a is one and one_1 is a and one is one_1
a is one and a is not ten and one is one_1

a is not three and a<ten and ten is not two
a is not three and a<=ten  and ten is not two
a is not three and a>zero  and ten is not two
a is not three and a>=zero and three is not two
a is not three and a ==one and three is not two
a is not three and a !=ten and three is not two
a is not three and a is one and three is not two
a is not three and a is not ten and three is not two
a is not three and a in a_list and three is not two
e is not three and e not in a_list and three is not two

zero<a and a in a_list and a_list in a_list_list
zero<=a and a in a_list and a_list in a_list_list
ten>a and a in a_list and a_list in a_list_list
ten>=a and a in a_list and a_list in a_list_list
one==a and a in a_list and a_list in a_list_list
two!=a and a in a_list and a_list in a_list_list
one is a and a in a_list and a_list in a_list_list
one is not a and a in a_list and a_list in a_list_list

zero<e and e not in a_list and a_list not in no_list_list
zero<=e and e not in a_list and a_list not in no_list_list
ten>e and e not in a_list and a_list not in no_list_list
ten>=e and e not in a_list and a_list not in no_list_list
five==e and e not in a_list and a_list not in no_list_list
two!=e and e not in a_list and a_list not in no_list_list
five is e and e not in a_list and a_list not in no_list_list
one is not e and e not in a_list and a_list not in no_list_list


# 4 operator ;全是True的chain compare的81种 2个一样的> >= < <=; !=; ==; in; not in; is; is not的操作符组合

b>one and b<three and one>zero
b>one and b<=three and one>zero
e>one and e>three and one>zero
e>one and e>=three and one>zero
b>one and b!=ten and one>zero
b>one and b==two and one>zero
b>one and b in a_list and one>zero
e>one and e not in a_list and one>zero
e>one and e is five and one>zero
e>one and e is not three and one>zero



b>=one and b<three and one>=zero
b>=one and b<=three and one>=zero
e>=one and e>three and one>=zero
e>=one and e>=three and one>=zero
b>=one and b!=ten and one>=zero
b>=one and b==two and one>=zero
b>=one and b in a_list and one>=zero
e>=one and e not in a_list and one>=zero
b>=one and b is two and one>=zero
b>=one and b is not three and one>=zero


a<=two and a<three and two<=twenty
a<=two and a<=three  and two<=twenty
a<=two and a>three  and two<=twenty
a<=two and a>=three  and two<=twenty
a<=two and a!=ten  and two<=twenty
a<=two and a==one  and two<=twenty
a<=two and a in a_list  and two<=twenty
e<=ten and e not in a_list  and two<=twenty
a<=two and a is one  and two<=twenty
a<=two and a is not two  and two<=twenty

a<two and a<three and two<twenty
a<two and a<=three and two<twenty
a<two and a>zero and two<twenty
a<two and a>=zero and two<twenty
a<two and a!=ten and two<twenty
a<two and a==one and two<twenty
a<two and a in a_list and two<twenty
e<ten and e not in a_list and ten<twenty
a<two and a is one and two<twenty
a<two and a is not one and two<twenty

b==two and b<ten and two==two_2
b==two and b<=ten and two==two_2
b==two and b>one and two==two_2
b==two and b>=one and two==two_2
b==two and b==two_2 and two==two_2
b==two and b!=ten and two==two_2
b==two and b in a_list and two==two_2
e==five and e not in a_list and five==five_2
b==two and b is two and two==two_2
b==two and b is not ten and two==two_2



b!=ten and b <ten and ten!=two
b!=ten and b <=ten and ten!=two
b!=ten and b >one and ten!=two
b!=ten and b >=one and ten!=two
b!=ten and b ==two and ten!=two
b!=ten and b !=one and ten!=two
b!=ten and b in a_list and ten!=two
e!=ten and e not in a_list and ten!=two
b!=ten and b is two and ten!=two
b!=ten and b is not ten and ten!=two


b in a_list and b is two
b in a_list and b is not ten

e not in a_list and e is five
e not in a_list and e is not ten

a is one and a<ten and one is one_1
a is one and a<=ten and one is one_1
a is one and a>zero and one is one_1
a is one and a>=zero and one is one_1
a is one and a ==one and one is one_1
a is one and a !=ten and one is one_1
a is one and a in a_list and one is one_1
e is five_1 and e not in a_list and five is five_5
a is one and a is one and one_1 is a and one is one_1
a is one and a is not ten and one is one_1

a is not three and a<ten and ten is not two
a is not three and a<=ten  and ten is not two
a is not three and a>zero  and ten is not two
a is not three and a>=zero and three is not two
a is not three and a ==one and three is not two
a is not three and a !=ten and three is not two
a is not three and a is one and three is not two
a is not three and a is not ten and three is not two
a is not three and a in a_list and three is not two
e is not three and e not in a_list and three is not two

zero<a and a in a_list and a_list in a_list_list
zero<=a and a in a_list and a_list in a_list_list
ten>a and a in a_list and a_list in a_list_list
ten>=a and a in a_list and a_list in a_list_list
one==a and a in a_list and a_list in a_list_list
two!=a and a in a_list and a_list in a_list_list
one is a and a in a_list and a_list in a_list_list
one is not a and a in a_list and a_list in a_list_list

zero<e and e not in a_list and a_list not in no_list_list
zero<=e and e not in a_list and a_list not in no_list_list
ten>e and e not in a_list and a_list not in no_list_list
ten>=e and e not in a_list and a_list not in no_list_list
five==e and e not in a_list and a_list not in no_list_list
two!=e and e not in a_list and a_list not in no_list_list
five is e and e not in a_list and a_list not in no_list_list
one is not e and e not in a_list and a_list not in no_list_list









