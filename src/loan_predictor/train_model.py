import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

import time
import joblib
import pandas as pd
import numpy as np

from src.loan_predictor.prepare_data import prepare_data
from src.loan_predictor.model import model_NN


def save_accuracy(eval_model, file_name, timestr):
    df_accuracy = pd.DataFrame({
        "Validation Accuracy": [eval_model[1]]
    }, index=None)
    
    file_name = file_name + "_" + timestr + ".csv"
    file_name_final = BASE_DIR + "/results/loan_predictor/model_val_accuracy/" + file_name
    
    df_accuracy.to_csv(file_name_final, index=False)


def save_model(classifier, file_name, timestr):
    file_name = file_name + "_" + timestr + ".h5"
    file_name_final = BASE_DIR + "/results/loan_predictor/model_file/" + file_name
    classifier.save(file_name_final)


def save_scaler(scaler, file_name, timestr):
    file_name = file_name + "_" + timestr + ".save"
    file_name_final = BASE_DIR + "/results/loan_predictor/model_scaler/" + file_name
    joblib.dump(scaler, file_name_final) 


def save_features(feature_list, file_name, timestr):
    file_name = file_name + "_" + timestr + ".csv"
    file_name_final = BASE_DIR + "/results/loan_predictor/model_features/" + file_name
    pd.DataFrame(
        0, index=np.arange(1), columns=feature_list
    ).to_csv(file_name_final, index=False)


def main():
    data = pd.read_csv("data/loan_predictor/raw/bankloan.csv")
    X_train_final, y_train_final, X_test_final, y_test_final, scaler, feature_list = prepare_data(data)
    classifier = model_NN(X_train_final, y_train_final)
    eval_model = classifier.evaluate(X_test_final, y_test_final)
    timestr = time.strftime("%Y%m%d_%H%M%S")
    save_accuracy(eval_model, "val_accuracy", timestr)
    save_model(classifier, "model", timestr)
    save_scaler(scaler, "scaler", timestr)
    save_features(feature_list, "features", timestr)

    return print("Model trained!!")


if __name__ == "__main__":
    main()