from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

import os,sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def predict(self, X):
        """
        Predict the target variable using the preprocessor and model.
        """
        try:
            X_transformed = self.preprocessor.transform(X)
            predictions = self.model.predict(X_transformed)
            return predictions
        except Exception as e:
            raise NetworkSecurityException(e, sys)