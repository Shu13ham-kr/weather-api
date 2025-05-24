import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ENV = os.environ.get("FLASK_ENV", "PROD")
    DEBUG = (ENV == "DEV")
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GCP_CRED")
    BUCKET_NAME = os.environ.get("GCS_NAME")