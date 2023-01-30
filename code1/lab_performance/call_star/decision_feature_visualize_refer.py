import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split,cross_val_score,cross_validate
import numpy as np
from sklearn.metrics import f1_score
from sklearn import tree
import pandas as pd
from sklearn.datasets import load_iris
data = load_iris()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target
# feature_names=["num_ele", 'num_subscript',"is_value_const",
#                'is_lower_0', 'is_upper_len','is_step_1', 'context']
# print(data.feature_names)
# print(data.target)
#'''
X_train, X_test, Y_train, Y_test = train_test_split(df[data.feature_names], df['target'], test_size=0.1, random_state=0)
# Step 1: Import the model you want to use
# This was already imported earlier in the notebook so commenting out
#from sklearn.tree import DecisionTreeClassifier
# Step 2: Make an instance of the Model
clf = DecisionTreeClassifier(max_depth = 2,
                             random_state = 0)
# Step 3: Train the model on the data
clf.fit(X_train, Y_train)
Y_pred=clf.predict(X_test)
print(f1_score(Y_test, Y_pred, average='macro'))
print(f1_score(Y_test, Y_pred, average='micro'))
print(f1_score(Y_test, Y_pred, average='weighted'))
# Step 4: Predict labels of unseen (test) data
# Not doing this step in the tutorial
# clf.predict(X_test)
tree.plot_tree(clf)
fn=['sepal length (cm)','sepal width (cm)','petal length (cm)','petal width (cm)']
cn=['regression', 'unchange', 'improve']
fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=300)
tree.plot_tree(clf,
               feature_names = fn,
               class_names=cn,
               filled = False)
fig.savefig('imagename.png')
plt.show()
#https://scikit-learn.org/stable/modules/model_evaluation.html
#https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier.score
score=cross_validate(clf, data.data, data.target, scoring = ['f1_micro','f1_macro'],cv=10)
print(score)
#'''