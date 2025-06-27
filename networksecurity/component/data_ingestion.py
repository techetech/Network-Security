from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


##configuration for the data ingestion module

from networksecurity.entity.congif_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import ArtifactEntity
import os
import sys
import numpy as np
import pymongo
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")

class DataIngestion:
    def __init__(self,data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def export_collection_as_dataframe(self):
        """
        Export MongoDB collection to a pandas DataFrame.
        """
        try:
            self.client = pymongo.MongoClient(MONGO_DB_URI)
            database = self.client[self.data_ingestion_config.database_name]
            collection_name = self.data_ingestion_config.collection_name
            collection = database[collection_name]

            dataframe = pd.DataFrame(list(collection.find()))

            if "_id" in dataframe.columns:
                dataframe.drop(columns=["_id"], axis=1, inplace=True)
            dataframe.replace({"na": np.nan, "NaN": np.nan, "null": np.nan}, inplace=True)
            return dataframe
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> List[pd.DataFrame]:
        """
        Split the DataFrame into train and test sets.
        """
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            logging.info("Performed train-test split")

            logging.info("Exited split_data_as_train_test method")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info("Exported data into feature store directory")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info(f"Train and test data exported to {self.data_ingestion_config.training_file_path} and {self.data_ingestion_config.testing_file_path} respectively")

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            ##splitting data into train and test set
            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = ArtifactEntity(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return data_ingestion_artifact

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        """
        Export the DataFrame to the feature store directory.
        """
        try:
            feature_store_dir = self.data_ingestion_config.feature_store_dir
            ##creating folder
            dir_path=os.path.dirname(feature_store_dir)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_dir, index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)
