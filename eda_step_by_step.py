# File: eda_step_by_step.py

# Generate Pollutted Dataset

# 1. Import necessary libraries
# -----------------------------

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')  # type: ignore # Or 'Qt5Agg', 'GTK3Agg', etc., depending on your system
import matplotlib.pyplot as plt


from sklearn.preprocessing import StandardScaler 
from logging_config import logger
from  utils import df_info_to_string

# Set random seed for reproducibility

np.random.seed(42)

# 1. Create a polluted dataset

data = {
    "ID": [1, 2, 2, 3, 4, 5, 6], # Duplicate ID
    "Age": [25, -5, 32, np.nan, 150, 28, "thirty"], # Negative, Outlier, NaN, String
    "Salary": [50000, 60000, np.nan, 75000, 9999999, 45000, 52000], # Outlier, NaN
    "Department": ["HR", "IT", "it", "Sales", "HR", np.nan, "Marketing"], # Inconsistent case, NaN
    "Join_Date": ["2020-01-15", "15/01/2021", "2022-13-01", np.nan, "2021-05-10", "2020-12-01", "2023-02-30"]  # Invalid dates
}
logger.info("1. Create a polluted dataset")
# 2. Load the data into dataframe

df = pd.DataFrame(data)

## Optional: Save to CSV Format for future observation
df.to_csv("polluted_dataset.csv", index=False)

logger.info("2. Polluted Dataset as whole::")
logger.info(df)

df = pd.read_csv("polluted_dataset.csv")  # Or use the DataFrame directly from above

# 3. Check the first few rows of the data


logger.info("3. Display few dataset::")

logger.info(df.head())

# 4. Get basic information about the dataset

logger.info("4. Dataset information::")

logger.info(df_info_to_string(df))

logger.info("**Note** Shows Age as object (due to 'thirty'), Salary/Department/Join_Date with NaN")

# 5. Check for missing values


logger.info("5. Check for missing values::")

logger.info(df.isnull().sum())

# # 6. Handle missing values

logger.info("6. Handling missing values::")

# Drop columns with excessive NaN
# Impute Age (convert to numeric first , will do on Step 7)
# Impute Salary with median
df["Salary"] = df["Salary"].fillna(df["Salary"].median())


# Impute Department with 'Unknown'
df["Department"] = df["Department"].fillna("Unknown")

# Impute Join_Date with a placeholder
df['Join_Date'] = df['Join_Date'].fillna('Unknown')
logger.info(df)
# 7. Check data types and convert if necessary
logger.info("7. Check data types and convert if necessary::")
# Convert Age to numeric, coerce errors
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

# Impute NaN in Age (from 'thirty') with median
df['Age'] = df['Age'].fillna(df['Age'].median())

# After handle missing values
logger.info("After Handling missing values::")

logger.info(df)

# 8. Explore summary statistics

logger.info("8. Explore summary statistics::")
logger.info(df.describe())

# 9. Identify and handle duplicates


logger.info("9. Identify and handle duplicates::")
logger.info(f"Check full row duplicates: {df.duplicated().sum()}")  # Check full row duplicates

df = df.drop_duplicates(keep='first')

# Drop duplicate ID
df = df.drop_duplicates(subset=['ID'], keep='first')
logger.info(df)

# 10. Detect outliers
logger.info("IQR for Age::")
# IQR for Age
# Calculate Q1, Q3, and IQR
Q1_age = df['Age'].quantile(0.25)
Q3_age = df['Age'].quantile(0.75)
IQR_age = Q3_age - Q1_age

# Define outlier bounds
lower_bound_age = Q1_age - 1.5 * IQR_age
upper_bound_age = Q3_age + 1.5 * IQR_age

# Log results
logger.info(f"Age - Q1 (25th percentile): {Q1_age}")
logger.info(f"Age - Q3 (75th percentile): {Q3_age}")

logger.info(f"Age - IQR: {IQR_age}")
logger.info(f"Age - Lower Bound: {lower_bound_age}")
logger.info(f"Age - Upper Bound: {upper_bound_age}")

# # Identify outliers
outliers_age = (df['Age'] < lower_bound_age) | (df['Age'] > upper_bound_age)
logger.info("Outliers in Age::")
logger.info(outliers_age.to_string())

# Handle outliers (e.g., cap Age)
df.loc[df['Age'] > upper_bound_age, 'Age'] = upper_bound_age
df.loc[df['Age'] < lower_bound_age, 'Age'] = lower_bound_age

# # IQR for Salary

# # Calculate Q1, Q3, and IQR
Q1_salary = df['Salary'].quantile(0.25)
Q3_salary = df['Salary'].quantile(0.75)

IQR_salary = Q3_salary - Q1_salary

# Define outlier bounds
lower_bound_salary = Q1_salary - 1.5 * IQR_salary
upper_bound_salary = Q3_salary + 1.5 * IQR_salary

# Log results
logger.info(f"Salary - Q1 (25th percentile): {Q1_salary}")
logger.info(f"Salary - Q3 (75th percentile): {Q3_salary}")

logger.info(f"Salary - IQR: {IQR_salary}")
logger.info(f"Salary - Lower Bound: {lower_bound_salary}")
logger.info(f"Salary - Upper Bound: {upper_bound_salary}")

# Identify outliers
outliers_salary = df[(df['Salary'] < lower_bound_salary) | (df['Salary'] > upper_bound_salary)]
logger.info("Outliers in Salary:")
logger.info(outliers_salary.to_string())

# Handle outliers (e.g., cap Salary)
df.loc[df['Salary'] > upper_bound_salary, 'Salary'] = upper_bound_salary
df.loc[df['Salary'] < lower_bound_salary, 'Salary'] = lower_bound_salary


# Log updated DataFrame
logger.info("DataFrame after handling outliers:")
logger.info(df.to_string())

# 11. Handle outliers
logger.info("11. Handle outliers::")
# Cap Age outliers
df.loc[df['Age'] < 0, 'Age'] = 0  # Replace negative with 0
df.loc[df['Age'] > 100, 'Age'] = 100  # Cap at 100
# Cap Salary at  1000000
df.loc[df['Salary'] > 1000000, 'Salary'] = 1000000

# Log updated DataFrame
logger.info("DataFrame after handling outliers:")
logger.info(df.to_string())

# 12. Visualize data distributions

logger.info("12. Data Visualization::")

df['Age'].hist()
plt.title("Age Distribution Histogram")
plt.savefig('age_histogram.png')  # Saves to current directory
logger.info("Age Distribution Hsitogram saved")
##plt.show(block=True) # Some WSL terminal the graph will nit display

sns.boxplot(x=df['Salary'])
plt.title("Salary Box Plot")
logger.info("Salary Box Plot saved")
plt.savefig('salary_box_plot.png')  # Saves to current directory
#plt.show()

# 13. Explore relationships between variables
logger.info("13. Explore relationships between variables::")

numeric_df = df.select_dtypes(include=[np.number])
logger.info(numeric_df.corr())
sns.heatmap(numeric_df.corr(), annot=True)
plt.title("Heat Map of Numeric data types")
plt.savefig("heat_map.png")
logger.info("Heat Map graph saved")

# 14. Perform feature encoding
logger.info("14. Perform feature encoding::")

# Standardize Department case and one-hot encode


df['Department'] = df['Department'].str.lower()
df = pd.get_dummies(df, columns=['Department'], prefix='Dept', dtype=int)
logger.info(df)

# 15. Scale or normalize data if required
logger.info("15. Scale or normalize data if required::")

scaler = StandardScaler()
df[['Age', 'Salary']] = scaler.fit_transform(df[['Age', 'Salary']])

logger.info(df)

# 16. Save the cleaned dataset
logger.info("16. Save the cleaned dataset::")

df.to_csv('cleaned_polluted_data.csv', index=False)
logger.info("Cleaned Dataset:")
logger.info(df)
logger.info("--Note-- The dataset is now clearned: No duplicates, no missing values, outliers capped, consistent types and scaled features.")




