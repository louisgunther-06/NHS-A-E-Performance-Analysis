import pandas as pd

df = pd.read_csv('data/raw/April-2025-CSV-revised.csv')
print(df.shape)
print(df.columns.tolist())
print(df.head(10))
