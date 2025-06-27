from datetime import datetime
import os
from networksecurity.constant import training_pipeline

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")):
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.DATA_INGESTION_DIR_NAME = training_pipeline.DATA_INGESTION_DIR_NAME
        self.DATA_INGESTION_FEATURE_STORE_DIR = training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR
        self.DATA_INGESTION_INGESTED_DIR = training_pipeline.DATA_INGESTION_INGESTED_DIR
        self.DATA_INGESTION_COLLECTION_NAME = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.DATA_INGESTION_DATABASE_NAME = training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.TRAIN_FILE_NAME = training_pipeline.TRAIN_FILE_NAME
        self.TEST_FILE_NAME = training_pipeline.TEST_FILE_NAME
        self.timestamp = timestamp
        self.artifact_dir = os.path.join(self.artifact_name, self.timestamp)
        self.training_pipeline_dir = os.path.join(os.getcwd(), self.pipeline_name)
        

class DataIngestionConfig:
    def __init__(self, training_pipeline: TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(
            training_pipeline.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME
        )
        
        self.feature_store_dir = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR
        )
        self.training_file_path = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME
        )
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

        