import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

df = pd.read_excel(r"C:\Users\Hari\Downloads\Python CA\excel crop data.xlsx")

df.columns = df.columns.str.strip().str.lower()
df.rename(columns={'state/crop/district': 'region'}, inplace=True)

years = [col for col in df.columns if "-" in col]

data_list = []

for year in years:
    idx = df.columns.get_loc(year)
    temp = pd.DataFrame({
        "region": df["region"],
        "season": df["season"],
        "year": year,
        "area": df.iloc[:, idx],
        "production": df.iloc[:, idx+1],
        "yield": df.iloc[:, idx+2]
    })
    data_list.append(temp)

df_long = pd.concat(data_list, ignore_index=True)

df_long["area"] = pd.to_numeric(df_long["area"], errors="coerce")
df_long["production"] = pd.to_numeric(df_long["production"], errors="coerce")
df_long["yield"] = pd.to_numeric(df_long["yield"], errors="coerce")

df_long.dropna(inplace=True)
df_long = df_long[df_long["production"] != 0]

df_long["year_num"] = df_long["year"].str.split("-").str[0].astype(int)
df_long = df_long.sort_values(by=["region", "year_num"])

perf = df_long.groupby("region").agg({
    "production": "sum",
    "area": "sum",
    "yield": "mean"
}).reset_index()

top_perf = perf.sort_values(by="production", ascending=False).head(10)

plt.figure()
ax = sns.barplot(x="production", y="region", hue="region", data=top_perf, palette="viridis", legend=False)
for i, v in enumerate(top_perf["production"]):
    ax.text(v, i, f"{int(v)}", va='center')
plt.title("Top 10 Regions by Production", fontsize=16, weight='bold')
plt.xlabel("Total Production")
plt.ylabel("Region")
plt.tight_layout()
plt.show()

perf["efficiency"] = perf["production"] / perf["area"]
top_eff = perf.sort_values(by="efficiency", ascending=False).head(10)

plt.figure()
ax = sns.barplot(x="efficiency", y="region", hue="region", data=top_eff, palette="coolwarm", legend=False)
for i, v in enumerate(top_eff["efficiency"]):
    ax.text(v, i, f"{round(v,2)}", va='center')
plt.title("Top 10 Most Efficient Regions", fontsize=16, weight='bold')
plt.xlabel("Efficiency")
plt.ylabel("Region")
plt.tight_layout()
plt.show()

df_long["growth (%)"] = df_long.groupby("region")["production"].pct_change() * 100

top_regions = top_perf["region"].head(5)
trend_data = df_long[df_long["region"].isin(top_regions)]

plt.figure()
sns.lineplot(data=trend_data, x="year_num", y="production", hue="region", marker="o", palette="tab10")
plt.title("Production Trend (Top Regions)", fontsize=16, weight='bold')
plt.xlabel("Year")
plt.ylabel("Production")
plt.tight_layout()
plt.show()

corr = df_long[["area", "production", "yield"]].corr()

plt.figure()
sns.heatmap(corr, annot=True, cmap="YlGnBu", linewidths=1)
plt.title("Correlation Matrix", fontsize=16, weight='bold')
plt.tight_layout()
plt.show()

total = df_long["production"].sum()

contribution = df_long.groupby("region")["production"].sum().reset_index()
contribution["contribution (%)"] = (contribution["production"] / total) * 100

top_contri = contribution.sort_values(by="contribution (%)", ascending=False).head(10)

plt.figure()
ax = sns.barplot(x="contribution (%)", y="region", hue="region", data=top_contri, palette="magma", legend=False)
for i, v in enumerate(top_contri["contribution (%)"]):
    ax.text(v, i, f"{round(v,2)}%", va='center')
plt.title("Top 10 Contribution by Region", fontsize=16, weight='bold')
plt.xlabel("Contribution (%)")
plt.ylabel("Region")
plt.tight_layout()
plt.show()
