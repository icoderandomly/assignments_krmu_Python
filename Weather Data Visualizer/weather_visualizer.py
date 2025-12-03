
# weather_visualizer.py
# Simple, readable script for the Weather Data Visualizer assignment.
# Place a CSV named 'weather_data.csv' in the same folder (a sample is included).

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_data(path="weather_data.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Could not find {path}. Put your CSV in the project folder.")
    df = pd.read_csv(path)
    print("Loaded data shape:", df.shape)
    return df

def clean_data(df, date_col_candidates=None):
    if date_col_candidates is None:
        date_col_candidates = ['date','Date','DATE','datetime','Timestamp']
    date_col = None
    for c in date_col_candidates:
        if c in df.columns:
            date_col = c
            break
    if date_col is None:
        # create synthetic date index
        df['Date'] = pd.date_range(start='2020-01-01', periods=len(df), freq='D')
    else:
        df['Date'] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.sort_values('Date').reset_index(drop=True)

    # detect columns
    cols = {c.lower(): c for c in df.columns}
    temp_col = next((cols[k] for k in cols if 'temp' in k), None)
    rain_col = next((cols[k] for k in cols if 'rain' in k or 'precip' in k), None)
    hum_col = next((cols[k] for k in cols if 'humid' in k), None)

    # convert to numeric and fill
    for col in [temp_col, rain_col, hum_col]:
        if col is None: continue
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(method='ffill').fillna(df[col].mean())

    # drop if essential cols absent
    return df, temp_col, rain_col, hum_col

def compute_stats(df):
    df['Day'] = df['Date'].dt.date
    daily = df.groupby('Day').agg(['mean','min','max','std'])
    df['Month'] = df['Date'].dt.to_period('M')
    monthly = df.groupby('Month').agg(['mean','min','max','std'])
    return daily, monthly

def save_cleaned(df, fname='cleaned_weather.csv'):
    df.to_csv(fname, index=False)
    print('Saved cleaned:', fname)

def make_plots(df, temp_col, rain_col, hum_col, outdir='plots'):
    os.makedirs(outdir, exist_ok=True)
    if temp_col:
        ts = df.set_index('Date').resample('D')[temp_col].mean()
        plt.figure(figsize=(10,4))
        plt.plot(ts.index, ts.values)
        plt.title('Daily Average Temperature')
        plt.xlabel('Date'); plt.ylabel('Temperature')
        plt.tight_layout()
        p = os.path.join(outdir, 'daily_temp.png')
        plt.savefig(p); plt.close(); print('Saved', p)
    if rain_col:
        mr = df.set_index('Date').resample('M')[rain_col].sum()
        plt.figure(figsize=(8,4))
        plt.bar(mr.index.astype(str), mr.values)
        plt.title('Monthly Rainfall'); plt.xticks(rotation=45)
        plt.tight_layout()
        p = os.path.join(outdir, 'monthly_rainfall.png')
        plt.savefig(p); plt.close(); print('Saved', p)
    if hum_col and temp_col:
        plt.figure(figsize=(6,5))
        plt.scatter(df[temp_col], df[hum_col], s=20)
        plt.title('Humidity vs Temperature')
        plt.xlabel(temp_col); plt.ylabel(hum_col)
        plt.tight_layout()
        p = os.path.join(outdir, 'humidity_vs_temp.png')
        plt.savefig(p); plt.close(); print('Saved', p)

def main():
    try:
        df = load_data('weather_data.csv')
        df, temp_col, rain_col, hum_col = clean_data(df)
        save_cleaned(df, 'cleaned_weather.csv')
        daily, monthly = compute_stats(df)
        print('\nDaily sample:\n', daily.head(2))
        print('\nMonthly sample:\n', monthly.head(2))
        make_plots(df, temp_col, rain_col, hum_col)
        print('\nDone. Check cleaned_weather.csv and the plots/ folder.')
    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    main()
