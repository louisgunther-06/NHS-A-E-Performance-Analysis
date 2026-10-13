import pandas as pd 

data = pd.read_csv('data/clean/ae_combined.csv')

bad = data[data['date'].isna()]
print (bad[['Period', 'Org Code', 'Org name', 'source_file', 'total_attendances']].to_string())

print('\nZero-attendance rows:', (data['total_attendances'] ==0).sum())

t1 = data[data['A&E attendances Type 1'] > 0]
print('Rows with Type 1 attendances:', len(t1))
print('Distinct providers with Type 1:', t1['Org Code'].nunique())
print(t1[['Org Code', 'Org name']].drop_duplicates().head(10).to_string())