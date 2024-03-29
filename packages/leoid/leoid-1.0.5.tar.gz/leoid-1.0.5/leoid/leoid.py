import pickle
import numpy as np
import os

class LEOID():
    """Level-based Ensemble for Overcoming Inbalanced Data"""

    def __init__(self):
        with open("leoid/leoid/stage_1.pkl", "rb") as f:
            self.model_1 = pickle.load(f)

        with open("leoid/leoid/stage_2.pkl", "rb") as f:
            self.model_2 = pickle.load(f)
    
    def predict(self, X):
        X = np.array(X)
        if X.ndim == 1:
            X = X.reshape(1, -1)
            
        model_1_predictions = self.model_1.predict(X)
        predictions = []
        for index, model_1_prediction in enumerate(model_1_predictions):
            if model_1_prediction == 1:
                model_2_prediction = self.model_2.predict(X[index].reshape(1, -1))[0]
                if model_2_prediction == 1:
                    predictions.append(2)
                else:
                    predictions.append(1)
            else:
                predictions.append(model_1_prediction)
                
        return np.array(predictions)
