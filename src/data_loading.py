# Load the required libraries  
import pandas as pd

# Load the data sets  - I am using VS code and running in therefore data filepath has to change
anno_df = pd.read_csv('data/anno_df.csv', 
                      usecols=["filename","image_id","id","defect_class_id","label","xy","x","y"])
pred_df = pd.read_csv('data/pred_df.csv', 
                     usecols=["image_id","prediction_id","confidence","polygon_id","prediction_class","xy"])

def load_data(filepath): 
    df = pd.read_csv(filepath)
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Drop unary columns 
    df = df.loc[:, df.nunique() > 1]
    # Remove duplicates
    df = df.drop_duplicates()
    # Handle missing values
    df = df.dropna()
    return df

def write_data(df: pd.DataFrame, filepath: str):
    df.to_csv(filepath, index=False)

def main():
    # Load the data
    anno_df = load_data('data/anno_df.csv')
    pred_df = load_data('data/pred_df.csv')

    # Clean the data
    anno_df = clean_data(anno_df)
    pred_df = clean_data(pred_df)

    # Write the cleaned data
    write_data(anno_df, 'data/clean-data/anno_df_clean.csv')
    write_data(pred_df, 'data/clean-data/pred_df_clean.csv')

if __name__ == "__main__":
    main()