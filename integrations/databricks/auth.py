import os

import mlflow
from dotenv import load_dotenv


def setup_mlflow():
    load_dotenv()
    host = os.getenv('DATABRICKS_HOST')
    mlflow.set_tracking_uri(host)
