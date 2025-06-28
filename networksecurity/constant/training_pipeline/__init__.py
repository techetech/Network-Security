import os
import sys
import numpy as np
import pandas as pd


"""
defining common constant variable for training pipeline
"""
TARGET_COLUMN_NAME = "Result"
PIPELINE_NAME = "NetworkSecurity"
ARTIFACT_DIR = "Artifacts"
FILE_NAME="phishingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

"""
Data Ingestion and Preprocessing Module
"""

DATA_INGESTION_COLLECTION_NAME = "phishing_data"
DATA_INGESTION_DATABASE_NAME = "network_security_db"
DATA_INGESTION_DIR_NAME = "Data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR= "feature_store"
DATA_INGESTION_INGESTED_DIR= "ingested_data"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2

"""
DATA VALIDATION MODULE
"""

DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_INVALID_DIR = "invalid_data"
DATA_VALIDATION_VALID_DIR = "valid_data"
DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "drift_report.yaml"

"""
DATA TRANSFORMATION MODULE
"""

DATA_TRANSFORMATION_DIR_NAME = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = "transformed_data"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = "transformed_object"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessor.pkl"


# KNN Imputer Parameters to replace missing values
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict={
    "missing_values": np.nan,
    "n_neighbors":3,
    "weights": "uniform",
}