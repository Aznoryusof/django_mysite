import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

import joblib
import re
import pandas as pd

from keras.models import load_model
from src.loan_predictor.prepare_data import get_test_dummies


def _get_latest_model(list):
    result = [re.sub("model_", "", ver) for ver in list]
    result = [re.sub("_", "", ver) for ver in result]
    result = [re.sub(".h5", "", ver) for ver in result]
    
    max_index = result.index(max(result))

    return list[max_index]


def _get_latest_scaler(list):
    result = [re.sub("scaler", "", ver) for ver in list]
    result = [re.sub("_", "", ver) for ver in result]
    result = [re.sub(".save", "", ver) for ver in result]
    
    max_index = result.index(max(result))

    return list[max_index]


def _get_latest_features(list):
    result = [re.sub("feature_list", "", ver) for ver in list]
    result = [re.sub("_", "", ver) for ver in result]
    result = [re.sub(".csv", "", ver) for ver in result]
    
    max_index = result.index(max(result))

    return list[max_index]


def _process_client_data(df, scaler, model, features):
    client_data_dumm = get_test_dummies(features, df)
    client_data_scaled = scaler.transform(client_data_dumm)
    
    return client_data_scaled


def _prediction(model, data, threshold=0.5):
    y_pred = model.predict(data)
    y_pred_bool = y_pred >= threshold
    if y_pred_bool == True:
        y_pred_status = "Approved"
    else:
        y_pred_status = "Rejected"

    return y_pred_status


def make_prediction(mydata):
    model_path = BASE_DIR + "/results/loan_predictor/model_file/"
    files = [f for f in os.listdir(model_path) if f.endswith('.h5')]
    latest_model_name = _get_latest_model(files)
    model = load_model(model_path + latest_model_name)

    scaler_path = BASE_DIR + "/results/loan_predictor/model_scaler/"
    files = [f for f in os.listdir(scaler_path) if f.endswith('.save')]
    latest_scaler_name = _get_latest_scaler(files)
    scaler = joblib.load(scaler_path + latest_scaler_name) 

    features_path = BASE_DIR + "/results/loan_predictor/model_features/"
    files = [f for f in os.listdir(features_path) if f.endswith('.csv')]
    latest_features_name = _get_latest_features(files)
    features = pd.read_csv(features_path + latest_features_name)

    # client_data = pd.read_csv(path)
    # X_client_processed = _process_client_data(client_data, scaler, model, features)

    X_client_processed = _process_client_data(mydata, scaler, model, features)
    result = _prediction(model, X_client_processed, 0.5)

    return result


if __name__ == "__main__":
    df_reject = pd.DataFrame(
        {
            "Firstname": "Aznor",
            "Lastname": "Yusof", 
            "Gender": "Male",
            "Married": "Yes",
            "Dependents": 4,
            "Education": "Graduate",
            "Self_Employed": "Yes",
            "ApplicantIncome": 0,
            "CoapplicantIncome": 0,
            "LoanAmount": 10000000,
            "Loan_Amount_Term": 10,
            "Credit_History": 0,
            "Property_Area": "Rural"
        }, index=[0]
    )

    df_approve = pd.DataFrame(
        {
            "Firstname": "Aznor",
            "Lastname": "Yusof", 
            "Gender": "Male",
            "Married": "Yes",
            "Dependents": 1,
            "Education": "Graduate",
            "Self_Employed": "Yes",
            "ApplicantIncome": 100000,
            "CoapplicantIncome": 0,
            "LoanAmount": 20,
            "Loan_Amount_Term": 2,
            "Credit_History": 1,
            "Property_Area": "Urban"
        }, index=[0]
    )

    df_reject = df_reject.drop(["Firstname", "Lastname"], axis=1)
    df_approve = df_approve.drop(["Firstname", "Lastname"], axis=1)

    assert make_prediction(df_reject) == "Rejected"
    assert make_prediction(df_approve) == "Approved"
    print("\n")
    print("Prediction Successful!")
