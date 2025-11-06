import pandas as pd
import psycopg2
from psycopg2 import extras
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load all the environment variables from the .env file
load_dotenv()


# --- Configuration ---
DB_NAME = os.getenv("DB_NAME")  # The database you created
DB_USER = os.getenv("DB_USER")            # Your postgres username
DB_PASSWORD = os.getenv("DB_PASSWORD")   # The password you set in Step 4
DB_HOST = os.getenv("DB_HOST")            # The host of your database
DB_PORT = os.getenv("DB_PORT")
            # The port of your database
CSV_FILE_PATH = "data/raw/fraudTrain.csv"
TARGET_TABLE = "raw.transactions_raw"

# --- Database Connection Functions ---

def get_db_connection_engine():
    """Create an SQLAlchemy engine for pandas to use."""
    # Format the database URL for SQLAlchemy
    db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(db_url)
    return engine

def connect_to_db():
    """Establish a direct psycopg2 connection."""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# --- Data Ingestion Logic ---

def ingest_raw_data(csv_path, table_name, engine):
    """Reads CSV, validates columns, and ingests into the specified DB table."""
    
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    print(f"Reading data from {csv_path}...")
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_path, index_col=0)
        print(f"Successfully read {len(df)} rows.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Basic Validation: Ensure column names match the expected schema
    expected_columns = [
        'trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'first',
        'last', 'gender', 'street', 'city', 'state', 'zip', 'lat', 'long',
        'city_pop', 'job', 'dob', 'trans_num', 'unix_time', 'merch_lat',
        'merch_long', 'is_fraud'
    ]
    
    if not all(col in df.columns for col in expected_columns):
        missing_cols = set(expected_columns) - set(df.columns)
        print(f"Error: Missing expected columns in CSV: {missing_cols}")
        return

    # Optional: Perform basic data type casting/cleaning if necessary before load
    # For raw schema, we keep everything close to original format as defined in 02_create_tables.sql
    df['trans_num'] = df['trans_num'].astype(str)
    df['cc_num'] = df['cc_num'].astype(str)

    print(f"Writing data to PostgreSQL table '{table_name}'...")
    try:
        # Use pandas to_sql method to write DataFrame to the database
        # if_exists='append' adds to the table. Use 'replace' if you want to clear it first.
        df.to_sql(
            name=table_name.split('.')[1], # table name (transactions_raw)
            schema=table_name.split('.')[0], # schema name (raw)
            con=engine,
            if_exists='append',
            index=False,
            chunksize=1000
        )
        print("Data ingestion complete.")
    except Exception as e:
        print(f"Error writing data to database: {e}")


# --- Main execution ---

if __name__ == "__main__":
    # 1. Get the DB engine
    db_engine = get_db_connection_engine()
    
    # 2. Ingest the data
    ingest_raw_data(CSV_FILE_PATH, TARGET_TABLE, db_engine)
    
    # 3. Verify the count (optional)
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {TARGET_TABLE};")
        count = cursor.fetchone()[0]
        print(f"\nVerification: Total rows in {TARGET_TABLE}: {count}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Verification failed: {e}")