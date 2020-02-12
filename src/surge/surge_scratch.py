# %% md
# Start by loading from pickle

# %%
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
# import psycopg2 as pg
import os
import sys
# import pandas.io.sql as pd_sql
import numpy as np
import sqlalchemy

project_dir = str(os.path.dirname((os.path.dirname(os.path.abspath('')))))
print(project_dir)
# sys.path.append(project_dir)
import matplotlib.pyplot as plt
from src.pickle.pickle_util import save_pickle, load_pickle
from sklearn.metrics import confusion_matrix

# %%
assert '/Users/erik/metis/data_hailing/data/pickles/' + 'trips_df_scratch_02_eda' == project_dir + '/data/pickles/' + 'trips_df_scratch_02_eda'
trips_df = load_pickle(project_dir + '/data/pickles/' + 'trips_df_scratch_02_eda').dropna()

# %% md
"""
Start a linear model to predict fare based on miles and seconds of trip
"""

# drop zero fare lines
trips_df = trips_df.loc[trips_df.fare > 0.001]

from sklearn.linear_model import LinearRegression

linreg = LinearRegression()
y = trips_df.loc[:, 'fare']
X = trips_df.loc[:, ['trip_miles', 'trip_seconds']]

linreg.fit(X, y)
# print(linreg.score(X, y))

trips_df['pred_fare'] = linreg.predict(X)
trips_df['pred_fare_over_fare'] = trips_df.pred_fare / trips_df.fare

# %%
"""
Run a logistic regression with target surge 
What can I use to try to predict?
# stuff derived from hour of day. like hour of day // 4
pickup community area as dummy variables
pickup_centroid_longitude, pickup_centroid_latitude

start with part of day (hours // 4) and dummies on community location
"""

trips_df['part_of_day'] = trips_df['trip_start_timestamp'].dt.hour // 8
#
#
# X = trips_df.loc[:, ['part_of_day', 'pickup_community_area']]
# y = (trips_df.loc[:,'pred_fare_over_fare'] > 1.15)
#
# logr = LogisticRegression(solver='lbfgs')
# logr.fit(X, y)
# print(logr.score(X, y))    # 0.7667824105325118
#
# print(confusion_matrix(y, logr.predict(X)))   # it's just predicting no surge for everything
#
#
# %%
"""
Maybe try with latitude and longitude now
"""

trips_df['part_of_day'] = trips_df['trip_start_timestamp'].dt.hour // 8

latitude_diff = trips_df.pickup_centroid_latitude - 41.8757
longitude_diff = trips_df.pickup_centroid_longitude + 87.6243
dist_from_loop = np.sqrt(latitude_diff ** 2 + longitude_diff ** 2)
# , 'pickup_centroid_longitude', 'pickup_centroid_latitude'
X = trips_df.loc[:, ['part_of_day', 'pickup_community_area']]
X = pd.concat([X, latitude_diff, longitude_diff, dist_from_loop], axis=1)
X = pd.get_dummies(X, columns=['pickup_community_area', 'part_of_day'])
y = (trips_df.loc[:, 'pred_fare_over_fare'] > 1.15)

# dtree = DecisionTreeClassifier()
# dtree.fit(X, y)
# print('dtree', dtree.score(X, y))  # 0.7674250319960687
# print(confusion_matrix(y, dtree.predict(X)))


# [[141816    176]
#  [ 42892    295]]

def dummy_predictor(X):
    """just predicts always no surge"""
    return [False] * len(X)

# print('dummy accuracy', accuracy_score(y, dummy_predictor(X)))   # dummy accuracy 0.7667824105325118

from sklearn.ensemble import RandomForestClassifier

# rforest = RandomForestClassifier()
# rforest.fit(X, y)
# print('rforest', rforest.score(X, y))   # rforest 0.7673224285691143
# print(confusion_matrix(y, rforest.predict(X)))

#%%
from sklearn.neighbors import KNeighborsClassifier

# knn = KNeighborsClassifier()
# knn.fit(X, y)
# print('knn', knn.score(X, y))   # took way too long!


### let's just try a linear regression from the numeric things to


# recall_score(y, rforest.predict(X))  # Out[9]: 0.009493597610392016

# precision_score(y, rforest.predict(X))    # Out[10]: 0.5624142661179699   # not terrible...
### what was the value of cutoff for surge or not here? ( I think it was 1.15)

### so, I don't catch many, but when I do give tell you it's there, I'm 50 % confident it will be there. That's... good?


# precision_score(y, dtree.predict(X))  # Out[13]: 0.6471389645776566

# recall_score(y, dtree.predict(X))   # Out[14]: 0.010998680158380994

### actually, normal decision tree looks *slightly* better.

#$$ md
# How about different thresholds for calling the surge on

def do_decision_tree(X, y):
    dtree = DecisionTreeClassifier()
    dtree.fit(X, y)
    # print('accurary', dtree.score(X, y))
    print('recall', recall_score(y, dtree.predict(X)))
    print('precision', precision_score(y, dtree.predict(X)))
    print('f1_score', f1_score(y, dtree.predict(X)))
    # print(confusion_matrix(y, dtree.predict(X)))
    return f1_score(y, dtree.predict(X))
#
#
# for i in np.linspace(1.833333, 2, 1):
#
#     print(i)
#     y = (trips_df.loc[:, 'pred_fare_over_fare'] > i)
#     foo = do_decision_tree(X, y)
#     print()

# best recall at low i. (perfect recall at i = 0.45)
# best precision at about i = 1.8 (but then the recall with surely be unnaceptably low...   # recall 0.004488200376429709
"""
with i = 1.83333
1.833333
recall 0.004488200376429709       0.44 percent. terrible!
precision 0.7948717948717948      79 percent.  decent.
[[178264      8]
 [  6876     31]]
"""




# y = (trips_df.loc[:, 'pred_fare_over_fare'] > 1.15)

### try f1 scores at different values of mult

# mult_and_score = []
# for mult in np.linspace(1, 2, 10):
#     y = (trips_df.loc[:, 'pred_fare_over_fare'] > mult)
#     mult_and_score.append(  (mult, do_decision_tree(X, y)))   # f1 score
#     print()

# print(mult_and_score)




### Try oversampling

### drop the pool trips

### can I work back from predicted surges to time and place?




y = (trips_df.loc[:, 'pred_fare_over_fare'] <0.75)
trips_df.loc[:,'surge_estimate'] = trips_df.fare / trips_df.pred_fare
my_var = 1.5
print(my_var)
y = (trips_df.loc[:, 'surge_estimate'] > my_var)
print(y.value_counts())
from sklearn.metrics import precision_recall_curve
#
#
#
#
#
#
dtree = DecisionTreeClassifier()
# logr = LogisticRegression(solver='lbfgs')
dtree.fit(X, y)
predict_proba_threshold = .45
print('accuracy', dtree.score(X, y))
print('recall', recall_score(y, (dtree.predict_proba(X)[:,1] >predict_proba_threshold)))
print('precision', precision_score(y, (dtree.predict_proba(X)[:,1] >predict_proba_threshold)))
print('f1_score', f1_score(y, (dtree.predict_proba(X)[:,1] >predict_proba_threshold)))
print(confusion_matrix(y, (dtree.predict_proba(X)[:,1] >predict_proba_threshold)))
#


# precision_recall_curve(y_true, )

# logr.predict_proba()