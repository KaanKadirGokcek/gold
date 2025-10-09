import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("goldsilver_1791-2021.csv")

#Sütun isimlerindeki boşlukları temizle
df.columns = df.columns.str.strip()

#Sütunları seç
df = df[["Year", "Gold Price"]]

#Eksik verileri at
df = df.dropna(subset=["Gold Price"])

#Tür dönüşümleri
df["Year"] = df["Year"].astype(int)
df["Gold Price"] = pd.to_numeric(df["Gold Price"], errors="coerce")

plt.figure(figsize=(12,6))
plt.plot(df["Year"], df["Gold Price"], color="gold", linewidth=2)
plt.title("Altın Fiyatlarının Tarihsel Değişimi (1791–2020)", fontsize=14)
plt.xlabel("Yıl")
plt.ylabel("Altın Fiyatı (USD / Ons)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()