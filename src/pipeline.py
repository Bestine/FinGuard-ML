# pipeline.py (final updated version)
from config import Config
from ingest import get_db_connection_engine, ingest_raw_data, connect_to_db
from preprocess import wrangle_data, feature_engineer_data
from merge import merge_staging_to_warehouse # Import the new function
import pandas as pd

def run_etl_pipeline():
    """
    Orchestrates the complete Extract, Transform, Load (ETL) pipeline.
    """
    print("--- Starting ETL Pipeline ---")
    conf = Config()
    engine = get_db_connection_engine(conf)
    
    # Step 1: Extract and Load Raw Data (EL)
    print("\n[STEP 1] Ingesting raw CSV data into PostgreSQL raw schema...")
    ingest_raw_data(conf, engine)
    
    # Step 2: Extract Raw Data from DB for Transformation (E)
    print(f"\n[STEP 2] Fetching raw data from {conf.RAW_TABLE} for processing...")
    try:
        df_raw = pd.read_sql_table(
            con=engine,
            table_name=conf.RAW_TABLE.split('.')[1],
            schema=conf.RAW_TABLE.split('.')[0],
        )
        print(f"[INFO] Retrieved {len(df_raw)} rows from raw schema.")
    except Exception as e:
        print(f"[CRITICAL ERROR] Failed to fetch raw data from DB: {e}")
        return

    # Step 3: Transform Data (T) -> Result goes to a DataFrame
    print("[STEP 3] Wrangling and Feature Engineering data...")
    df_clean = wrangle_data(df_raw, conf)
    df_processed = feature_engineer_data(df_clean, conf)
    
    # Step 4: Load Transformed Data to Staging (L to Staging)
    print(f"\n[STEP 4] Loading processed data into temporary staging table {conf.STAGING_TABLE}...")
    try:
        df_processed.to_sql(
            name=conf.STAGING_TABLE.split('.')[1],
            schema=conf.STAGING_TABLE.split('.')[0],
            con=engine,
            if_exists='replace', # Replace the staging table every run
            index=False
        )
        print(f"[INFO] Successfully loaded {len(df_processed)} rows to staging.")
    except Exception as e:
        print(f"[ERROR] Error loading processed data to staging: {e}")
        return

    # Step 5: Merge Staging Data into Main Warehouse (Merge)
    print(f"\n[STEP 5] Merging staging data into main table {conf.PROCESSED_TABLE}...")
    merge_staging_to_warehouse(conf)

    # Verification
    try:
        conn = connect_to_db(conf)
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {conf.PROCESSED_TABLE};")
        count = cursor.fetchone()
        print(f"\nVerification: Total rows in {conf.PROCESSED_TABLE}: {count}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Verification failed: {e}")
        
    print("\n--- ETL Pipeline Complete ---")

if __name__ == "__main__":
    run_etl_pipeline()
