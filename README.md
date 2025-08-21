# Image Processing

## Problem Breakdown

### 1. Data Loading & Initial Exploration

- Load both anno_df.csv and pred_df.csv from the data directory.
- Inspect data structure, missing values, and class distributions.
- Summarize key statistics and visualize basic distributions.

### 2. Data Quality & Consistency Checks

- Check for duplicates, inconsistencies, or anomalies in both datasets.
- Validate annotation formats and label consistency.
- Identify potential biases or collection artifacts.

### 3. Exploratory Data Analysis (EDA)

- Visualize class balance, defect types, and annotation density.
- Explore relationships between manual and predicted results.
- Investigate outliers and unexpected patterns.

### 4. Metric Computation

- Define and compute standard metrics: accuracy, precision, recall, F1-score.
- Compare metrics across different confidence thresholds.
- Visualize confusion matrices and ROC/PR curves.

### 5. Threshold Optimization

- Analyze model confidence scores.
- Use ROC/PR analysis to determine optimal thresholds for each dataset.
- Document threshold selection rationale.

### 6. Error & Agreement Analysis

- Identify and analyze false positives/negatives.
- Compare manual and system annotations (e.g., using Cohen’s Kappa).
- Visualize and summarize error patterns.

### 7. Improvement Recommendations

- Summarize findings from analysis.
- Propose concrete steps for improving model performance (data, preprocessing, model, augmentation).
- Justify each recommendation with evidence from your analysis.

### 8. Reporting

- Compile results, figures, and recommendations into markdown reports in the reports directory.
- Ensure all code is modularized in the src directory and notebooks are reproducible.
