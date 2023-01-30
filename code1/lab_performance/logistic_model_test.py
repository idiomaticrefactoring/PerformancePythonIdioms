import pandas as pd
import numpy as np

from math import log
import scipy as sp

from scipy import stats

from sklearn import preprocessing
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

#from sklearn.cross_validation import train_test_split

import statsmodels.formula.api as smf
import seaborn as sns

import warnings
if __name__ == '__main__':

        stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)
        # warnings.filterwarnings(action='once')
        warnings.filterwarnings(action='default')
        # load Data
        dataMain = pd.read_csv("https://raw.githubusercontent.com/sqlshep/SQLShepBlog/master/data/USA.dataAll.csv")

        # Remove infinites and NAs
        dataMain = dataMain.replace([np.inf, -np.inf], np.nan)
        dataMain = dataMain.fillna(0)

        # Rename Column
        dataMain = dataMain.rename(columns={'Unnamed: 0': 'X'})

        # remove extra NY County
        dataMain = dataMain[dataMain.X != 1864]

        # Shape of the data
        print(dataMain.shape)
        # Statistics on the data
        #print(dataMain.describe().T)

        # elect_lg.glm <- glm(Winner ~ lg_Population + lg_PovertyPercent + lg_EDU_HSDiploma +
        #      lg_EDU_SomeCollegeorAS + lg_EDU_BSorHigher + lg_UnemploymentRate +
        #      lg_Married + lg_HHMeanIncome + lg_Diabetes + lg_Inactivity +
        #      lg_OpioidRx, family = binomial, data = data.Main)

        results = smf.logit('Winner ~ lg_Population \
                            + lg_PovertyPercent \
                            + lg_EDU_HSDiploma \
                            + lg_EDU_SomeCollegeorAS \
                            + lg_EDU_BSorHigher \
                            + lg_UnemploymentRate \
                            + lg_Married \
                            + lg_HHMeanIncome \
                            + lg_Diabetes \
                            + lg_Inactivity \
                            + lg_OpioidRx', data=dataMain).fit()
        print(results.summary())