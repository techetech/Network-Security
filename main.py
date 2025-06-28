from networksecurity.component.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.congif_entity import DataIngestionConfig,DataValidationConfig, TrainingPipelineConfig,DataTransformationConfig
from networksecurity.component.data_validation import DataValidation
from networksecurity.component.data_transformation import DataTransformation
import os
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        Data_Ingestion = DataIngestion(data_ingestion_config)
        logging.info("Data ingestion started")
        dataingestionartifact=Data_Ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        print(dataingestionartifact)

        logging.info("Data validation started")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_validation_config, dataingestionartifact)
        logging.info("Initiating data validation")
        # Validate the data
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_artifact)

        ## Data Transformation
        logging.info("Data transformation started")
        data_transformation_config= DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        logging.info("Initiating data transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation completed")
        print(data_transformation_artifact)

        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
