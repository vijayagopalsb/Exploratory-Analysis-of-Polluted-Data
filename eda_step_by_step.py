# File: eda_step_by_step.py

# Generate Pollutted Dataset

# 1. Import necessary libraries
# -----------------------------

import pandas as pd
import numpy as np
from logging_config import logger

# Set random seed for reproducibility

np.random.seed(42)

# Create a polluted dataset
# -------------------------
data = {
    "ID": [1, 2, 2, 3, 4, 5, 6], # Duplicate ID
    "Age": [25, -5, 32, np.nan, 150, 28, "thirty"], # Negative, Outlier, NaN, String
    "Salary": [50000, 60000, np.nan, 75000, 9999999, 45000, 52000], # Outlier, NaN
    "Department": ["HR", "IT", "it", "Sales", "HR", np.nan, "Marketing"], # Inconsistent case, NaN
    "Join_Date": ["2020-01-15", "15/01/2021", "2022-13-01", np.nan, "2021-05-10", "2020-12-01", "2023-02-30"]  # Invalid dates
}

df = pd.DataFrame(data)


# Save to CSV Format
df.to_csv("polluted_dataset.csv", index=False)

logger.info("Polluted Dataset ...")
logger.info(df)

# 2. Load the dataset
# -------------------

df = pd.read_csv("polluted_dataset.csv")  # Or use the DataFrame directly from above

# 3. Check the first few rows of the data
# ---------------------------------------

logger.info("Display few dataset ...")

logger.info(df.head())

# 4. Get basic information about the dataset
# ------------------------------------------

logger.info("Dataset information ...")
logger.info(df.info())

# 5. Check for missing values
# ---------------------------

logger.info("Check for missing values ...")
logger.info(df.isnull().sum())

# 6. Handle missing values
# ------------------------
logger.info("Handling missing values ...")

# Drop columns with excessive NaN
# Impute Age (convert to numeric first)
# Impute Salary with median
df["Salary"] = df["Salary"].fillna(df["Salary"].median())

# Impute Department with 'Unknown'
df["Department"] = df["Department"].fillna("Unknown")

# Impute Join_Date with a placeholder
df['Join_Date'] = df['Join_Date'].fillna('Unknown')


# 7. Check data types and convert if necessary
# --------------------------------------------

# Convert Age to numeric, coerce errors
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
# Impute NaN in Age (from 'thirty') with median
df['Age'] = df['Age'].fillna(df['Age'].median())
# Convert Join_Date to datetime later after fixing formats

logger.info(df)

# 8. Explore summary statistics
# -----------------------------
logger.info("8. Explore summary statistics ...")
logger.info(df.describe())

# 9. Identify and handle duplicates
# ---------------------------------

logger.info("9. Identify and handle duplicates ...")
logger.info(f"Check full row duplicates: {df.duplicated().sum()}")  # Check full row duplicates
df = df.drop_duplicates(keep='first')
# Drop duplicate ID
df = df.drop_duplicates(subset=['ID'], keep='first')
logger.info(df)

# 10. Detect outliers
# -------------------

# IQR for Age
Q1_age = df['Age'].quantile(0.25)
Q3_age = df['Age'].quantile(0.75)
IQR_age = Q3_age - Q1_age
outliers_age = (df['Age'] < Q1_age - 1.5 * IQR_age) | (df['Age'] > Q3_age + 1.5 * IQR_age)
print(df[outliers_age])  # Shows -5 and 150

# IQR for Salary (similarly)




