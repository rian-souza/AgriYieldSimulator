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

df_real = pd.DataFrame(response['daily'])

df_real['temperature_avg'] = (df_real['temperature_2m_max'] + df_real['temperature_2m_min']) / 2
df_real['precipitation_cumsum'] = df_real['precipitation_sum'].cumsum()

ideal_temp = 25
ideal_precip = 100

df_real['yield_sim'] = (
    (1 - abs(df_real['temperature_avg'] - ideal_temp)/10) *
    (df_real['precipitation_cumsum']/ideal_precip)
).clip(0, 1)

df_real['temperature_norm'] = df_real['temperature_avg']/50
df_real['precipitation_norm'] = df_real['precipitation_cumsum']/200

sns.set(style="whitegrid")
plt.figure(figsize=(14,7))

sns.lineplot(x='time', y='yield_sim', data=df_real, label='Produtividade Simulada', linewidth=2.5)
sns.lineplot(x='time', y='temperature_norm', data=df_real, label='Temperatura Média (normalizada)', linestyle='--', linewidth=2)
sns.lineplot(x='time', y='precipitation_norm', data=df_real, label='Precipitação Acumulada (normalizada)', linestyle=':', linewidth=2)

plt.xlabel('Data')
plt.ylabel('Valor Normalizado / Produtividade')
plt.title('Produtividade Agrícola Simulada - Dados Reais')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

ideal_precip = 10

df_real['yield_sim'] = (
    (1 - abs(df_real['temperature_avg'] - ideal_temp)/10) *
    (df_real['precipitation_sum']/ideal_precip)
).clip(0, 1)

def classify_yield_real(y):
    if y > 0.8:
        return "Colher/Plantar ideal"
    elif y < 0.3:
        return "Evitar"
    else:
        return "Período médio"

df_real['recommendation'] = df_real['yield_sim'].apply(classify_yield_real)

print(df_real[['time','temperature_avg','precipitation_sum','yield_sim','recommendation']].tail(10))

np.random.seed(42)

dates = pd.date_range(start="2026-03-08", periods=14)
temperature_avg = np.random.normal(loc=20, scale=5, size=14)
precipitation_sum = np.random.uniform(low=0, high=10, size=14)

df_sim = pd.DataFrame({
    'time': dates,
    'temperature_avg': temperature_avg,
    'precipitation_sum': precipitation_sum
})

ideal_temp = 25
ideal_precip = 5

df_sim['yield_sim'] = (
    (1 - abs(df_sim['temperature_avg'] - ideal_temp)/10) *
    (df_sim['precipitation_sum']/ideal_precip)
).clip(0, 1)

def classify_yield_sim(y):
    if y > 0.8:
        return "Colher/Plantar ideal (Simulado)"
    elif y < 0.3:
        return "Evitar (Simulado)"
    else:
        return "Período médio (Simulado)"

df_sim['recommendation'] = df_sim['yield_sim'].apply(classify_yield_sim)

palette = {
    'Colher/Plantar ideal (Simulado)': 'green',
    'Período médio (Simulado)': 'orange',
    'Evitar (Simulado)': 'red'
}

sns.set(style="whitegrid")
plt.figure(figsize=(14,7))

sns.lineplot(x='time', y='yield_sim', data=df_sim, linewidth=1.5, alpha=0.5)
sns.scatterplot(x='time', y='yield_sim', data=df_sim, hue='recommendation', palette=palette, s=100)

plt.xlabel('Data')
plt.ylabel('Produtividade Simulada')
plt.title('Produtividade Agrícola Simulada com Recomendações (Dados Simulados)')
plt.xticks(rotation=45)
plt.legend(title='Recomendação')
plt.tight_layout()
plt.show()

print(df_sim[['time','temperature_avg','precipitation_sum','yield_sim','recommendation']])
