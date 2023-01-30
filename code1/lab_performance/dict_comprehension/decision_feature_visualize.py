import os,sys
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split,cross_val_score,cross_validate
import numpy as np
from sklearn.metrics import f1_score,roc_auc_score,make_scorer
from sklearn import tree
import pandas as pd
from sklearn.datasets import load_iris
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
sys.path.append(code_dir+"wrap_refactoring/")
import util
'''
https://zhuanlan.zhihu.com/p/125685550
'''
csv_feature_file_name_corr = util.data_root_mv + "lab_performance/dict_compre_benchmarks/csv/train_data_dict_compre.csv"#"lab_performance/call_star_benchmarks/csv/train_data_call_star.csv"
df=pd.read_csv(csv_feature_file_name_corr)
# print(df)'regression', 'unchange', 'improve'
print(list(df['kind']).count("unchange"))
print(len(list(df['kind'])))
# print(df)'regression', 'unchange', 'improve'
df['kind'] = df['kind'].map({'regression':0,
                             'unchange':1,
                             'improve':2,
                             np.nan:'NY'},
                             na_action=None).astype('int')
# for ind,kind in enumerate(df.kind):
#     if kind=="regression":
#         df.kind[ind]=0
#     elif kind=="unchange":
#         df.kind[ind] = 1
#     else:
#         df.kind[ind] = 2
df['target']=df.kind
# print(list(df['target']))
feature_names = ["num_ele",'num_loop',
                   'num_if', 'num_if_else',
                   'context']

'''
data = load_iris()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target
feature_names=data.feature_names
'''
# feature_names=["num_ele", 'num_subscript',"is_value_const",
#                'is_lower_0', 'is_upper_len','is_step_1', 'context']
# print(data.feature_names)
# print(data.target)
# print(df[feature_names])
X_train, X_test, Y_train, Y_test = train_test_split(df[feature_names], df['target'], test_size=0.1, random_state=0)
print(X_train)
# Step 1: Import the model you want to use
# This was already imported earlier in the notebook so commenting out
#from sklearn.tree import DecisionTreeClassifier
# Step 2: Make an instance of the Model
clf = DecisionTreeClassifier(max_depth = 4,
                             random_state = 0)#max_depth = 2,
# Step 3: Train the model on the data
clf.fit(X_train, Y_train)
# Y_pred=clf.predict(X_test)
Y_pred=clf.predict_proba(X_test)

# print(f1_score(Y_test, Y_pred, average='macro'))
# print(f1_score(Y_test, Y_pred, average='micro'))
# print(f1_score(Y_test, Y_pred, average='weighted'))
print("roc_auc_score(Y_test, Y_pred)",roc_auc_score(Y_test, Y_pred,multi_class='ovo'))

# '''
# Step 4: Predict labels of unseen (test) data
# Not doing this step in the tutorial
# clf.predict(X_test)
#https://blog.csdn.net/qq_41103204/article/details/116778943 tree的含义解释
#https://datagy.io/sklearn-decision-tree-classifier/
# tree.plot_tree(clf)
fn=feature_names
cn=['regression', 'unchange', 'improve']
fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=500)
tree.plot_tree(clf,
               feature_names = fn,
               class_names=cn,
               filled = False)
# fig.savefig('imagename.png')
plt.savefig("performance_rq1_dict_compre.pdf", format="pdf", bbox_inches="tight",pad_inches=0)

plt.show()
print(tree.export_text(clf))
myscore = make_scorer(roc_auc_score, multi_class='ovo',needs_proba=True)

#https://scikit-learn.org/stable/modules/model_evaluation.html
#https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier.score
score=cross_validate(clf, df[feature_names], df.target, scoring =myscore,cv=10)

# score=cross_validate(clf, df[feature_names], df.target, scoring = ['f1_micro','f1_macro'],cv=10)
print(score)
#'''