import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

# carregar database
base_path = Path(__file__).parent
file_path = base_path / "Mix_energético.csv"

df = pd.read_csv(file_path, encoding='latin1', sep=';')

# veure columnes
print(df.columns)

# 🔥 FILTRAR ANY (2024)
df = df[df["Periodo"] == 2024]

# eliminar Total
df = df[df["Tipo de flujo energético"] != "Total"]

# labels
labels = df["Tipo de flujo energético"]

# valors (neteja)
values = df.iloc[:, -1].astype(str)
values = values.str.replace('.', '', regex=False)
values = values.str.replace(',', '.', regex=False)
values = values.astype(float)

# plot
plt.figure(figsize=(6,6))
plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)

plt.title("Distribució d'energia a Espanya (2024)")
plt.axis('equal')

plt.savefig("pie_chart.png", dpi=300)
plt.show()