import os,sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.component.data_ingestion import DataIngestion
from networksecurity.component.data_validation import DataValidation
from networksecurity.component.data_transformation import DataTransformation
from networksecurity.component.model_trainer import ModelTrainer

from networksecurity.entity.congif_entity import(
     DataIngestionConfig,
     DataValidationConfig, 
     TrainingPipelineConfig,
     DataTransformationConfig,
     ModelTrainerConfig,
)

from networksecurity.entity.artifact_entity import(
     DataIngestionArtifact,
     DataValidationArtifact,
     DataTransformationArtifact,
     ModelTrainerArtifact,
)

class TrainingPipeline:
    def __init__(self):
        try:
            self.training_pipeline_config = TrainingPipelineConfig()
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_ingestion(self) -> ModelTrainerArtifact:
        try:
            # Data Ingestion
            logging.info("Starting data ingestion process")
            self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            data_ingestion = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            # Data Validation
            logging.info("Starting data validation process")
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_validation_config, data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data validation completed successfully")
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            # Data Transformation
            logging.info("Starting data transformation process")
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data transformation completed successfully")
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)  
        
    def start_model_training(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            # Model Training
            logging.info("Starting model training process")
            model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_train_model()
            logging.info("Model training completed successfully")
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def run_pipeline(self) -> ModelTrainerArtifact:
        """
        Run the entire training pipeline.
        """
        try:
            logging.info("Starting the training pipeline")
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_training(data_transformation_artifact)
            logging.info("Training pipeline completed successfully")
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)