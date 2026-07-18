import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import matplotlib.dates as mdates

# 1. CONNEXION (Port 5434 redirige vers 5432 dans ton docker-compose)
import os
from dotenv import load_dotenv
load_dotenv()
db_password = os.getenv('POSTGRES_PASSWORD', 'change_me')
engine = create_engine(f'postgresql://postgres:{db_password}@localhost:5434/postgres')


df_daily = pd.read_sql("SELECT * FROM weather_daily_metrics ORDER BY time", engine)
df_daily['time'] = pd.to_datetime(df_daily['time'])


df_hourly = pd.read_sql("SELECT time, temp_celsius FROM cleaned_weather_data ORDER BY time", engine)
df_hourly['time'] = pd.to_datetime(df_hourly['time'])


plt.style.use('dark_background')
sns.set_theme(style="darkgrid")


fig1, ax1 = plt.subplots(figsize=(14, 8))
sns.lineplot(data=df_daily, x='time', y='temp_moyenne', marker='o',
             color='cyan', linewidth=3, label='Temperature Moyenne', ax=ax1)
ax1.fill_between(df_daily['time'], df_daily['temp_min'], df_daily['temp_max'],
                 alpha=0.2, color='cyan', label='Plage Min/Max')

ax1.set_title('PAGE 1 : ANALYSE DES TEMPERATURES QUOTIDIENNES', fontsize=16, pad=20, color='cyan')
ax1.set_ylabel('Degres Celsius (C)', fontsize=12)
ax1.set_xlabel('Date', fontsize=12)
plt.xticks(rotation=30)
ax1.legend(loc='upper right')
plt.tight_layout()


fig2, ax2 = plt.subplots(figsize=(14, 8))
df_melt = df_daily.melt(id_vars=['time'], value_vars=['temp_min', 'temp_max'],
                        var_name='Metrique', value_name='Temp')

sns.barplot(data=df_melt, x='time', y='Temp', hue='Metrique',
            palette=['#00d4ff', '#ff4b2b'], ax=ax2)

ax2.set_title('PAGE 2 : ECART THERMIQUE MINIMAL ET MAXIMAL', fontsize=16, pad=20, color='orange')
ax2.set_ylabel('Temperature (C)', fontsize=12)
ax2.set_xlabel('Date', fontsize=12)


x_labels = df_daily['time'].dt.strftime('%Y-%m-%d')
plt.xticks(range(len(x_labels)), x_labels, rotation=30)
ax2.legend(title='Indicateurs')
plt.tight_layout()


fig3, ax3 = plt.subplots(figsize=(14, 8))
sns.lineplot(data=df_hourly, x='time', y='temp_celsius', color='#39FF14', linewidth=1.5, ax=ax3)

ax3.set_title('PAGE 3 : FLUX DE DONNEES HORAIRES (Dagster Silver Layer)', fontsize=16, pad=20, color='#39FF14')
ax3.set_ylabel('Temperature (C)', fontsize=12)
ax3.set_xlabel('Timeline (Heure par Heure)', fontsize=12)

ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %H:%M'))
plt.xticks(rotation=35)
plt.tight_layout()

# Affichage des 3 pages
plt.show()