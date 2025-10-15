# load SaludMental.csv
import pandas as pd

df = pd.read_csv('SaludMental.csv')


# Drop columns with in which all values are NaN
df = df.dropna(axis=1, how='all')

print("##########Head:\n", df.head())
print("##########Info:\n", df.info())
print("##########Describe:\n", df.describe())
print("##########Columns:\n", df.columns)
print("##########Shape:\n", df.shape)

# Save cleaned data to a new CSV file
df.to_csv('SaludMental_cleaned.csv', index=False)