import os 
from dotenv import load_dotenv

# Load all the environment variables from the .env file
load_dotenv()

class Config:
    """Centralized configuration manager"""

    # Database configuration
    DB_NAME = os.getenv("DB_NAME")  # The database you created
    DB_USER = os.getenv("DB_USER")            # Your postgres username
    DB_PASSWORD = os.getenv("DB_PASSWORD")   # The password you set in Step 4
    DB_HOST = os.getenv("DB_HOST", "localhost")            # The host of your database
    DB_PORT = os.getenv("DB_PORT", "5432")            # The port of your database

    # Paths and table names
    CSV_FILE_PATH = "data/raw/fraudTrain.csv"
    RAW_TABLE = "raw.transactions_raw"
    PROCESSED_TABLE = "warehouse.transactions_processed"
    STAGING_TABLE = "warehouse.transactions_staging"

    # Columns definition for validation and processing
    RAW_COLS = [
        'trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'first',
        'last', 'gender', 'street', 'city', 'state', 'zip', 'lat', 'long',
        'city_pop', 'job', 'dob', 'trans_num', 'unix_time', 'merch_lat',
        'merch_long', 'is_fraud'
    ]

    # Columns to be dropped during preprocessing
    DROP_COLS = ["cc_num", "first", "last", "trans_num", "unix_time", "merchant"]

    # Columns to be label encoded during feature engineering
    ENCODE_COLS = ["category", "street", "city", "state", "job", "gender"]