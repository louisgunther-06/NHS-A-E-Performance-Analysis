import glob
import pandas as pd
import os 

files = sorted(glob.glob('data/raw/*.csv'))
print(f'Found {len(files)} files')

frames = []
base_cols = None

for f in files:
    df = pd.read_csv(f)
    df.columns = df.columns.str.strip()

    if base_cols is None:
        base_cols = list(df.columns)
    elif list(df.columns) != base_cols:
        print(f'WARNING: Columns differ in {f}')
        print(' extra:'. set(df.columns) - set(base_cols))
        print(' missing:', set(base_cols) - set(df.columns))

    df['source_file'] = f.split('/')[-1]
    frames.append(df)

data = pd.concat(frames, ignore_index=True)

period = data['Period'].str.replace('MSitAE-', '', regex=False)
data['date'] = pd.to_datetime(period, format='%B-%Y', errors='coerce')
print('Rows with unparsed dates:', data['date'].isna().sum())

num_cols = [c for c in data.columns if c not in
            ['Period', 'Org Code', 'Parent Org', 'Org name', 'source_file', 'date']]
for c in num_cols:
    data[c] = pd.to_numeric(data[c], errors='coerce')

att_cols = [c for c in num_cols if c.startswith('A&E attendances')]
over_cols = [c for c in num_cols if c.startswith('Attendances over 4hrs')]

data['total_attendances'] = data[att_cols].sum(axis=1)
data['total_over_4hrs'] = data[over_cols].sum(axis=1)
data['pct_within_4hrs'] = (1 - data['total_over_4hrs'] / data['total_attendances']) * 100

print(data[['date', 'Org Code', 'Org name', 'total_attendances', 'pct_within_4hrs']].head(8))
print(data['date'].value_counts().sort_index())

os.makedirs('data/clean', exist_ok=True)

data.to_csv('data/clean/ae_combined.csv', index=False)
print('Saved data/clean/ae_combined.csv', data.shape)