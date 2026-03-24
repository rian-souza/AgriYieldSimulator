import pandas as pd
import numpy as np
import requests
from datetime import date
import seaborn as sns
import matplotlib.pyplot as plt

latitude = 40.71
longitude = -74.01

hoje = date.today().isoformat()

url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America/New_York&start=2026-01-01&end={hoje}"

response = requests.get(url).json()

df = pd.DataFrame(response['daily'])

df['temperature_avg'] = (df['temperature_2m_max'] + df['temperature_2m_min']) / 2
df['precipitation_cumsum'] = df['precipitation_sum'].cumsum()

ideal_temp = 25
ideal_precip = 100

df['yield_sim'] = ((1 - abs(df['temperature_avg'] - ideal_temp)/10) * (df['precipitation_cumsum']/ideal_precip)).clip(0, 1)

df['temperature_norm'] = df['temperature_avg']/50
df['precipitation_norm'] = df['precipitation_cumsum']/200

sns.set(style="whitegrid")
plt.figure(figsize=(14,7))

sns.lineplot(x='time', y='yield_sim', data=df, label='Produtividade Simulada', color='green', linewidth=2.5)
sns.lineplot(x='time', y='temperature_norm', data=df, label='Temperatura Média (normalizada)', color='orange', linestyle='--', linewidth=2)
sns.lineplot(x='time', y='precipitation_norm', data=df, label='Precipitação Acumulada (normalizada)', color='blue', linestyle=':', linewidth=2)

plt.xlabel('Data', fontsize=12)
plt.ylabel('Valor Normalizado / Produtividade', fontsize=12)
plt.title('Produtividade Agrícola Simulada - Nova York, NY', fontsize=16)
plt.xticks(rotation=45)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

ideal_temp = 25
ideal_precip = 10

df['yield_sim'] = ((1 - abs(df['temperature_avg'] - ideal_temp)/10) * (df['precipitation_sum']/ideal_precip)).clip(0, 1)

def classify_yield(y):
    if y > 0.8:
        return "Colher/Plantar ideal"
    elif y < 0.3:
        return "Evitar"
    else:
        return "Período médio"

df['recommendation'] = df['yield_sim'].apply(classify_yield)

df[['time','temperature_avg','precipitation_sum','yield_sim','recommendation']].tail(10)

np.random.seed(42)

dates = pd.date_range(start="2026-03-08", periods=14)
temperature_avg = np.random.normal(loc=20, scale=5, size=14)
precipitation_sum = np.random.uniform(low=0, high=10, size=14)

df = pd.DataFrame({
    'time': dates,
    'temperature_avg': temperature_avg,
    'precipitation_sum': precipitation_sum
})

def classify_yield(y):
    if y > 0.8:
        return "Colher/Plantar ideal (Simulado)"
    elif y < 0.3:
        return "Evitar (Simulado)"
    else:
        return "Período médio (Simulado)"

df['recommendation'] = df['yield_sim'].apply(classify_yield)

palette = {'Colher/Plantar ideal (Simulado)':'green', 'Período médio (Simulado)':'orange', 'Evitar (Simulado)':'red'}

sns.set(style="whitegrid")
plt.figure(figsize=(14,7))
sns.lineplot(x='time', y='yield_sim', data=df, color='gray', linewidth=1.5, alpha=0.5)
sns.scatterplot(x='time', y='yield_sim', data=df, hue='recommendation', palette=palette, s=100)

plt.xlabel('Data', fontsize=12)
plt.ylabel('Produtividade Simulada', fontsize=12)
plt.title('Produtividade Agrícola Simulada com Recomendações (Dados Simulados) - Nova York, NY', fontsize=16)
plt.xticks(rotation=45)
plt.legend(title='Recomendação', fontsize=12)
plt.tight_layout()
plt.show()

df[['time','temperature_avg','precipitation_sum','yield_sim','recommendation']]

ideal_temp = 25
ideal_precip = 5

df['yield_sim'] = ((1 - abs(df['temperature_avg'] - ideal_temp)/10) * (df['precipitation_sum']/ideal_precip)).clip(0, 1)
