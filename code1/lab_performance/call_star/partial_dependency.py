import pandas as pd
import os,sys
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
sys.path.append(code_dir+"wrap_refactoring/")
import util
from time import time
from sklearn.inspection import PartialDependenceDisplay
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
import pandas as pd
# https://scikit-learn.org/stable/modules/partial_dependence.html
# Use "gpu_hist" for training the model.
import xgboost as xgb
reg = xgb.XGBRegressor(tree_method="gpu_hist")
# Fit the model using predictor X and response y.
reg.fit(X, y)
csv_feature_file_name_corr_dir = util.data_root_mv + "lab_performance/call_star_benchmarks/csv/"
csv_feature_file_name_corr = csv_feature_file_name_corr_dir + "call_star_lab_performance_features.csv"

df = pd.read_csv(csv_feature_file_name_corr)



common_params = {
    "subsample": 50,
    "n_jobs": 2,
    "grid_resolution": 20,
    "centered": True,
    "random_state": 0,
}
cal_housing = fetch_california_housing()
X = pd.DataFrame(cal_housing.data, columns=cal_housing.feature_names)
y = cal_housing.target
print(X)
y -= y.mean()

X_train, X_test, y_train, y_test = train_test_split(X[:640], y[:640], test_size=0.1, random_state=0)



# %%
# Gradient boosting
# .................
#
# Let's now fit a :class:`~sklearn.ensemble.HistGradientBoostingRegressor` and
# compute the partial dependence on the same features.

from sklearn.ensemble import HistGradientBoostingRegressor

print("Training HistGradientBoostingRegressor...")
tic = time()
est = HistGradientBoostingRegressor(random_state=0)
est.fit(X_train, y_train)
print(f"done in {time() - tic:.3f}s")
print(f"Test R2 score: {est.score(X_test, y_test):.2f}")

# %%
# Here, we used the default hyperparameters for the gradient boosting model
# without any preprocessing as tree-based models are naturally robust to
# monotonic transformations of numerical features.
#
# Note that on this tabular dataset, Gradient Boosting Machines are both
# significantly faster to train and more accurate than neural networks. It is
# also significantly cheaper to tune their hyperparameters (the defaults tend
# to work well while this is not often the case for neural networks).
#
# We will plot the partial dependence, both individual (ICE) and averaged one
# (PDP). We limit to only 50 ICE curves to not overcrowd the plot.

print("Computing partial dependence plots...")
tic = time()
display = PartialDependenceDisplay.from_estimator(
    est,
    X_train,
    features=["MedInc", "AveOccup", "HouseAge", "AveRooms"],
    kind="both"
)
print(f"done in {time() - tic:.3f}s")
display.figure_.suptitle(
    "Partial dependence of house value on non-location features\n"
    "for the California housing dataset, with Gradient Boosting"
)
display.figure_.subplots_adjust(wspace=0.4, hspace=0.3)
