import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs('outputs', exist_ok=True)

df = pd.read_csv("data/clean/ae_trusts_type1.csv", parse_dates=["date"])
eng = pd.read_csv("data/clean/ae_england_totals.csv", parse_dates=["date"]).sort_values("date")
df["region"] = df["Parent Org"].str.replace("NHS ENGLAND ", "", regex=False).str.title()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(eng["date"], eng["pct_within_4hrs"], marker="o", label="All A&E types")
ax.plot(eng["date"], eng["pct_t1_within_4hrs"], marker="o", label="Type 1 (major A&E)")
ax.set_title("England: % seen within 4 hours")
ax.set_ylabel("%")
ax.legend()
fig.autofmt_xdate()
fig.savefig("outputs/england_trend.png", dpi=150, bbox_inches="tight")

reg = df.groupby(["region", "date"]).agg(att=("t1_attendances", "sum"), over=("t1_over4", "sum")).reset_index()
reg["pct"] = (1 - reg["over"] / reg["att"]) * 100
pivot = reg.pivot(index="date", columns="region", values="pct")
ax = pivot.plot(figsize=(10, 5), marker="o")
ax.set_title("Type 1 % within 4 hours by NHS England region")
ax.set_ylabel("%")
ax.legend(fontsize=8)
ax.figure.savefig("outputs/regional_trend.png", dpi=150, bbox_inches="tight")

tr = df.groupby("Org name").agg(att=("t1_attendances", "sum"), over=("t1_over4", "sum"), months=("date", "nunique"))
tr = tr[tr["months"] >= 12]
tr["pct"] = (1 - tr["over"] / tr["att"]) * 100
bottom = tr.sort_values("pct").head(10)

short = (bottom.index.str.title()
         .str.replace(" Nhs Foundation Trust", "", regex=False)
         .str.replace(" Nhs Trust", "", regex=False)
         .str.replace("University Hospitals", "UH", regex=False)
         .str.replace("Hospitals", "Hosp.", regex=False))

fig, ax = plt.subplots(figsize=(11, 6))
ax.barh(short, bottom["pct"])
ax.invert_yaxis()
ax.set_title("10 lowest-performing trusts (Type 1 % within 4 hours)")
ax.set_xlabel("%")
ax.tick_params(axis="y", labelsize=8)   # <- the font size for the names
fig.tight_layout()                       # <- stops labels being cut off
fig.savefig("outputs/lowest_trusts.png", dpi=150, bbox_inches="tight")
pivot.round(1).to_csv("outputs/regional_table.csv")
tr.sort_values("pct").round(1).to_csv("outputs/trust_ranking.csv")

print(pivot.round(1).to_string())
print()
print(bottom[["pct", "months"]].round(1).to_string())
print("\nRegion averages over the period:")
r = df.groupby("region").agg(att=("t1_attendances", "sum"), over=("t1_over4", "sum"))
print(((1 - r["over"] / r["att"]) * 100).round(1).sort_values().to_string())
plt.show()