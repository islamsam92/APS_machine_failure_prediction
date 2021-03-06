# -*- coding: utf-8 -*-
"""Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ie5TaLV-MRfeVdz_-YmgzY3_YZrZx491
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_digits
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
##Calculate the total cost
from sklearn.metrics import accuracy_score
#accuracy_score(test_labels, y_pred)
## Confusion matrix
from sklearn.metrics import confusion_matrix
#confusion_matrix(test_labels, y_pred)

!pip install xgboost
from numpy import loadtxt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn import metrics

from matplotlib import pyplot

### Functions

"""### Defining the Cost Function (Evaluation Function)"""

def calculate_cost(test_labels,y_pred):
  confusion_matrix(test_labels, y_pred)
  con_mat = confusion_matrix(test_labels, y_pred)
  cost_1 = con_mat[0][1]
  cost_2 = con_mat[1][0]
  total_pred = con_mat[0][0] + con_mat[0][1] + con_mat[1][0] + con_mat[1][1]
  accur = (con_mat[0][0] / total_pred ) * 100
  total_cost = (cost_1 * 10) + (cost_2*500)
  # accuracy: (tp + tn) / (p + n)
  accuracy = accuracy_score(test_labels, y_pred)
  print('Accuracy: %f' % accuracy)
  # precision tp / (tp + fp)
  precision = precision_score(test_labels, y_pred)
  print('Precision: %f' % precision)
  # recall: tp / (tp + fn)
  recall = recall_score(test_labels, y_pred)
  print('Recall: %f' % recall)
  # f1: 2 tp / (2 tp + fp + fn)
  f1 = f1_score(test_labels, y_pred)
  print('F1 score: %f' % f1)


  # ROC AUC
  auc = roc_auc_score(test_labels, y_pred)
  print('ROC AUC: %f' % auc)
  # confusion matrix
  matrix = confusion_matrix(test_labels, y_pred)
  print(matrix)
  return total_cost, cost_1, cost_2, accur


## As chi squred does not accept negative we need to make all the values between zero and 1
## Also some of algorithm works better when do this step ahead
def MinMaxScaler_def(features,feature_list):
  scaler = MinMaxScaler()
  scaler.fit(features)
  train_features = pd.DataFrame(scaler.transform(features), columns=feature_list)
  return train_features


def selectKBest(k_best,train_features,labels,test_features):
  selectKBest = SelectKBest(chi2, k_best)
  selectKBest.fit(train_features, labels)
  best_train_features = selectKBest.transform(train_features)

  idxs_selected = selectKBest.get_support(indices=True)
  best_train_features = train_features.iloc[:,idxs_selected]
  best_test_features = test_features.iloc[:,idxs_selected]

  return best_train_features,best_test_features

""" Train Data"""

train_raw = pd.read_csv('/content/aps_failure_training_set.csv',na_values='na')
train_processed = pd.read_csv('/content/aps_failure_training_set_processed_8bit.csv',na_values='na')
train_processed["class"] = train_raw["class"]

train_processed.columns

test_raw = pd.read_csv('/content/aps_failure_test_set.csv',na_values='na')
test_processed = pd.read_csv('/content/aps_failure_test_set_processed_8bit.csv',na_values='na')
test_processed["class"] = test_raw["class"]

test_processed.columns

"""**All Data**"""

all = train_processed.append(test_processed)

### 170 features
### 76000 instances
all.shape

labelencoder = LabelEncoder()

# Assigning numerical values and storing in another column
all['class_labeled'] = labelencoder.fit_transform(all['class'])
The_class = all[['class_labeled']]
all = all.drop('class',axis=1)
#aps_failure_processed.head()

## all data
ozero_counter = 0
oone_counter = 0
for i in all['class_labeled']:
    if i == 0 :
        ozero_counter+=1
    if i == 1:
        oone_counter+=1
print("Original Zeros count is",ozero_counter)
print("Original Ones count is",oone_counter)

all_df = pd.DataFrame({'neg':[74625],'pos':[1375]})
all_df.plot(kind='bar')
all_df.index = ['label']
plt.ylabel(' count')

#from google.colab import drive
#drive.mount('/content/drive')

"""**Cleaning and preparation**"""

## 80% , 10% , 10%
from sklearn.model_selection import train_test_split

# Let's say we want to split the data in 80:10:10 for train:valid:test dataset
train_size=0.8

X = all.drop(columns = ['class_labeled']).copy()
y = all['class_labeled']

# In the first step we will split the data in training and remaining dataset
X_train, X_rem, y_train, y_rem = train_test_split(X,y, train_size=0.8)

# Now since we want the valid and test size to be equal (10% each of overall data). 
# we have to define valid_size=0.5 (that is 50% of remaining data)
test_size = 0.5
X_valid, X_test, y_valid, y_test = train_test_split(X_rem,y_rem, test_size=0.5)

print("Train shape: ")
print(X_train.shape), print(y_train.shape)
print("Validation shape: ")
print(X_valid.shape), print(y_valid.shape)
print("Test shape: ")
print(X_test.shape), print(y_test.shape)

"""## **Train**"""

# Labels are the values we want to predict
train_labels = np.array(y_train)
# Remove the labels from the features
# axis 1 refers to the columns
train_features = X_train
# Saving feature names for later use
train_feature_list = list(train_features.columns)
# Convert to numpy array
train_features = np.array(train_features)

train_features.shape

y_train.shape

train_labels.shape

"""# **Validation**"""

# Labels are the values we want to predict
validation_labels = np.array(y_valid)
# Remove the labels from the features
# axis 1 refers to the columns
validation_features = X_valid
# Saving feature names for later use
validation_feature_list = list(validation_features.columns)
# Convert to numpy array
validation_features = np.array(validation_features)

validation_features.shape

validation_labels.shape

"""# **Test**"""

# Labels are the values we want to predict
test_labels = np.array(y_test)
# Remove the labels from the features
# axis 1 refers to the columns
test_features = X_test
# Saving feature names for later use
test_feature_list = list(test_features.columns)
# Convert to numpy array
test_features = np.array(test_features)

test_features.shape

test_labels.shape

## Check with shapes
print('Training Features Shape:', train_features.shape)
print('Training Labels Shape:', train_labels.shape)
print('Validation Features Shape:', validation_features.shape)
print('Validation Labels Shape:', validation_labels.shape)
print('Testing Features Shape:', test_features.shape)
print('Testing Labels Shape:', test_labels.shape)

train_labels

"""### Imbalanced Training handling using SMOTE"""

import imblearn 
from collections import Counter
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE

#Print 0s and 1s original count 
ozero_counter = 0
oone_counter = 0
for i in train_labels:
    if i == 0 :
        ozero_counter+=1
    if i == 1:
        oone_counter+=1
print("Original Zeros count is",ozero_counter)
print("Original Ones count is",oone_counter)

# transform the dataset
oversample = SMOTE()
train_features, train_labels = oversample.fit_resample(train_features, train_labels)

#Print 0s and 1s after SMOTE
zero_counter = 0
one_counter = 0
for i in train_labels:
    if i == 0 :
        zero_counter+=1
    if i ==1:
        one_counter+=1
print("After SMOTE Zeros count is",zero_counter)
print("After SMOTE Ones count is",one_counter)

train_features.shape

train_labels.shape

##befor
before_df = pd.DataFrame({'0':[60800],'1':[1075]})
before_df.plot(kind='bar')

##after
after_df = pd.DataFrame({'Neg':[59725],'Pos':[59725]})
after_df.plot(kind='bar')

"""**CHI SQUARE**"""

## As chi squred does not accept negative we need to make all the values between zero and 1
## Also some of algorithm works better when do this step ahead
def MinMaxScaler_def(features,feature_list):
  scaler = MinMaxScaler()
  scaler.fit(features)
  train_features = pd.DataFrame(scaler.transform(features), columns=feature_list)
  return train_features

def selectKBest(k_best,train_features,validation_features,test_features):
  selectKBest = SelectKBest(chi2, k_best)
  selectKBest.fit(train_features, train_labels)
  best_train_features = selectKBest.transform(train_features)

  idxs_selected = selectKBest.get_support(indices=True)
  best_train_features = train_features.iloc[:,idxs_selected]
  best_validation_features = validation_features.iloc[:,idxs_selected]
  best_test_features = test_features.iloc[:,idxs_selected]

  return best_train_features,best_validation_features,best_test_features

##Main
train_features_scaled = MinMaxScaler_def( train_features ,train_feature_list)
validation_features_scaled = MinMaxScaler_def(validation_features, validation_feature_list)
test_features_scaled = MinMaxScaler_def(test_features,test_feature_list)

best_train_features,best_validation_features,best_test_features = selectKBest(40,train_features_scaled,validation_features_scaled,test_features_scaled)

best_train_features.shape

best_validation_features.shape

best_test_features.shape

"""### **PCA**"""

from sklearn.decomposition import PCA
pca = PCA().fit(train_features)
#remove ; to see the output
pca.explained_variance_ratio_;

plt.rcParams["figure.figsize"] = (12,6)
fig, ax = plt.subplots()
xi = np.arange(1, 171, step=1)
y = np.cumsum(pca.explained_variance_ratio_)

plt.ylim(0.0,1.1)
plt.plot(xi, y, marker='o', linestyle='--', color='b')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative variance (%)')
plt.title('The number of components needed to explain variance')
plt.axhline(y=0.70, color='r', linestyle='-')
plt.text(0.5, 0.73, '70% cut-off threshold', color = 'red', fontsize=16)
plt.axhline(y=0.90, color='r', linestyle='-')
plt.text(0.5, 0.85, '90% cut-off threshold', color = 'red', fontsize=16)

ax.grid(axis='x')
plt.show()

n_comp=[0.70,0.75,0.80,0.85,0.90]

"""**TEST AND TRAIN VALUES FOR VARIANCE**"""

#70%
pca = PCA(n_components = n_comp[0],random_state = 42)
pca.fit(train_features)
x_train_new_0 = pca.transform(train_features)
X_valid_0 = pca.transform(X_valid)
x_test_0 = pca.transform(X_test)
print("Number of features after PCA = ", x_test_0.shape[1])

#75
pca = PCA(n_components = n_comp[1],random_state = 42)
pca.fit(X_train)
x_train_new_1 = pca.transform(train_features)
X_valid_1 = pca.transform(X_valid)
x_test_1 = pca.transform(X_test)
print("Number of features after PCA = ", x_test_1.shape[1])

#80
pca = PCA(n_components = n_comp[2],random_state = 42)
pca.fit(X_train)
x_train_new_2 = pca.transform(train_features)
X_valid_2 = pca.transform(X_valid)
x_test_2 = pca.transform(X_test)
print("Number of features after PCA = ", x_test_2.shape[1])

#85
pca = PCA(n_components = n_comp[3],random_state = 42)
pca.fit(X_train)
x_train_new_3 = pca.transform(train_features)
X_valid_3 = pca.transform(X_valid)
x_test_3 = pca.transform(X_test)
print("Number of features after PCA = ", x_test_3.shape[1])

#90
pca = PCA(n_components = n_comp[4],random_state = 42)
pca.fit(X_train)
x_train_new_4 = pca.transform(train_features)
X_valid_4 = pca.transform(X_valid)
x_test_4 = pca.transform(X_test)
print("Number of features after PCA = ", x_test_4.shape[1])

"""### Plain RF"""

#Import Random Forest Model
from sklearn.ensemble import RandomForestClassifier

#Create a Gaussian Classifier
clf = RandomForestClassifier(n_estimators=100 )

#Train the model using the training sets y_pred=clf.predict(X_test)
clf.fit(train_features,train_labels)

y_pred=clf.predict(validation_features)
rf_cost = calculate_cost(test_labels,y_pred)
print(rf_cost)

#testing 70
y_pred=clf.predict(test_features)
rf_pca_cost_0 = calculate_cost(test_labels,y_pred)
print(rf_pca_cost_0)

"""## **1. Training with PCA**

### RF + PCA
"""

train_labels.shape

x_train_new_0.shape

#Import Random Forest Model
from sklearn.ensemble import RandomForestClassifier

#Create a Gaussian Classifier
clf = RandomForestClassifier(n_estimators=100 )

#Train the model using the training sets y_pred=clf.predict(X_test)
#70%
clf.fit(x_train_new_0,train_labels)

#validation
y_pred=clf.predict(X_valid_0)
rf_pca_cost_0 = calculate_cost(validation_labels,y_pred)
print(rf_pca_cost_0)

#testing 70
y_pred=clf.predict(x_test_0)
rf_pca_cost_0 = calculate_cost(test_labels,y_pred)
print(rf_pca_cost_0)

#Create a Gaussian Classifier
clf = RandomForestClassifier(n_estimators=100 )

#Train the model using the training sets y_pred=clf.predict(X_test)
#75%
clf.fit(x_train_new_1,train_labels)

y_pred=clf.predict(X_valid_1)
rf_pca_cost_1 = calculate_cost(validation_labels,y_pred)
print(rf_pca_cost_1)

#testing 75
y_pred=clf.predict(x_test_1)
rf_pca_cost_1 = calculate_cost(test_labels,y_pred)
print(rf_pca_cost_1)

#Create a Gaussian Classifier
clf = RandomForestClassifier(n_estimators=100 )

#Train the model using the training sets y_pred=clf.predict(X_test)
#80%
clf.fit(x_train_new_2,train_labels)

y_pred=clf.predict(X_valid_2)
rf_pca_cost_2 = calculate_cost(validation_labels,y_pred)
print(rf_pca_cost_2)

#testing 80
y_pred=clf.predict(x_test_2)
rf_pca_cost_2 = calculate_cost(test_labels,y_pred)
print(rf_pca_cost_2)

#Create a Gaussian Classifier
clf = RandomForestClassifier(n_estimators=100 )

#Train the model using the training sets y_pred=clf.predict(X_test)
#85%
clf.fit(x_train_new_3,train_labels)

y_pred=clf.predict(X_valid_3)
rf_pca_cost_3 = calculate_cost(validation_labels,y_pred)
print(rf_pca_cost_3)

#testing 85
y_pred=clf.predict(x_test_3)
rf_pca_cost_3 = calculate_cost(test_labels,y_pred)
print(rf_pca_cost_3)

#Create a Gaussian Classifier
clf = RandomForestClassifier(n_estimators=100 )

#Train the model using the training sets y_pred=clf.predict(X_test)
#90%
clf.fit(x_train_new_4,train_labels)

y_pred=clf.predict(X_valid_4)
rf_pca_cost_4 = calculate_cost(validation_labels,y_pred)
print(rf_pca_cost_4)

#testing 90
y_pred=clf.predict(x_test_4)
rf_pca_cost_4 = calculate_cost(test_labels,y_pred)
print(rf_pca_cost_4)

"""### GB + PCA"""

from sklearn.ensemble import GradientBoostingClassifier

clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,\
                                 max_depth=1, random_state=0)
#Train the model using the training sets y_pred=clf.predict(X_test)
#70%
clf.fit(x_train_new_0,train_labels)

#validation
y_pred=clf.predict(X_valid_0)
gb_pca_cost_0 = calculate_cost(validation_labels,y_pred)
print(gb_pca_cost_0)

#testing 70
y_pred=clf.predict(x_test_0)
gb_pca_cost_0 = calculate_cost(test_labels,y_pred)
print(gb_pca_cost_0)

#75%
clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,\
                                 max_depth=1, random_state=0)
#Train the model using the training sets y_pred=clf.predict(X_test)
#75%
clf.fit(x_train_new_1,train_labels)

#validation
y_pred=clf.predict(X_valid_1)
gb_pca_cost_1 = calculate_cost(validation_labels,y_pred)
print(gb_pca_cost_1)

#testing 75
y_pred=clf.predict(x_test_1)
gb_pca_cost_1 = calculate_cost(test_labels,y_pred)
print(gb_pca_cost_1)

#80%
clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,\
                                 max_depth=1, random_state=0)

#Train the model using the training sets y_pred=clf.predict(X_test)
#80%
clf.fit(x_train_new_2,train_labels)

#validation
y_pred=clf.predict(X_valid_2)
gb_pca_cost_2 = calculate_cost(validation_labels,y_pred)
print(gb_pca_cost_2)

#testing 80
y_pred=clf.predict(x_test_2)
gb_pca_cost_2 = calculate_cost(test_labels,y_pred)
print(gb_pca_cost_2)

#85%
clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,\
                                 max_depth=1, random_state=0)


#Train the model using the training sets y_pred=clf.predict(X_test)
#80%
clf.fit(x_train_new_3,train_labels)

#validation
y_pred=clf.predict(X_valid_3)
gb_pca_cost_3 = calculate_cost(validation_labels,y_pred)
print(gb_pca_cost_3)

#testing 85
y_pred=clf.predict(x_test_3)
gb_pca_cost_3 = calculate_cost(test_labels,y_pred)
print(gb_pca_cost_3)

#90%
clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,\
                                 max_depth=1, random_state=0)


#Train the model using the training sets y_pred=clf.predict(X_test)
#80%
clf.fit(x_train_new_4,train_labels)

#validation
y_pred=clf.predict(X_valid_4)
gb_pca_cost_4 = calculate_cost(validation_labels,y_pred)
print(gb_pca_cost_4)

#testing 90
y_pred=clf.predict(x_test_4)
gb_pca_cost_4 = calculate_cost(test_labels,y_pred)
print(gb_pca_cost_4)

"""### XGBoost + PCA"""

from sklearn.ensemble import GradientBoostingClassifier
# fit model no training data
clf = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
              colsample_bynode=1, colsample_bytree=0.3, gamma=0.4,
              learning_rate=0.15, max_delta_step=0, max_depth=15,
              min_child_weight=1, missing=None, n_estimators=100, n_jobs=1,
              nthread=None, objective='binary:logistic', random_state=42,
              reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
              silent=None, subsample=1, verbosity=1)

#Train the model using the training sets y_pred=clf.predict(X_test)
#70%
clf.fit(x_train_new_0,train_labels)

#validation
y_pred=clf.predict(X_valid_0)
xgb_pca_cost_0 = calculate_cost(validation_labels,y_pred)
print(xgb_pca_cost_0)

#testing 70
y_pred=clf.predict(x_test_0)
xgb_pca_cost_0 = calculate_cost(test_labels,y_pred)
print(xgb_pca_cost_0)

#75%
# fit model no training data
clf = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
              colsample_bynode=1, colsample_bytree=0.3, gamma=0.4,
              learning_rate=0.15, max_delta_step=0, max_depth=15,
              min_child_weight=1, missing=None, n_estimators=100, n_jobs=1,
              nthread=None, objective='binary:logistic', random_state=42,
              reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
              silent=None, subsample=1, verbosity=1)

#Train the model using the training sets y_pred=clf.predict(X_test)
#75%
clf.fit(x_train_new_1,train_labels)

#validation
y_pred=clf.predict(X_valid_1)
xgb_pca_cost_1 = calculate_cost(validation_labels,y_pred)
print(xgb_pca_cost_1)

#testing 75
y_pred=clf.predict(x_test_1)
xgb_pca_cost_1 = calculate_cost(test_labels,y_pred)
print(xgb_pca_cost_1)

#80%
# fit model no training data
clf = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
              colsample_bynode=1, colsample_bytree=0.3, gamma=0.4,
              learning_rate=0.15, max_delta_step=0, max_depth=15,
              min_child_weight=1, missing=None, n_estimators=100, n_jobs=1,
              nthread=None, objective='binary:logistic', random_state=42,
              reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
              silent=None, subsample=1, verbosity=1)


#Train the model using the training sets y_pred=clf.predict(X_test)
#80%
clf.fit(x_train_new_2,train_labels)

#validation
y_pred=clf.predict(X_valid_2)
xgb_pca_cost_2 = calculate_cost(validation_labels,y_pred)
print(xgb_pca_cost_2)

#testing 80
y_pred=clf.predict(x_test_2)
xgb_pca_cost_2 = calculate_cost(test_labels,y_pred)
print(xgb_pca_cost_2)

#85%
# fit model no training data
clf = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
              colsample_bynode=1, colsample_bytree=0.3, gamma=0.4,
              learning_rate=0.15, max_delta_step=0, max_depth=15,
              min_child_weight=1, missing=None, n_estimators=100, n_jobs=1,
              nthread=None, objective='binary:logistic', random_state=42,
              reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
              silent=None, subsample=1, verbosity=1)



#Train the model using the training sets y_pred=clf.predict(X_test)
#80%
clf.fit(x_train_new_3,train_labels)

#validation
y_pred=clf.predict(X_valid_3)
xgb_pca_cost_3 = calculate_cost(validation_labels,y_pred)
print(xgb_pca_cost_3)

#testing 85
y_pred=clf.predict(x_test_3)
xgb_pca_cost_3 = calculate_cost(test_labels,y_pred)
print(xgb_pca_cost_3)

#90%
# fit model no training data
clf = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
              colsample_bynode=1, colsample_bytree=0.3, gamma=0.4,
              learning_rate=0.15, max_delta_step=0, max_depth=15,
              min_child_weight=1, missing=None, n_estimators=100, n_jobs=1,
              nthread=None, objective='binary:logistic', random_state=42,
              reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
              silent=None, subsample=1, verbosity=1)



#Train the model using the training sets y_pred=clf.predict(X_test)
#80%
clf.fit(x_train_new_4,train_labels)

#validation
y_pred=clf.predict(X_valid_4)
xgb_pca_cost_4 = calculate_cost(validation_labels,y_pred)
print(xgb_pca_cost_4)

#testing 90
y_pred=clf.predict(x_test_4)
xgb_pca_cost_4 = calculate_cost(test_labels,y_pred)
print(xgb_pca_cost_4)

"""### NN + PCA"""

## Neural netowrk with chi square
import tensorflow as tf 
from tensorflow import keras 
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

clf = MLPClassifier(activation='relu', solver='adam', alpha=1e-5,hidden_layer_sizes=(10,), random_state=1,max_iter=1500)

#70%
clf.fit(x_train_new_0,train_labels)

#validation
y_pred=clf.predict(X_valid_0)
nn_pca_cost_0 = calculate_cost(validation_labels,y_pred)
print(nn_pca_cost_0)

#testing 70
y_pred=clf.predict(x_test_0)
nn_pca_cost_0 = calculate_cost(test_labels,y_pred)
print(nn_pca_cost_0)

#75%
# fit model no training data
## Neural netowrk with chi square
import tensorflow as tf 
from tensorflow import keras 
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

clf = MLPClassifier(activation='relu', solver='adam', alpha=1e-5,hidden_layer_sizes=(10,), random_state=1,max_iter=1500)
#75%
clf.fit(x_train_new_1,train_labels)

#validation
y_pred=clf.predict(X_valid_1)
nn_pca_cost_1 = calculate_cost(validation_labels,y_pred)
print(nn_pca_cost_1)

#testing 75
y_pred=clf.predict(x_test_1)
nn_pca_cost_1 = calculate_cost(test_labels,y_pred)
print(nn_pca_cost_1)

#80%
# fit model no training data
## Neural netowrk with chi square
import tensorflow as tf 
from tensorflow import keras 
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

clf = MLPClassifier(activation='relu', solver='adam', alpha=1e-5,hidden_layer_sizes=(10,), random_state=1,max_iter=1500)
#80%
clf.fit(x_train_new_2,train_labels)

#validation
y_pred=clf.predict(X_valid_2)
nn_pca_cost_2 = calculate_cost(validation_labels,y_pred)
print(nn_pca_cost_2)

#testing 80
y_pred=clf.predict(x_test_2)
nn_pca_cost_2 = calculate_cost(test_labels,y_pred)
print(nn_pca_cost_2)

#85%
# fit model no training data
## Neural netowrk with chi square
import tensorflow as tf 
from tensorflow import keras 
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

clf = MLPClassifier(activation='relu', solver='adam', alpha=1e-5,hidden_layer_sizes=(10,), random_state=1,max_iter=1500)
#85%
clf.fit(x_train_new_3,train_labels)

#validation
y_pred=clf.predict(X_valid_3)
nn_pca_cost_3 = calculate_cost(validation_labels,y_pred)
print(nn_pca_cost_3)

#testing 85
y_pred=clf.predict(x_test_3)
nn_pca_cost_3 = calculate_cost(test_labels,y_pred)
print(nn_pca_cost_3)

#90%
# fit model no training data
## Neural netowrk with chi square
import tensorflow as tf 
from tensorflow import keras 
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

clf = MLPClassifier(activation='relu', solver='adam', alpha=1e-5,hidden_layer_sizes=(10,), random_state=1,max_iter=1500)

#90%
clf.fit(x_train_new_4,train_labels)

#validation
y_pred=clf.predict(X_valid_4)
nn_pca_cost_4 = calculate_cost(validation_labels,y_pred)
print(nn_pca_cost_4)

#testing 90
y_pred=clf.predict(x_test_4)
nn_pca_cost_4 = calculate_cost(test_labels,y_pred)
print(nn_pca_cost_4)

"""roc nn1"""

lr_fpr_pca_nn, lr_tpr_pca_nn, _ = roc_curve(test_labels,y_pred)

"""### SVM + PCA"""

from sklearn import svm
clf = svm.SVC(C = 0.03,kernel = 'rbf',gamma = 0.15,random_state = 20)

#70%
clf.fit(x_train_new_0,train_labels)

#validation
y_pred=clf.predict(X_valid_0)
svm_pca_cost_0 = calculate_cost(validation_labels,y_pred)
print(svm_pca_cost_0)

#testing 70
y_pred=clf.predict(x_test_0)
svm_pca_cost_0 = calculate_cost(test_labels,y_pred)
print(svm_pca_cost_0)

## SVM 
from sklearn import svm
clf = svm.SVC(C = 0.03,kernel = 'rbf',gamma = 0.15,random_state = 20)


#75%
clf.fit(x_train_new_1,train_labels)

#validation
y_pred=clf.predict(X_valid_1)
svm_pca_cost_1 = calculate_cost(validation_labels,y_pred)
print(svm_pca_cost_1)

#testing 75
y_pred=clf.predict(x_test_1)
svm_pca_cost_1 = calculate_cost(test_labels,y_pred)
print(svm_pca_cost_1)

from sklearn import svm
clf = svm.SVC(C = 0.03,kernel = 'rbf',gamma = 0.15,random_state = 20)

#80%
clf.fit(x_train_new_2,train_labels)

#validation
y_pred=clf.predict(X_valid_2)
svm_pca_cost_2 = calculate_cost(validation_labels,y_pred)
print(svm_pca_cost_2)

#testing 80
y_pred=clf.predict(x_test_2)
svm_pca_cost_2 = calculate_cost(test_labels,y_pred)
print(svm_pca_cost_2)

## SVM
from sklearn import svm
clf = svm.SVC(C = 0.03,kernel = 'rbf',gamma = 0.15,random_state = 20)


#85%
clf.fit(x_train_new_3,train_labels)

#validation
y_pred=clf.predict(X_valid_3)
svm_pca_cost_3 = calculate_cost(validation_labels,y_pred)
print(svm_pca_cost_3)

#testing 85
y_pred=clf.predict(x_test_3)
svm_pca_cost_3 = calculate_cost(test_labels,y_pred)
print(svm_pca_cost_3)

## SVM 
from sklearn import svm
clf = svm.SVC(C = 0.03,kernel = 'rbf',gamma = 0.15,random_state = 20)


#Train the model using the training sets y_pred=clf.predict(X_test)
#90%
clf.fit(x_train_new_4,train_labels)

#validation
y_pred=clf.predict(X_valid_4)
svm_pca_cost_4 = calculate_cost(validation_labels,y_pred)
print(svm_pca_cost_4)

#testing 90
y_pred=clf.predict(x_test_4)
svm_pca_cost_4 = calculate_cost(test_labels,y_pred)
print(svm_pca_cost_4)

"""ROC1"""

lr_fpr_pca_svm, lr_tpr_pca_svm, _ = roc_curve(test_labels,y_pred)

"""**1. Training with Chi square**

## RF + Chi
"""

#Create a Gaussian Classifier
clf = RandomForestClassifier(n_estimators=100 )

clf.fit(best_train_features,train_labels)

#validation
y_pred=clf.predict(best_validation_features)
rf_chi_cost = calculate_cost(validation_labels,y_pred)
print(rf_chi_cost)

#testing 
y_pred=clf.predict(best_test_features)
rf_chi_cost = calculate_cost(test_labels,y_pred)
print(rf_chi_cost)

"""## GB + Chi"""

clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,\
                                 max_depth=1, random_state=0)


#Train the model using the training sets y_pred=clf.predict(X_test)
#80%
clf.fit(best_train_features,train_labels)

#validation
y_pred=clf.predict(best_validation_features)
gb_chi_cost = calculate_cost(validation_labels,y_pred)
print(gb_chi_cost)

#testing 
y_pred=clf.predict(best_test_features)
gb_chi_cost = calculate_cost(test_labels,y_pred)
print(gb_chi_cost)

"""ROC GB"""

lr_fpr_chi_gb, lr_tpr_chi_gb, _ = roc_curve(test_labels,y_pred)

"""## XGBoost + Chi"""

# fit model no training data
clf = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
              colsample_bynode=1, colsample_bytree=0.3, gamma=0.4,
              learning_rate=0.15, max_delta_step=0, max_depth=15,
              min_child_weight=1, missing=None, n_estimators=100, n_jobs=1,
              nthread=None, objective='binary:logistic', random_state=42,
              reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
              silent=None, subsample=1, verbosity=1)

#Train the model using the training sets y_pred=clf.predict(X_test)
#80%
clf.fit(best_train_features,train_labels)

#validation
y_pred_chi_xgboost_valid=clf.predict(best_validation_features)
xgb_chi_cost = calculate_cost(validation_labels,y_pred_chi_xgboost_valid)
print(xgb_chi_cost)

#testing 
y_pred_chi_xgboost_test=clf.predict(best_test_features)
xgb_chi_cost = calculate_cost(test_labels,y_pred_chi_xgboost_test)
print(xgb_chi_cost)

"""## SVM + Chi"""

## SVM + CHi square
from sklearn import svm
svmclf = svm.SVC(C = 0.03,kernel = 'rbf',gamma = 0.15,random_state = 20)
svmclf.fit(best_train_features,train_labels)
y_pred_chi_valid = svmclf.predict(best_validation_features)

svm_chi_cost = calculate_cost(validation_labels,y_pred_chi_valid)
print('SVM + Select K=40 Best:', svm_chi_cost)

#testing 
y_pred_chi_test=clf.predict(best_test_features)
svm_chi_cost = calculate_cost(test_labels,y_pred_chi_test)
print(svm_chi_cost)

# accuracy: (tp + tn) / (p + n)
accuracy_svm_chi = accuracy_score(test_labels,y_pred_chi_test)
print('Accuracy: %f' % accuracy)
# precision tp / (tp + fp)
precision_svm_chi = precision_score(test_labels,y_pred_chi_test)
print('Precision: %f' % precision)
# recall: tp / (tp + fn)
recall_svm_chi = recall_score(test_labels,y_pred_chi_test)
print('Recall: %f' % recall)
# f1: 2 tp / (2 tp + fp + fn)
f1 = f1_score(test_labels,y_pred_chi_test)
print('F1 score: %f' % f1)


# ROC AUC
auc_svm_chi = roc_auc_score(test_labels,y_pred_chi_test)
print('ROC AUC: %f' % auc)
# confusion matrix
matrix_svm_chi = confusion_matrix(test_labels,y_pred_chi_test)
print(matrix)

"""ROC"""

lr_fpr_chi_svm, lr_tpr_chi_svm, _ = roc_curve(test_labels,y_pred_chi_test)

"""### NN + Chi """

### Neural netowrk with chi square
import tensorflow as tf 
from tensorflow import keras 
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

clf = MLPClassifier(activation='relu', solver='adam', alpha=1e-5,hidden_layer_sizes=(10,), random_state=1,max_iter=1500)
clf.fit(best_train_features,train_labels)
y_pred_chi_nn = clf.predict(best_validation_features)

perceptron_cost = calculate_cost(validation_labels,y_pred_chi_nn)
print('multilayer perceptron', perceptron_cost)

y_pred_chi_nn=clf.predict(best_test_features)
nn_chi_cost = calculate_cost(test_labels,y_pred_chi_nn)
print(nn_chi_cost)

nn_chi_cost = calculate_cost(test_labels,y_pred_chi_nn)
print(nn_chi_cost)

"""CHI ROC NN"""

lr_fpr_chi_nn, lr_tpr_chi_nn, _ = roc_curve(test_labels,y_pred_chi_test)

"""validation"""

c = 0
for i in validation_labels:
  if i == 1:
    c+=1

print('validation failures count is', c)
print('validation failures cost is', c*500,'$')

"""Test"""

c = 0
for i in test_labels:
  if i == 1:
    c+=1

print('test failures count is', c)
print('tets failures cost is', c*500,'$')

# accuracy: (tp + tn) / (p + n)
accuracy = accuracy_score(test_labels, y_pred_chi_nn)
print('Accuracy: %f' % accuracy)
# precision tp / (tp + fp)
precision = precision_score(test_labels, y_pred_chi_nn)
print('Precision: %f' % precision)
# recall: tp / (tp + fn)
recall = recall_score(test_labels, y_pred_chi_nn)
print('Recall: %f' % recall)
# f1: 2 tp / (2 tp + fp + fn)
f1 = f1_score(test_labels, y_pred_chi_nn)
print('F1 score: %f' % f1)


# ROC AUC
auc = roc_auc_score(test_labels, y_pred_chi_nn)
print('ROC AUC: %f' % auc)
# confusion matrix
matrix = confusion_matrix(test_labels, y_pred_chi_nn)
print(matrix)

# generate a no skill prediction (majority class)
ns_probs = [0 for _ in range(len(test_labels))]

ns_fpr, ns_tpr, _ = roc_curve(test_labels, ns_probs)
lr_fpr, lr_tpr, _ = roc_curve(test_labels, y_pred_chi_nn)

lr_tpr_pca_svm

# plot the roc curve for the model
pyplot.plot(ns_fpr, ns_tpr, linestyle='--', label='Majority Prediction')
pyplot.plot(lr_fpr, lr_tpr, marker='.', label='NN+PCA90',  color='r')
pyplot.plot(lr_fpr_chi_svm, lr_tpr_chi_svm, marker='.', label='SVM+Chi',  color='g')
pyplot.plot(lr_fpr_pca_nn, lr_tpr_pca_nn, marker='.', label='NN+PCA',  color='b')
pyplot.plot(lr_fpr_pca_svm, lr_tpr_pca_svm, marker='.', label='SVM+PCA',  color='k')
pyplot.plot(lr_fpr_chi_gb, lr_tpr_chi_gb, marker='.', label='GB+Chi',  color='m')

# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

