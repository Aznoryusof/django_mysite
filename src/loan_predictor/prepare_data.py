import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

import yaml
import pandas as pd
import numpy as np

from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

with open(os.path.join(BASE_DIR, "parameters.yml"), "r") as params:
    param_dict = yaml.safe_load(params) 


def clean_data(df):
    df_clean = df.copy()
    df_clean = df_clean.dropna()
    df_clean = df_clean.drop("Loan_ID", axis=1)
    df_clean["LoanAmount"] = (df_clean["LoanAmount"] * 1000).astype(int)

    return df_clean


def split_train_test(df, test_ratio, seed):
    np.random.seed(seed)
    shuffled_indices = np.random.permutation(len(df))
    test_set_size = int(len(df) * test_ratio)
    
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    
    train_set = df.iloc[train_indices]
    test_set = df.iloc[test_indices]

    return train_set.loc[:, train_set.columns != "Loan_Status"], train_set["Loan_Status"], test_set.loc[:, test_set.columns != "Loan_Status"], test_set["Loan_Status"]


def get_test_dummies(X_train_dumm, X_test):
    X_test_dumm = pd.get_dummies(X_test)
    missing_cols = set(X_train_dumm.columns) - set(X_test_dumm.columns)
    for col in missing_cols:
        X_test_dumm[col] = 0

    X_test_dumm = X_test_dumm[X_train_dumm.columns]
    
    return X_test_dumm


def label_encode_y(y_train, y_test):
    y_train_enc = y_train.map(dict(Y=1, N=0))
    y_test_enc = y_test.map(dict(Y=1, N=0))

    return y_train_enc, y_test_enc


def dummify_X(X_train, X_test):
    X_train_dumm = pd.get_dummies(X_train)
    X_test_dumm = get_test_dummies(X_train_dumm, X_test)

    return X_train_dumm, X_test_dumm


def smote_scale(X_train_dumm, y_train_enc):
    smote = SMOTE(sampling_strategy='minority')
    X_train_smote, y_train_smote = smote.fit_sample(X_train_dumm, y_train_enc)
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train_smote)

    return X_train_scaled, y_train_smote, scaler


def scale_test(X_test_dumm, y_test_enc, scaler):
    y_test_final = y_test_enc
    X_test_final = scaler.transform(X_test_dumm)

    return X_test_final, y_test_final


def get_feature_list(X_train_dumm):
    
    return X_train_dumm.columns.tolist()


def prepare_data(df):
    df_clean = clean_data(df)
    X_train, y_train, X_test, y_test = split_train_test(df_clean, param_dict["test_ratio"], param_dict["seed"])
    y_train_enc, y_test_enc = label_encode_y(y_train, y_test)
    X_train_dumm, X_test_dumm = dummify_X(X_train, X_test)
    X_train_final, y_train_final, scaler = smote_scale(X_train_dumm, y_train_enc)
    X_test_final, y_test_final = scale_test(X_test_dumm, y_test_enc, scaler)
    feature_list = get_feature_list(X_train_dumm)

    return X_train_final, y_train_final, X_test_final, y_test_final, scaler, feature_list