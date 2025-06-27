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
"""
Data Ingestion and Preprocessing Module
"""

DATA_INGESTION_COLLECTION_NAME = "phishing_data"
DATA_INGESTION_DATABASE_NAME = "network_security_db"
DATA_INGESTION_DIR_NAME = "networksecurity_data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR= "feature_store"
DATA_INGESTION_INGESTED_DIR= "ingested_data"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2