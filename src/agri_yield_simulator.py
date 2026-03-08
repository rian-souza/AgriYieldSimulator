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
