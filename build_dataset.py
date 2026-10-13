import pandas as pd

data = pd.read_csv('data/clean/ae_combined.csv', parse_dates=['date'])

file_date = data.dropna(subset=['date']).groupby('source_file')['date'].first()
data['date'] = data['date'].fillna(data['source_file'].map(file_date))

is_total = data['Org Code'].astype(str).str.strip().str.upper() == 'TOTAL'
england = data[is_total].copy()
providers = data[~is_total].copy()

def add_type1(df):
    att = df['A&E attendances Type 1'].fillna(0) + df['A&E attendances Booked Appointments Type 1'].fillna(0)
    over = df['Attendances over 4hrs Type 1'].fillna(0) + df['Attendances over 4hrs Booked Appointments Type 1'].fillna(0)
    df['t1_attendances'] = att
    df['t1_over4'] = over
    df['pct_t1_within_4hrs'] = (1 - over / att.where(att > 0)) * 100
    return df

providers = add_type1(providers)
england = add_type1(england)

trusts = providers[providers['t1_attendances'] > 0].copy()
specialist = trusts['Org name'].str.contains('CHILDREN|WOMEN', case=False, na=False)
print('Excluded specialist trusts:', trusts[specialist]['Org name'].unique())
trusts = trusts[~specialist].copy()

trusts.to_csv("data/clean/ae_trusts_type1.csv", index=False)
england.to_csv("data/clean/ae_england_totals.csv", index=False)

print("Trust-month rows:", len(trusts), "| trusts:", trusts["Org Code"].nunique())
print("\nParent Org values:")
print(trusts["Parent Org"].value_counts().to_string())

print("\nEngland monthly (sanity check):")
cols = ["date", "total_attendances", "pct_within_4hrs", "pct_t1_within_4hrs"]
print(england.sort_values("date")[cols].to_string(index=False))

avg = trusts.groupby(["Org Code", "Org name"])["pct_t1_within_4hrs"].mean().sort_values()
print("\nLowest 5 trusts (avg Type 1 % within 4hrs):")
print(avg.head(5).round(1).to_string())
print("\nHighest 5 trusts:")
print(avg.tail(5).round(1).to_string())