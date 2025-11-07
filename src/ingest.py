# ingestion.py
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os
from config import Config

# --- Database Connection Functions ---

def get_db_connection_engine(config: Config):
    """Create an SQLAlchemy engine for pandas to use."""
    db_url = f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    engine = create_engine(db_url)
    return engine

def connect_to_db(config: Config):
    """Establish a direct psycopg2 connection."""
    conn = psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT
    )
    return conn

# --- Data Ingestion Logic ---

def ingest_raw_data(config: Config, engine):
    """Reads CSV, validates columns, and ingests into the specified DB table."""
    csv_path = config.CSV_FILE_PATH
    table_name = config.RAW_TABLE
    expected_columns = config.RAW_COLS

    if not os.path.exists(csv_path):
        print(f"[ERROR] CSV file not found at {csv_path}")
        return

    print(f"[INFO] Reading data from {csv_path}...")
    try:
        df = pd.read_csv(csv_path, index_col=0)
        print(f"[INFO] Successfully read {len(df)} rows.")
    except Exception as e:
        print(f"[ERROR] Error reading CSV file: {e}")
        return

    # Validation: Ensure column names match the expected schema
    if not all(col in df.columns for col in expected_columns):
        missing_cols = set(expected_columns) - set(df.columns)
        print(f"[ERROR] Missing expected columns in CSV: {missing_cols}")
        return

    # Basic type casting before loading into raw VARCHAR columns
    df['trans_num'] = df['trans_num'].astype(str)
    df['cc_num'] = df['cc_num'].astype(str)

    print(f"[INFO] Writing data to PostgreSQL table '{table_name}'...")
    try:
        df.to_sql(
            name=table_name.split('.')[1], 
            schema=table_name.split('.')[0], 
            con=engine,
            if_exists='replace', # Use 'replace' for an ETL run to clear previous raw data
            index=False,
            chunksize=1000
        )
        print("[INFO] Data ingestion complete.")
    except Exception as e:
        print(f"[ERROR] Error writing data to database: {e}")

# If run directly (for testing/debugging ingestion specifically)
if __name__ == "__main__":
    conf = Config()
    db_engine = get_db_connection_engine(conf)
    ingest_raw_data(conf, db_engine)
