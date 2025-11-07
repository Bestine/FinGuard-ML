import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from datetime import date 

from sklearn.preprocessing import LabelEncoder

def calculate_age(birth_date):
    """
    This function calculates date from the difference between;
        - today date 
        - date of birth

    And truncates to return the age in years
    """
    today_date = date.today()
    age  = int((today_date - birth_date).days / 365)
    return age

def wrangle_data(df):
    """Wrangle the raw transaction data for analysis."""
    
    # Convert transaction date to datetime
    df["trans_date_trans_time"] = pd.to_datetime(
        df["trans_date_trans_time"], 
        errors="raise", 
        format="%Y-%m-%d %H:%M:%S"
    )

    # Extract month, day and hour of transaction
    df["trans_month"] = df["trans_date_trans_time"].dt.month
    df["trans_day"] = df["trans_date_trans_time"].dt.day
    df["trans_hour"] = df["trans_date_trans_time"].dt.hour

    # Drop the transaction time  after extracting useful features
    df.drop(["trans_date_trans_time"], axis=1, inplace=True)

    # Apply the `calculate_age` function to the data set
    ## Convert the column to datetime object 
    df["dob"] = pd.to_datetime(df["dob"], errors="raise")

    # Calculate age from date of birth
    df["age"] = [calculate_age(dob.date()) for dob in df["dob"]]
    # Drop the dob column after extracting age
    df.drop(["dob"], axis=1, inplace=True)

    # Drop other irrelevant columns 
    df.drop(
        ["cc_num", "first", "last", "trans_num", "unix_time", "merchant"],
        axis=1, 
        inplace = True
    )

    cleaned_df = df.copy()
    return cleaned_df

def feature_engineer_data(cleaned_df):
    """Feature engineer the cleaned transaction data for analysis."""
    
    df = cleaned_df.copy()

    # Label encode categorical features
    label_encode_columns = ["category", "street", "city", "state", "job", "gender"]

    for col in label_encode_columns: 
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

    engineered_df = df.copy()
    return engineered_df

    

