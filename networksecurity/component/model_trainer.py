import os,sys

import mlflow.sklearn

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.congif_entity import ModelTrainerConfig

from networksecurity.utils.main_utils.utils import load_object,save_object,load_numpy_array_data,evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metrics import get_classification_metrics
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier,AdaBoostClassifier
import mlflow


class ModelTrainer:
    def __init__(self,model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def track_mlflow(self,model,classification_metrics):
        with mlflow.start_run():
            f1_score = classification_metrics.f1_score
            precision_score = classification_metrics.precision_score
            recall_score = classification_metrics.recall_score
            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)
            mlflow.sklearn.log_model(model, "model")

    def train_model(self, X_train, y_train,X_test,y_test):
        try:
            model = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
            params={
                "Decision Tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    'splitter':['best','random'],
                    'max_features':['sqrt','log2'],
                    },
                "Random Forest":{
                    'criterion':['gini', 'entropy', 'log_loss'],
                    'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                    },
                "Gradient Boosting":{
                    'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    'criterion':['squared_error', 'friedman_mse'],
                    'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                    },
                "Logistic Regression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }
            
            }
            model_report:dict = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                                               models=model, params=params)

            best_model_score = max(list(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model=model[best_model_name]
            y_train_pred=best_model.predict(X_train)

            classification_train_metrics=get_classification_metrics(y_true=y_train, y_pred=y_train_pred)

            #Track the ml flow
            self.track_mlflow(best_model,classification_train_metrics)

            y_test_pred=best_model.predict(X_test)
            classification_test_metrics=get_classification_metrics(y_true=y_test, y_pred=y_test_pred)

            preprocessor =load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path= os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)
            Network_Model= NetworkModel(
                model=best_model,
                preprocessor=preprocessor,
            )
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=Network_Model)
            save_object(file_path="final_model/model.pkl", obj=Network_Model)

            ##Model Trainer Artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metrics,
                test_metric_artifact=classification_test_metrics
            )
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_train_model(self):
        """
        Train the model using the preprocessed data.
        """
        try:
            logging.info("Loading preprocessor and model")

            #load training data and test data
            logging.info("Loading training data")
            train_data = load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            logging.info("Loading test data")
            test_data = load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)

            # Extract features and target variable
            X_train = train_data[:, :-1]  # All columns except the last one
            y_train = train_data[:, -1]    # Last column as target variable
            X_test = test_data[:, :-1]      # All columns except the last one
            y_test = test_data[:, -1]       # Last column as target variable

            model_trainer_artifact=self.train_model(X_train,y_train,X_test,y_test)

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    

