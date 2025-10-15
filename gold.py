import pandas as pd
import plotly.express as px

df = pd.read_csv("goldsilver_1791-2021.csv")
df.columns = df.columns.str.strip()
df = df[["Year", "Gold Price"]].dropna()
df["Year"] = df["Year"].astype(int)

fig = px.line(df, x="Year", y="Gold Price",
              title="Altın Fiyatlarının Tarihsel Değişimi (1791–2020)",
              labels={"Year": "Yıl", "Gold Price": "Altın Fiyatı (USD/Ons)"},
              template="plotly_dark")

fig.update_yaxes(type="log")  # Logaritmik ölçek (isteğe bağlı)
fig.show()