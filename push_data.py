import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_DB_URI")

import certifi
ca=certifi.where()

import pandas as pd
import pymongo
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json(self, csv_file_path: str) -> str:
        """
        Convert a CSV file to a JSON file.
        
        :param csv_file_path: Path to the input CSV file.
        :return: Path to the output JSON file.
        """
        try:
            df = pd.read_csv(csv_file_path)
            df.reset_index(drop=True, inplace=True)
            records=json.loads(df.T.to_json()).values()
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_to_mongodb(self, data: list, db_name: str, collection_name: str) -> None:
        """
        Insert data into MongoDB.
        
        :param data: List of records to be inserted.
        :param db_name: Name of the database.
        :param collection_name: Name of the collection.
        """
        try:
            self.db_name=db_name
            self.collection_name=collection_name
            self.data=data
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI, tlsCAFile=ca)
            self.db_name = self.mongo_client[self.db_name]
            self.collection_name = self.db_name[self.collection_name]

            self.collection_name.insert_many(self.data)
            logging.info(f"Data inserted successfully into {self.db_name.name}.{self.collection_name.name}")
            return (len(self.data))
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    

    network_data_extractor = NetworkDataExtract()
    csv_file_path = "Network_Data\phisingData.csv"  # Replace with your CSV file path
    json_data = network_data_extractor.csv_to_json(csv_file_path)
     
    db_name = "network_security_db"  # Replace with your database name
    collection_name = "phishing_data"  # Replace with your collection name
        
    inserted_count = network_data_extractor.insert_data_to_mongodb(json_data, db_name, collection_name)
    print(f"Inserted {inserted_count} records into MongoDB.")
    