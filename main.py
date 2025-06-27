from networksecurity.component.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.congif_entity import DataIngestionConfig
from networksecurity.entity.congif_entity import TrainingPipelineConfig
import os
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        Data_Ingestion = DataIngestion(data_ingestion_config)
        logging.info("Data ingestion started")
        data_ingestion_artifact = Data_Ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
