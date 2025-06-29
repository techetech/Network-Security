import os,sys
import certifi
ca=certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
if not mongo_db_url:
    raise Exception("MONGO_DB_URL environment variable is not set.")
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME,DATA_INGESTION_DATABASE_NAME
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")
@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training pipeline executed successfully.", status_code=200)
    except Exception as e:
        logging.error(f"Error in training pipeline: {str(e)}")
        return Response(f"Training pipeline failed: {str(e)}", status_code=500)
    
@app.post("/predict",tags=["prediction"])
async def predict_route(request: Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)

        preprocessor= load_object(file_path="final_model/preprocessor.pkl")
        final_model=load_object(file_path="final_model/model.pkl")

        network_model = NetworkModel(
            model=final_model,
            preprocessor=preprocessor,
        )
        y_pred = network_model.predict(df)
        print(y_pred)
        df['prediction'] = y_pred
        print(df['prediction'])
        df.to_csv("prediction_output/predicted_data.csv", index=False)
        table_html= df.to_html(classes='table table-striped', index=False)

        return templates.TemplateResponse("table.html", {
            "request": request,
            "table": table_html
        })
    
    except Exception as e:
        logging.error(f"Error in prediction route: {str(e)}")
        return Response(f"Prediction failed: {str(e)}", status_code=500)


if __name__ == "__main__":
    try:
        app_run(app, host="0.0.0.0", port=8000) 
    except Exception as e:
        logging.error(f"Failed to start application: {str(e)}")
        print(f"Failed to start application: {str(e)}")
