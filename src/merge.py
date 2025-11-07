# merge.py
from config import Config
from ingest import connect_to_db

def merge_staging_to_warehouse(config: Config):
    """
    Merges data from the staging table into the main warehouse table using
    PostgreSQL's MERGE or INSERT ON CONFLICT commands.
    """
    print(f"[INFO] Starting merge from {config.STAGING_TABLE} to {config.PROCESSED_TABLE}...")
    
    conn = connect_to_db(config)
    cursor = conn.cursor()

    try:
        # Define the SQL UPSERT/MERGE statement
        # This assumes your processed table has a unique identifier (transaction_id or maybe trans_num from raw if you keep it)
        # We need a business key to check for conflicts. Let's assume you kept `trans_num` in your final processed table schema 
        # as a unique identifier for this merge to work reliably. 
        # *Note: Your current processed table schema doesn't have `trans_num` anymore.* 
        
        # If we assume *all* data in staging is NEW data that hasn't been processed before:
        # A simple INSERT INTO SELECT is enough.
        
        # If we assume we might re-process the *same* data files and only want unique records added:
        # We need a conflict target. Let's update the strategy to use a unique constraint on the data itself, 
        # for example, a composite key if necessary, or just rely on a simple INSERT of *new* raw data batches.

        # Assuming the pipeline runs on new raw data batches each time, we just INSERT new unique data:

        merge_query = f"""
        INSERT INTO {config.PROCESSED_TABLE} (
            category, amt, gender, street, city, state, zip, lat, long, city_pop, 
            job, merch_lat, merch_long, trans_month, trans_day, trans_hour, age, is_fraud
        )
        SELECT 
            category, amt, gender, street, city, state, zip, lat, long, city_pop, 
            job, merch_lat, merch_long, trans_month, trans_day, trans_hour, age, is_fraud
        FROM {config.STAGING_TABLE} AS st
        WHERE NOT EXISTS (
            SELECT 1 
            FROM {config.PROCESSED_TABLE} AS pt
            WHERE -- Need a unique business key match here to avoid true duplicates
                -- Since we dropped trans_num, this gets tricky.
                -- We assume every run processes a fresh batch of raw data.
                1=0 -- This WHERE clause ensures we always insert everything from staging.
        );
        """
        
        # A more robust approach requires a unique business key (like trans_num) in the PROCESSED table.
        # Let's adjust based on the assumption you only ever ADD new transactions.

        merge_query_simple_insert = f"""
        INSERT INTO {config.PROCESSED_TABLE} (
            category, amt, gender, street, city, state, zip, lat, long, city_pop, 
            job, merch_lat, merch_long, trans_month, trans_day, trans_hour, age, is_fraud
        )
        SELECT * FROM {config.STAGING_TABLE};
        """

        cursor.execute(merge_query_simple_insert)
        conn.commit()
        print(f"[INFO] Merge completed. {cursor.rowcount} rows inserted into main warehouse table.")

    except Exception as e:
        print(f"[ERROR] Merge failed: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    conf = Config()
    merge_staging_to_warehouse(conf)
