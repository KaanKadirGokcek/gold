import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Veriyi Yükleme ve Temizleme
df = pd.read_csv("goldsilver_1791-2021.csv")
df.columns = df.columns.str.strip()  # Boşlukları temizle

df["Year"] = df["Year"].astype(int)
df["Gold Price"] = pd.to_numeric(df["Gold Price"], errors="coerce")
df["Silver Price"] = pd.to_numeric(df["Silver Price"], errors="coerce")
df["Gold/Silver Price Ratio"] = pd.to_numeric(df["Gold/Silver Price Ratio"], errors="coerce")
df = df.dropna()

# 2. Finansal Özet Metrikleri
start_gold = df.iloc[0]["Gold Price"]
end_gold = df.iloc[-1]["Gold Price"]
years = df.iloc[-1]["Year"] - df.iloc[0]["Year"]
cagr_gold = ((end_gold / start_gold) ** (1 / years) - 1) * 100
mean_ratio = df["Gold/Silver Price Ratio"].mean()

print(f"--- 1791-2020 FİNANSAL ÖZET ---")
print(f"Altın Başlangıç: ${start_gold:.2f} | Bitiş (2020): ${end_gold:.2f}")
print(f"Altın Yıllık Bileşik Getiri (CAGR): %{cagr_gold:.2f}")
print(f"Tarihsel Ortalama Altın/Gümüş Rasyosu: {mean_ratio:.1f}")

# 3. İki Katmanlı İnteraktif Grafik Oluşturma
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.08,
    subplot_titles=("Altın ve Gümüş Fiyat Trendi (USD/Ons)", "Altın / Gümüş Fiyat Rasyosu"),
    row_heights=[0.65, 0.35],
    specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
)

# Üst Grafik: Altın (Sol Eksen)
fig.add_trace(
    go.Scatter(x=df["Year"], y=df["Gold Price"], name="Altın (Ons)",
               line=dict(color="#FFD700", width=2.5)),
    row=1, col=1, secondary_y=False
)

# Üst Grafik: Gümüş (Sağ Eksen)
fig.add_trace(
    go.Scatter(x=df["Year"], y=df["Silver Price"], name="Gümüş (Ons)",
               line=dict(color="#C0C0C0", width=1.8, dash="dot")),
    row=1, col=1, secondary_y=True
)

# Alt Grafik: Rasyo
fig.add_trace(
    go.Scatter(x=df["Year"], y=df["Gold/Silver Price Ratio"], name="Altın/Gümüş Rasyosu",
               line=dict(color="#00CED1", width=2)),
    row=2, col=1
)

# Rasyo Tarihsel Ortalama Çizgisi
fig.add_hline(y=mean_ratio, line_dash="dash", line_color="orange",
              annotation_text=f"Ortalama ({mean_ratio:.1f})",
              annotation_position="bottom right", row=2, col=1)

# 4. Kritik Tarihsel Olaylar (Annotations)
events = [
    (1864, 42.0, "1864: İç Savaş Zirvesi"),
    (1934, 35.0, "1934: Gold Reserve Act ($35 Sabit)"),
    (1971, 41.2, "1971: Nixon Şoku (Altın Standardı Bitişi)"),
    (1980, 612.5, "1980: Enflasyon & Gümüş Krizi"),
    (2020, 1770.0, "2020: Pandemi Zirvesi")
]

for year, price, text in events:
    fig.add_annotation(
        x=year, y=price, xref="x", yref="y",
        text=text, showarrow=True, arrowhead=2,
        arrowcolor="#FF6347", bgcolor="#1e1e1e", bordercolor="#FF6347",
        font=dict(size=10, color="white"), row=1, col=1
    )

# 5. Butonlar: Logaritmik / Lineer ve Eksen Ayarları
fig.update_layout(
    title="230 Yıllık Altın ve Gümüş Dinamikleri (1791–2020)",
    template="plotly_dark",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            x=0.0, y=1.12,
            buttons=[
                dict(args=[{"yaxis.type": "linear", "yaxis2.type": "linear"}], label="Lineer Ölçek", method="relayout"),
                dict(args=[{"yaxis.type": "log", "yaxis2.type": "log"}], label="Logaritmik Ölçek", method="relayout")
            ]
        )
    ]
)

fig.update_yaxes(title_text="Altın (USD)", secondary_y=False, row=1, col=1)
fig.update_yaxes(title_text="Gümüş (USD)", secondary_y=True, row=1, col=1)
fig.update_yaxes(title_text="Rasyo Değeri", row=2, col=1)
fig.update_xaxes(title_text="Yıl", rangeslider=dict(visible=True), row=2, col=1)

fig.show()