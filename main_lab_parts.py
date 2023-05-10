# -*- coding: utf-8 -*-
"""LAB1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r67WGdRadF2QPDw5x6mHnAoa-VlmwH7-
"""

#!tar -xvf data.tar

"""import os
import csv
import pandas as pd

def extract_df(Folder):
    data_frames = []

    for filename in os.listdir(os.path.join('data', Folder)):
          with open(os.path.join('data', Folder, filename), 'r') as f:
              reader = csv.reader(f, delimiter='|')
              data = [row for row in reader]
              headers = data[0]
              df = pd.DataFrame(data[1:], columns=headers)
              df['index'] = os.path.join(Folder, filename)
              if (df['SepsisLabel'] == '1').any():
                  index_of_first_1 = (df['SepsisLabel'] == '1').idxmax()
                  df['label'] = 1
                  df = df.iloc[:index_of_first_1+1]
              else:
                  df['label'] = 0
              data_frames.append(df)

    df_all = pd.concat(data_frames, ignore_index=True)
    df_all.loc[:, df_all.columns != 'index'] = df_all.loc[:, df_all.columns != 'index'].apply(pd.to_numeric, errors='coerce')
    return df_all

train_df = extract_df('train')
test_df = extract_df('test')
train_df.to_csv('train.csv', index=False)
test_df.to_csv('test.csv', index=False)

from google.colab import drive
#drive.mount('/content/gdrive')
import zipfile

# Specify the file names and paths
file1 = '/content/train.csv'
file2 = '/content/test.csv'
zip_path = '/content/gdrive/My Drive/train_test_csv.zip'

# Create a ZipFile object and add the files to it
with zipfile.ZipFile(zip_path, 'w') as zip_file:
    zip_file.write(file1)
    zip_file.write(file2)
import os

# Check that the file was created
if os.path.exists(zip_path):
    print('File saved successfully to Google Drive')
else:
    print('File not found')
""
"""

from google.colab import drive
import pandas as pd
import zipfile

drive.mount('/content/gdrive')

zip_path = '/content/gdrive/MyDrive/train_test_csv.zip'
with zipfile.ZipFile(zip_path, 'r') as zip_file:
    zip_file.extractall('/content/train_test_csv')


train_path = '/content/train_test_csv/content/train.csv'
test_path = '/content/train_test_csv/content/test.csv'

train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

def grouped(df_to_groupby):
    df_to_groupby.drop(columns=['SepsisLabel'])  

    to_stats = ['HR', 'O2Sat', 'Temp', 'SBP', 'MAP', 'DBP', 'Resp', 'EtCO2',
          'BaseExcess', 'HCO3', 'FiO2', 'pH', 'PaCO2', 'SaO2', 'AST', 'BUN',
          'Alkalinephos', 'Calcium', 'Chloride', 'Creatinine', 'Bilirubin_direct',
          'Glucose', 'Lactate', 'Magnesium', 'Phosphate', 'Potassium',
          'Bilirubin_total', 'TroponinI', 'Hct', 'Hgb', 'PTT', 'WBC',
          'Fibrinogen', 'Platelets', 'Age', 'Gender', 'HospAdmTime', 'ICULOS','label']

    import numpy as np

    # Group by index column and apply multiple aggregation functions
    agg_dict = {'HR': ['mean', 'std'], 
                'O2Sat': ['mean', 'std'], 
                'Temp': ['mean', 'std'], 
                'SBP': ['mean', 'std'], 
                'MAP': ['mean',  'std'], 
                'DBP': ['mean', 'std'], 
                'Resp': ['mean', 'std'], 
                'EtCO2': ['mean', 'std'], 

                'BaseExcess': ['mean', 'std'], 
                'HCO3': ['mean', 'std'], 
                'FiO2': ['mean', 'std'], 
                'pH': ['mean', 'std'], 
                'PaCO2': ['mean', 'std'], 
                'SaO2': ['mean', 'std'], 
                'AST': ['mean', 'std'], 
                'BUN': ['mean', 'std'], 

                'Alkalinephos': ['mean','std'], 
                'Calcium': ['mean', 'std'], 
                'Chloride': ['mean', 'std'], 
                'Creatinine': ['mean', 'std'], 
                'Bilirubin_direct': ['mean', 'std'], 

                'Glucose': ['mean', 'std'], 
                'Lactate': ['mean',  'std'], 
                'Magnesium': ['mean', 'std'], 
                'Phosphate': ['mean', 'std'], 
                'Potassium': ['mean', 'std'], 

                'Bilirubin_total': ['mean', 'std'], 
                'TroponinI': ['mean', 'std'], 
                'Hct': ['mean', 'std'], 
                'Hgb': ['mean', 'std'], 
                'PTT': ['mean', 'std'], 
                'WBC': ['mean', 'std'], 

                'Fibrinogen': ['mean', 'std'], 
                'Platelets': ['mean', 'std'], 
                'Age': ['mean'], 
                'Gender': ['mean'],  
                'HospAdmTime': ['mean'], 
                'ICULOS': ['mean', 'std'], 
                'label': ['mean'], 
                }

    grouped_df = df_to_groupby.groupby('index')[to_stats].agg(agg_dict)

    # Flatten column names in the resulting DataFrame
    grouped_df.columns = ['_'.join(col).strip() for col in grouped_df.columns.values]

    # Reset the index to make the groupby column a regular column
    grouped_df = grouped_df.reset_index()
    grouped_df = grouped_df.drop(columns=['index'])
    return grouped_df


train_grouped = grouped(train_df)
test_grouped = grouped(test_df)

def impute_knn(df_to_impute):
    dropped = 0
    if 'label_mean' in df_to_impute.columns:
        dropped = df_to_impute.pop('label_mean')

    missing_cols = [col for col in df_to_impute.columns if df_to_impute[col].isnull().any()]
    missing_cols_idx = [df_to_impute.columns.get_loc(col) for col in missing_cols]

    imputer = KNNImputer(n_neighbors=3)
    df_imputed = pd.DataFrame(imputer.fit_transform(df_to_impute), columns=df_to_impute.columns)
    if dropped != 0:
        return pd.concat([df_imputed, dropped], axis=1)
    else:
        return df_imputed

from sklearn.metrics import f1_score
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer
import pandas as pd


try1 = ['HR_mean', 'O2Sat_mean', 'Temp_mean', 'MAP_mean',  'Resp_mean', 'Hgb_mean',
       'WBC_mean', 'HospAdmTime_mean', 'ICULOS_mean',
       'ICULOS_std','label_mean']

try2 = ['HR_mean', 'O2Sat_mean', 'Temp_mean', 'MAP_mean',  'Resp_mean','Chloride_mean', 'Lactate_mean', 'Hct_mean', 'Hgb_mean',
       'WBC_mean', 'Platelets_std', 'HospAdmTime_mean', 'ICULOS_mean',
       'ICULOS_std','label_mean']
train_grouped_copy = impute_knn(train_grouped[try2])
test_grouped_copy = impute_knn(test_grouped[try2])

X_train = train_grouped_copy.drop('label_mean', axis=1)
y_train = train_grouped_copy['label_mean']

X_test = test_grouped_copy.drop('label_mean', axis=1)
y_test = test_grouped_copy['label_mean']

from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100, random_state=42)

rf.fit(X_train, y_train)

# Predict the train data
y_pred_train = rf.predict(X_train)

f1_train = f1_score(y_pred_train, y_train)

# Predict the test data
y_pred_test = rf.predict(X_test)

f1_test = f1_score(y_test, y_pred_test)

print("F1 train score:", f1_train)
print("F1 test score:", f1_test)

from keras.models import Sequential
from keras.layers import Dense
import torch.nn as nn
import numpy as np

# create neural network model
model = Sequential()
model.add(Dense(256, input_dim=X_train.shape[1], activation='relu')) 
model.add(Dense(32, activation='relu')) 
model.add(Dense(1, activation='sigmoid')) 

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=100, batch_size=16, verbose=0)

y_pred_nn = model.predict(X_test)
y_pred_train = model.predict(X_train)

threshold = 0.55
binary_predictions_test = np.where(y_pred_nn > threshold, 1, 0)
binary_predictions_train = np.where(y_pred_train > threshold, 1, 0)

f1_nn = f1_score(y_test, binary_predictions_test)
f1_train = f1_score(y_train, binary_predictions_train)

print(f"F1 score for neural network train: {f1_train:.4f}")
print(f"F1 score for neural network test: {f1_nn:.4f}")

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import f1_score

gbm = GradientBoostingClassifier(learning_rate=0.12, subsample=0.8, n_estimators=200, random_state=42)

gbm.fit(X_train, y_train)

# Predict the train data
y_pred_train = gbm.predict(X_train)

f1_train = f1_score(y_pred_train, y_train)

# Predict the test data
y_pred_test = gbm.predict(X_test)

f1_test = f1_score(y_test, y_pred_test)

print("F1 train score:", f1_train)
print("F1 test score:", f1_test)

import joblib

def make_comp_model(train_grouped, test_grouped):
  df_comp = pd.concat([train_grouped, test_grouped], ignore_index=True)
  comp_grouped_copy = impute_knn(df_comp[try2])
  X_comp = train_grouped_copy.drop('label_mean', axis=1)
  y_comp = train_grouped_copy['label_mean']
  gbm.fit(X_comp, y_comp)
  joblib.dump(gbm, 'comp_gbm_model.joblib')

make_comp_model(train_grouped, test_grouped)

import sys, os, csv
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import joblib

# predict.py

def extract_df_comp(Folder):
    data_frames = []

    for filename in os.listdir(Folder):
          with open(os.path.join('data', Folder, filename), 'r') as f:
              reader = csv.reader(f, delimiter='|')
              data = [row for row in reader]
              headers = data[0]
              df = pd.DataFrame(data[1:], columns=headers)
              df['index'] = filename
              
              data_frames.append(df)

    df_all = pd.concat(data_frames, ignore_index=True)
    df_all.loc[:, df_all.columns != 'index'] = df_all.loc[:, df_all.columns != 'index'].apply(pd.to_numeric, errors='coerce')

    return df_all

def grouped_comp(df_to_groupby):
    to_stats = ['HR', 'O2Sat', 'Temp', 'SBP', 'MAP', 'DBP', 'Resp', 'EtCO2',
          'BaseExcess', 'HCO3', 'FiO2', 'pH', 'PaCO2', 'SaO2', 'AST', 'BUN',
          'Alkalinephos', 'Calcium', 'Chloride', 'Creatinine', 'Bilirubin_direct',
          'Glucose', 'Lactate', 'Magnesium', 'Phosphate', 'Potassium',
          'Bilirubin_total', 'TroponinI', 'Hct', 'Hgb', 'PTT', 'WBC',
          'Fibrinogen', 'Platelets', 'Age', 'Gender', 'HospAdmTime', 'ICULOS']


    # Group by index column and apply multiple aggregation functions
    agg_dict = {'HR': ['mean', 'std'], 
                'O2Sat': ['mean', 'std'], 
                'Temp': ['mean', 'std'], 
                'SBP': ['mean', 'std'], 
                'MAP': ['mean',  'std'], 
                'DBP': ['mean', 'std'], 
                'Resp': ['mean', 'std'], 
                'EtCO2': ['mean', 'std'], 

                'BaseExcess': ['mean', 'std'], 
                'HCO3': ['mean', 'std'], 
                'FiO2': ['mean', 'std'], 
                'pH': ['mean', 'std'], 
                'PaCO2': ['mean', 'std'], 
                'SaO2': ['mean', 'std'], 
                'AST': ['mean', 'std'], 
                'BUN': ['mean', 'std'], 

                'Alkalinephos': ['mean','std'], 
                'Calcium': ['mean', 'std'], 
                'Chloride': ['mean', 'std'], 
                'Creatinine': ['mean', 'std'], 
                'Bilirubin_direct': ['mean', 'std'], 

                'Glucose': ['mean', 'std'], 
                'Lactate': ['mean',  'std'], 
                'Magnesium': ['mean', 'std'], 
                'Phosphate': ['mean', 'std'], 
                'Potassium': ['mean', 'std'], 

                'Bilirubin_total': ['mean', 'std'], 
                'TroponinI': ['mean', 'std'], 
                'Hct': ['mean', 'std'], 
                'Hgb': ['mean', 'std'], 
                'PTT': ['mean', 'std'], 
                'WBC': ['mean', 'std'], 

                'Fibrinogen': ['mean', 'std'], 
                'Platelets': ['mean', 'std'], 
                'Age': ['mean'], 
                'Gender': ['mean'],  
                'HospAdmTime': ['mean'], 
                'ICULOS': ['mean', 'std'], 
                }

    grouped_df = df_to_groupby.groupby('index')[to_stats].agg(agg_dict)

    # Flatten column names in the resulting DataFrame
    grouped_df.columns = ['_'.join(col).strip() for col in grouped_df.columns.values]

    # Reset the index to make the groupby column a regular column
    grouped_df = grouped_df.reset_index()
    return grouped_df

def impute_knn_comp(df_to_impute):
    missing_cols = [col for col in df_to_impute.columns if df_to_impute[col].isnull().any()]
    missing_cols_idx = [df_to_impute.columns.get_loc(col) for col in missing_cols]

    imputer = KNNImputer(n_neighbors=3)
    df_imputed = pd.DataFrame(imputer.fit_transform(df_to_impute), columns=df_to_impute.columns)
    return df_imputed


# Define the path to the patient tables folder as the first argument in the command line
folder_path = sys.argv[1]

test_df = extract_df_comp(folder_path)
print(test_df, '*'*50)
test_df_grouped = grouped_comp(test_df)
print(test_df_grouped, '*'*50)

best_cols = ['HR_mean', 'O2Sat_mean', 'Temp_mean', 'MAP_mean',  'Resp_mean','Chloride_mean', 'Lactate_mean', 'Hct_mean', 'Hgb_mean',
      'WBC_mean', 'Platelets_std', 'HospAdmTime_mean', 'ICULOS_mean',
      'ICULOS_std']
test_grouped_copy = impute_knn_comp(test_df_grouped[best_cols])

print(test_grouped_copy, '*'*50)

gbm_loaded = joblib.load('comp_gbm_model.joblib')
y_pred = gbm_loaded.predict(test_grouped_copy)
print('sum is:', np,sum(y_pred))
new_df = pd.DataFrame({'id': test_df_grouped['index'], 'prediction': y_pred})
new_df.to_csv('prediction.csv', index=False)

test_df = pd.read_csv('/content/prediction.csv')
y_pred_test = test_df['prediction']
y_test = y_train
f1_test = f1_score(y_test, y_pred_test)

print("F1 train score:", f1_test)

import shutil
from google.colab import drive
import zipfile

# copy the zip file to current directory
drive.mount('/content/drive')
zip_file_path = '/content/drive/MyDrive/folder_to_zip.zip'

shutil.copy(zip_file_path, '/content')

# to load the zip file from drive:
with zipfile.ZipFile(zip_file_path, 'r') as zip:
    zip.extractall('/content/data')