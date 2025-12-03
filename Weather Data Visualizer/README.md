
# Weather Data Visualizer

K.R. Mangalam University
Name: Harsh Singh
Roll No: 2501730400

## Overview
Loads a local weather CSV, cleans data, computes daily/monthly statistics, and saves plots.

## Files
- weather_visualizer.py
- weather_data.csv (sample)
- cleaned_weather.csv (generated)
- plots/ (generated PNGs)

## Requirements
- Python 3.8+
- pandas, numpy, matplotlib

Install:
```
pip install pandas numpy matplotlib
```

## Run
```
python weather_visualizer.py
```

## Notes
The script auto-detects common column names (temp, rain/precip, humid). Replace the CSV with your dataset.
