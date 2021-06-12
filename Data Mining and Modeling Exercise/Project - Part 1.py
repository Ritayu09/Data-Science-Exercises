#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV

# loading dataset
data = pd.read_excel('diseases_hormonalmeasurements - Prepared Data.xlsx', sheet_name = 'Data')

# observing first few rows of data
data.head(10)

# gathering information on data
data.info()

# identifying fraction of missign values in the dataset
missing_frac = np.round(data.isnull().sum()/len(data), 2)
missing_frac

# Few of data variables have very high fraction of missing values. We will remove all such columns from our data for preparing a Robust data model and therefore threshold for removing values is set at 0.23    

del_columns = list(missing_frac[missing_frac>0.23].index)

# Updating data by removing redundant columns
required_columns = list(set(data.columns) - set(del_columns))
data_2 = data[required_columns]


# missing values are updated with the average value calculated from other data points within the same disease category
cleaned_data = pd.DataFrame()

# creating a function to update values
def fill_missing(data, disease_var):
    filtered_data = data[data['Disease'] == disease_var]
    for data_column in data.columns:
        if filtered_data[data_column].dtypes.kind != 'O':
            filtered_data[data_column].fillna(filtered_data[data_column].mean(), inplace = True)
        else:
            filtered_data[data_column].fillna(filtered_data[data_column].mode(), inplace = True)
    return filtered_data


for disease_category in list(data_2['Disease'].unique()):
    interim_data = fill_missing(data_2, disease_category)
    cleaned_data = pd.concat([cleaned_data, interim_data])
          
# Checking whether all missing values have been addressed now
np.round(cleaned_data.isnull().sum()/len(cleaned_data), 2)

# After cleaning the data, next step is putting data in correct format for machine learning algorithm
# String output are updated to numeric entries to be easily feed into model fitting process

cleaned_data['Gender'] = cleaned_data['Gender'].map({'F':0, 'M':1})
cleaned_data['Sick'] = cleaned_data['Sick'].map({'No':0, 'Yes':1})

# setting columns in order and removing columns that are not required like Patient ID
column_order = ['Gender', 'aldosterone', 'cortisol', 'dheas','corticosterone', '11-Deoxycortisol',
               'androstenedion', '11-Deoksicortikosterone', 'testosterone', 'dhea', '17-OH-Pregnenolone',
               '17-OH-Progesterone', 'progesterone', 'androsterone', 'pregnenolone','Disease', 'Sick']

cleaned_data = cleaned_data[column_order]

# We do not need 'Disease' column in Part A therefore dropping that column

part_1 = cleaned_data.drop(['Disease'], axis = 1)


# splitting data into training and testing in 80-20 ratio using stratified sampling technique

train, test = train_test_split(part_1, test_size = 0.20, stratify = part_1['Sick'], random_state = 9)

# standardizing data before training random forest classifier

X_train = train.iloc[:,:-1].values
Y_train = train.iloc[:,-1].values

X_test = test.iloc[:,:-1].values
Y_test = test.iloc[:,-1].values

# Normalizing data values for Random Forest Model
norm = StandardScaler()
X_train[:,1:] = norm.fit_transform(X_train[:,1:])
X_test[:,1:] = norm.transform(X_test[:,1:])

# training the Random Forest model with base parameters
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, Y_train)

# Prediction on Test set 
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
conf_matrix = confusion_matrix(Y_test, y_pred)
conf_matrix

# Prediction Accuracy
classifier.score(X_test, Y_test)

# Hyper Parameter Tuning using GridSearch and 10-Fold Cross Validation to identify most suitable parameters for Random Forest Model
parameters = {'criterion': ['gini', 'entropy'],
             'max_depth': [5, 10, None],
             'max_features': ['auto', 'sqrt'],
             'min_samples_leaf': [1, 2],
             'min_samples_split': [2, 5],
             'n_estimators': [5, 10, 15, 50, 75]}

grid_search = GridSearchCV(estimator = classifier,
                           param_grid = parameters,
                           scoring = 'accuracy',
                           cv = 10,
                           n_jobs = -1)

grid_search = grid_search.fit(X_train, Y_train)
best_accuracy = grid_search.best_score_
best_accuracy
best_parameters = grid_search.best_params_
best_parameters

# Preparing Final Model
best_classifier = RandomForestClassifier(n_estimators = 50, criterion = 'entropy', max_depth=10, max_features= 'auto', min_samples_leaf= 2, min_samples_split= 5, random_state = 13)
best_classifier.fit(X_train, Y_train)


# Predicting the Test set results
y_pred = best_classifier.predict(X_test)

# Making the Confusion Matrix
conf_matrix = confusion_matrix(Y_test, y_pred)
conf_matrix

# Prediction Accuracy
best_classifier.score(X_test, Y_test)
