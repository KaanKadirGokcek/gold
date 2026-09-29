import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Dosya Yollarını ve Veriyi Hazırlama
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "goldsilver_1791-2021.csv")

df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()  # Sütun isimlerindeki boşlukları temizle

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

# 3. İki Katmanlı İnteraktif Grafik
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.08,
    subplot_titles=("Altın ve Gümüş Fiyat Trendi (USD/Ons)", "Altın / Gümüş Fiyat Rasyosu"),
    row_heights=[0.65, 0.35],
    specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
)

# Altın (Sol Y Ekseni)
fig.add_trace(
    go.Scatter(x=df["Year"], y=df["Gold Price"], name="Altın (Ons)",
               line=dict(color="#FFD700", width=2.5)),
    row=1, col=1, secondary_y=False
)

# Gümüş (Sağ Y Ekseni)
fig.add_trace(
    go.Scatter(x=df["Year"], y=df["Silver Price"], name="Gümüş (Ons)",
               line=dict(color="#C0C0C0", width=1.8, dash="dot")),
    row=1, col=1, secondary_y=True
)

# Altın/Gümüş Rasyosu
fig.add_trace(
    go.Scatter(x=df["Year"], y=df["Gold/Silver Price Ratio"], name="Altın/Gümüş Rasyosu",
               line=dict(color="#00CED1", width=2)),
    row=2, col=1
)

# Tarihsel Ortalama Çizgisi
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

# 5. Düzenlenmiş Yerleşim (Çakışmalar Çözüldü & Boşluklar Ferahlatıldı)
fig.update_layout(
    margin=dict(t=130, b=60, l=70, r=70),
    title=dict(
        text="<b>230 Yıllık Altın ve Gümüş Dinamikleri (1791–2020)</b>",
        x=0.01,
        y=0.97,
        xanchor="left",
        yanchor="top",
        font=dict(size=18, color="#f8fafc")
    ),
    template="plotly_dark",
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="top",
        y=1.04,
        xanchor="left",
        x=0.01,
        font=dict(size=11)
    ),
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            x=1.0,
            y=1.14,
            xanchor="right",
            yanchor="top",
            bgcolor="#1e293b",
            bordercolor="#475569",
            borderwidth=1,
            font=dict(color="#f8fafc", size=12),
            showactive=True,
            buttons=[
                dict(
                    args=[{"yaxis.type": "linear", "yaxis2.type": "linear"}],
                    label="Lineer Ölçek",
                    method="relayout"
                ),
                dict(
                    args=[{"yaxis.type": "log", "yaxis2.type": "log"}],
                    label="Logaritmik Ölçek",
                    method="relayout"
                )
            ]
        )
    ]
)

fig.update_yaxes(title_text="Altın (USD)", secondary_y=False, row=1, col=1)
fig.update_yaxes(title_text="Gümüş (USD)", secondary_y=True, row=1, col=1)
fig.update_yaxes(title_text="Rasyo Değeri", row=2, col=1)
fig.update_xaxes(title_text="Yıl", rangeslider=dict(visible=True), row=2, col=1)

# 6. HTML Kaydetme ve Buton Kontrastı için Özel CSS Stili
output_file = os.path.join(current_dir, "grafik.html")
html_content = fig.to_html(include_plotlyjs="cdn")

custom_style = """
<style>
  .updatemenu-button text {
    fill: #ffffff !important;
    font-weight: 600 !important;
  }
  .updatemenu-button rect {
    fill: #1e293b !important;
    stroke: #475569 !important;
    rx: 4px; ry: 4px;
  }
  .updatemenu-button:hover rect {
    fill: #334155 !important;
  }
  .updatemenu-button:active rect {
    fill: #b45309 !important;
    stroke: #f59e0b !important;
  }
</style>
"""

html_content = html_content.replace("</head>", f"{custom_style}</head>")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"\nGrafik başarıyla güncellendi: {output_file}")