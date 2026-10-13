import pandas as pd 

df = pd.read_csv("data/clean/ae_trusts_type1.csv", parse_dates=["date"])
print("Trusts:", df["Org Code"].nunique())

g = df.groupby(["Org name", "Parent Org"]).agg(
    att=("t1_attendances", "sum"), over=("t1_over4", "sum"),
    best_month=("pct_t1_within_4hrs", "max")).reset_index()
g["pct"] = (1 - g["over"] / g["att"]) * 100
print(g.sort_values("pct").head(10)[["Org name", "Parent Org", "pct", "best_month"]].round(1).to_string(index=False))

print(df[df["Org name"].str.contains("CALDERDALE")][["date", "t1_attendances", "pct_t1_within_4hrs"]].to_string(index=False))