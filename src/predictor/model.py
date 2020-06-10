import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

print(BASE_DIR)
import yaml
from keras import Sequential
from keras.layers import Dense

with open("parameters.yml", "r") as params:
    param_dict = yaml.safe_load(params) 


def model_NN(X_train_final, y_train_final):
    classifier = Sequential()
    classifier.add(Dense(param_dict["model"]["dense_1"], activation='relu', kernel_initializer='random_normal', input_dim=X_train_final.shape[1]))
    classifier.add(Dense(param_dict["model"]["dense_2"], activation='relu', kernel_initializer='random_normal'))
    classifier.add(Dense(param_dict["model"]["dense_3"], activation='relu', kernel_initializer='random_normal'))
    classifier.add(Dense(param_dict["model"]["dense_4"], activation='sigmoid', kernel_initializer='random_normal'))
    classifier.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    classifier.fit(
        X_train_final, 
        y_train_final, 
        batch_size=param_dict["model"]["batch_size"], 
        epochs=param_dict["model"]["epochs"], 
        verbose=0
    )
    
    return classifier