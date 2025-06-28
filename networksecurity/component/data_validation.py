from networksecurity.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from networksecurity.entity.congif_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import os,sys
import pandas as pd
from networksecurity.utils.main_utils.utils import read_yaml_file ,write_yaml_file  


class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)

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
    
    def validate_column_number(self, df: pd.DataFrame) -> bool:
        """
        Validates if the DataFrame has the expected column names.
        """
        try:
            number_of_columns = len(self.schema_config)
            logging.info(f"Expected number of columns: {number_of_columns}, Actual number of columns: {len(df.columns)}")
            if len(df.columns) != number_of_columns:
                logging.error(f"Number of columns mismatch: Expected {number_of_columns}, but got {len(df.columns)}")
                return False
            logging.info("Number of columns validation passed")
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold: float=0.05) -> bool:
        """
        Detects data drift between the base DataFrame and the current DataFrame.
        """
        try:
            status=True
            report={}
            for col in base_df.columns:
                d1=base_df[col]
                d2=current_df[col]
                is_sample_dist=ks_2samp(d1,d2)
                if threshold<=is_sample_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False

                report.update({col:{
                    "p_value": float(is_sample_dist.pvalue),
                    "drift_status": is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(drift_report_file_path, report)
            return status

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> None:
        """
        Initiates the data validation process.
        """
        try:
            logging.info("Starting data validation process")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            ##Read data from train and test files
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)
            logging.info("Data validation process completed successfully")

            # Validate number of columns
            if not self.validate_column_number(train_df):
                error="Train data validation failed: Column number mismatch"

            if not self.validate_column_number(test_df):
                error="Test data validation failed: Column number mismatch"

            # Validate numeric columns
            numeric_columns = self.schema_config.get("numeric_columns", [])
            for col in numeric_columns:
                if col not in train_df.columns:
                    raise NetworkSecurityException(f"Train data validation failed: Missing numeric column '{col}'")
                if not pd.api.types.is_numeric_dtype(train_df[col]):
                    raise NetworkSecurityException(f"Train data validation failed: Column '{col}' is not numeric")

            for col in numeric_columns:
                if col not in test_df.columns:
                    raise NetworkSecurityException(f"Test data validation failed: Missing numeric column '{col}'")
                if not pd.api.types.is_numeric_dtype(test_df[col]):
                    raise NetworkSecurityException(f"Test data validation failed: Column '{col}' is not numeric")
                
            ## Data drift detection
            status = self.detect_data_drift(train_df, test_df)

            if status:
                dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
                os.makedirs(dir_path, exist_ok=True)
                train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
                test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)
            else:
                dir_path = os.path.dirname(self.data_validation_config.invalid_train_file_path)
                os.makedirs(dir_path, exist_ok=True)
                train_df.to_csv(self.data_validation_config.invalid_train_file_path, index=False, header=True)
                test_df.to_csv(self.data_validation_config.invalid_test_file_path, index=False, header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)