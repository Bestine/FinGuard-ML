import numpy as np
import pandas as pd 
from matplotlib import pyplot as plt
import seaborn as sns 
from data_loading import load_data
import warnings 

warnings.filterwarnings("ignore")

# These function will extract x and y coordinates from the 'xy' column and pair them in lists of tuples
def extract_xy_coords(xy_str):
    """Parse the xy string into separate x and y lists."""
    coords = [float(val) for val in xy_str.split(',')]
    x_coords = coords[::2]
    y_coords = coords[1::2]
    return x_coords, y_coords

def get_all_coords(df):
    """Aggregate all x and y coordinates from the dataframe."""
    all_x, all_y = [], []
    for xy_str in df['xy']:
        x, y = extract_xy_coords(xy_str)
        all_x.extend(x)
        all_y.extend(y)
    return np.array(all_x), np.array(all_y)

def main():
    # Load the required data
    anno_df = load_data('data/clean-data/anno_df_clean.csv')
    pred_df = load_data('data/clean-data/pred_df_clean.csv')

    # Visualizations 
    ## Distribution of confidence in the generated images 
    plt.figure(figsize=(8,4))
    sns.distplot(pred_df["confidence"])
    plt.title('Distribution of confidence in generated images')
    plt.savefig('visualizations/confidence_distribution.png')
    # plt.xticks(rotation=45)
    plt.show()

    ## Visualiz defect location 
    ### For anno_df
    anno_x, anno_y = get_all_coords(anno_df)

    plt.figure(figsize=(8, 6))
    sns.kdeplot(x=anno_x, y=anno_y, cmap="Reds", fill=True, thresh=0.05)
    plt.title("Defect Location Heatmap (anno_df)")
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.gca().invert_yaxis()  # Optional: match image coordinate system
    plt.savefig('visualizations/defect_location_heatmap_anno_df.png')
    plt.show()

    ### For pred_df
    pred_x, pred_y = get_all_coords(pred_df)
    plt.figure(figsize=(8, 6))
    sns.kdeplot(x=pred_x, y=pred_y, cmap="Blues", fill=True, thresh=0.05)
    plt.title("Defect Location Heatmap (pred_df)")
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.gca().invert_yaxis()
    plt.savefig('visualizations/defect_location_heatmap_pred_df.png')
    plt.show()

    ## Count and compare defects count 
    ### Count defects per image for both datasets
    anno_counts = anno_df['image_id'].value_counts().sort_index()
    pred_counts = pred_df['image_id'].value_counts().sort_index()

    ## Combine into a DataFrame for grouped bar chart
    counts_df = pd.DataFrame({
        'Manual (anno_df)': anno_counts,
        'Predicted (pred_df)': pred_counts
    }).fillna(0).astype(int)

    ### Plot grouped bar chart
    counts_df.plot(kind='bar', figsize=(14, 6))
    plt.title('Per-Image Defect Count: Manual vs Predicted')
    plt.xlabel('Image Id')
    plt.ylabel('Number of Defects')
    plt.legend()
    plt.tight_layout()
    plt.savefig('visualizations/defect_count_comparison.png')
    plt.show()

if __name__ == "__main__":
    main()
