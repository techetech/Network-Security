import sys, os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constant.training_pipeline import TARGET_COLUMN_NAME,DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact

from networksecurity.entity.congif_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self,data_validation_artifact: DataValidationArtifact 
                 ,data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        Reads a CSV file and returns a pandas DataFrame.
        """
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @classmethod
    def get_data_transformation_object(cls) -> Pipeline:
        """
        Creates a data transformation pipeline with KNN imputer.
        """
        try:
            logging.info("Creating data transformation pipeline")
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            pipeline = Pipeline(
                steps=[
                    ('imputer', imputer)
                ]
            )
            return pipeline
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Initiates the data transformation process.
        """
        try:
            logging.info("Starting data transformation process")
            # Read the validated train and test data
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            logging.info("Data read successfully for transformation")
            # Training dataframe
            input_feature_train_df= train_df.drop(columns=[TARGET_COLUMN_NAME], axis=1)
            target_feature_train_df= train_df[TARGET_COLUMN_NAME]
            target_feature_train_df=target_feature_train_df.replace(-1,0)

            # Test dataframe
            input_feature_test_df= test_df.drop(columns=[TARGET_COLUMN_NAME], axis=1)
            target_feature_test_df= test_df[TARGET_COLUMN_NAME]
            target_feature_test_df=target_feature_test_df.replace(-1,0)

            
            preprocessor= self.get_data_transformation_object()
            logging.info("Data transformation pipeline created successfully")
            # Fit the preprocessor on the training data
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor_object.transform(input_feature_test_df)

            train_arr=np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]

            save_numpy_array_data(
                file_path=self.data_transformation_config.transformed_train_file_path,
                array=train_arr
            )
            save_numpy_array_data(
                file_path=self.data_transformation_config.transformed_test_file_path,
                array=test_arr
            )
            save_object(
                file_path=self.data_transformation_config.transformed_object_file_path,
                obj=preprocessor_object
            )
            save_object(
                file_path="final_model/preprocessor.pkl",
                obj=preprocessor_object
            )

            logging.info("Data transformation completed successfully")
            #Preparing the artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)