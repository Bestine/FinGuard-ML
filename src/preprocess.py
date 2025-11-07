import pandas as pd 
from datetime import date 
from sklearn.preprocessing import LabelEncoder
from config import Config
from ingest import get_db_connection_engine

def calculate_age(birth_date: date) -> int:
    """Calculates age in years from a given birth date."""
    today_date = date.today()
    age  = int((today_date - birth_date).days / 365)
    return age

def wrangle_data(df: pd.DataFrame, config: Config) -> pd.DataFrame:
    """Wrangle the raw transaction data for analysis."""
    print("[INFO] Starting data wrangling...")

    # Convert date columns to datetime objects
    df["trans_date_trans_time"] = pd.to_datetime(
        df["trans_date_trans_time"], 
        format="%Y-%m-%d %H:%M:%S"
        )
    df["dob"] = pd.to_datetime(df["dob"])

    # Feature Engineering: Time features and Age
    df = df.assign(
        trans_month=df["trans_date_trans_time"].dt.month,
        trans_day=df["trans_date_trans_time"].dt.day,
        trans_hour=df["trans_date_trans_time"].dt.hour,
        age=[calculate_age(d.date()) for d in df["dob"]]
    )

    # Drop original date columns
    df.drop(["trans_date_trans_time", "dob"], axis=1, inplace=True)

    # Drop other irrelevant columns defined in Config
    df.drop(config.DROP_COLS, axis=1, inplace=True)
    
    print("[INFO] Data wrangling complete.")
    return df

def feature_engineer_data(df: pd.DataFrame, config: Config) -> pd.DataFrame:
    """Feature engineer the cleaned transaction data (label encoding)."""
    print("[INFO] Starting feature engineering (label encoding)...")
    
    # Use copy to avoid SettingWithCopyWarning in pandas
    engineered_df = df.copy() 

    # Label encode categorical features
    for col in config.ENCODE_COLS: 
        le = LabelEncoder()
        # fit_transform can fail if categories vary between runs; in production MLOps, 
        # encoders should be saved/loaded. For this script, we fit on the fly.
        engineered_df[col] = le.fit_transform(engineered_df[col].astype(str)) 
        
    print("[INFO] Feature engineering complete.")
    return engineered_df

# If run directly (for testing/debugging preprocessing specifically)
if __name__ == "__main__":
    conf = Config()
    engine = get_db_connection_engine(conf)
    
    # Read raw data from DB
    print(f"[INFO] Fetching raw data from {conf.RAW_TABLE}...")
    df_raw = pd.read_sql_table(
        conf.RAW_TABLE.split('.')[1], 
        schema=conf.RAW_TABLE.split('.')[0], 
        con=engine
        )
    
    # Process
    df_clean = wrangle_data(df_raw, conf)
    df_processed = feature_engineer_data(df_clean, conf)

    # Write to STAGING table first
    print(f"[INFO] Writing processed data to temporary staging table {conf.STAGING_TABLE}...")
    df_processed.to_sql(
        name=conf.STAGING_TABLE.split('.')[1],
        schema=conf.STAGING_TABLE.split('.')[0],
        con=engine,
        if_exists='replace', # Replace the staging table every run
        index=False
    )
    print(f"[INFO] Total rows written to staging: {len(df_processed)}")