from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    ### APP CONFIG
    APP_NAME = os.getenv("APP_NAME")
    APP_HOST = os.getenv("APP_HOST")
    APP_PORT = os.getenv("APP_PORT")
    API_PATH = os.getenv("API_PATH")
    API_VERSION = os.getenv("API_VERSION")
    ### DIR FILES CONFIG
    DIR_PDF_FILES = os.getenv("DIR_PDF_FILES")
    DIR_TMP_FILES = "./tmp"
    ### IRBIS
    IRBIS_HOST = os.getenv("IRBIS_HOST")
    IRBIS_POST = os.getenv("IRBIS_POST")
    IRBIS_DB_USER = os.getenv("IRBIS_DB_USER")
    IRBIS_DB_PASSWORD = os.getenv("IRBIS_DB_PASSWORD")
    IRBIS_DB_NAME = os.getenv("IRBIS_DB_NAME")
    ### DATABASE
    MONGODB_HOST_NAME = os.getenv("MONGODB_HOST_NAME")
    MOGODB_PORT = os.getenv("MOGODB_PORT")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
    MONGODB_USER = os.getenv("MONGODB_USER")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")