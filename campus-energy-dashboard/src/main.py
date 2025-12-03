
import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = pd.to_datetime(timestamp)
        self.kwh = float(kwh)

class Building:
    def __init__(self, name):
        self.name = name
        self.readings = []

    def add_reading(self, reading):
        self.readings.append(reading)

    def to_dataframe(self):
        df = pd.DataFrame([{"timestamp": r.timestamp, "kwh": r.kwh} for r in self.readings])
        df = df.sort_values("timestamp").set_index("timestamp")
        return df

    def total_consumption(self):
        return sum(r.kwh for r in self.readings)

class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def load_csvs(self, data_dir):
        files = list(data_dir.glob("*.csv"))
        if not files:
            print("No CSV files found in", data_dir)
        for f in files:
            name = f.stem.split("_")[0]
            try:
                df = pd.read_csv(f, parse_dates=["timestamp"])
            except Exception as e:
                print(f"Failed to read {f}: {e}")
                continue
            if name not in self.buildings:
                self.buildings[name] = Building(name)
            for _, row in df.iterrows():
                try:
                    mr = MeterReading(row["timestamp"], row["kwh"])
                    self.buildings[name].add_reading(mr)
                except Exception as e:
                    continue

    def combined_dataframe(self):
        frames = []
        for name, b in self.buildings.items():
            df = b.to_dataframe().copy()
            df["building"] = name
            frames.append(df.reset_index())
        if frames:
            return pd.concat(frames, ignore_index=True)
        else:
            return pd.DataFrame(columns=["timestamp","kwh","building"]) 

def calculate_daily_totals(df):
    df2 = df.copy()
    df2["timestamp"] = pd.to_datetime(df2["timestamp"])
    df2 = df2.set_index("timestamp")
    daily = df2.groupby("building").resample("D")["kwh"].sum().reset_index()
    return daily

def calculate_weekly_aggregates(df):
    df2 = df.copy()
    df2["timestamp"] = pd.to_datetime(df2["timestamp"])
    df2 = df2.set_index("timestamp")
    weekly = df2.groupby("building").resample("W")["kwh"].sum().reset_index()
    return weekly

def building_wise_summary(df):
    summaries = {}
    for b, g in df.groupby("building"):
        total = g["kwh"].sum()
        summaries[b] = {
            "mean": g["kwh"].mean(),
            "min": g["kwh"].min(),
            "max": g["kwh"].max(),
            "total": total
        }
    return pd.DataFrame.from_dict(summaries, orient="index")

def main():
    manager = BuildingManager()
    manager.load_csvs(DATA_DIR)
    combined = manager.combined_dataframe()
    combined.to_csv(OUTPUT_DIR / "cleaned_energy_data.csv", index=False)

    daily = calculate_daily_totals(combined)
    weekly = calculate_weekly_aggregates(combined)
    summary = building_wise_summary(combined)
    summary.to_csv(OUTPUT_DIR / "building_summary.csv")

    combined["timestamp"] = pd.to_datetime(combined["timestamp"])
    campus_total = combined["kwh"].sum()
    highest_building = summary["total"].idxmax() if not summary.empty else "n/a"
    combined["hour"] = combined["timestamp"].dt.hour
    peak_hour = combined.groupby("hour")["kwh"].sum().idxmax() if not combined.empty else -1

    summary_txt = f"""Campus Energy Summary
Generated: {datetime.now().isoformat()}

Total campus consumption (kWh): {campus_total:.2f}
Highest-consuming building: {highest_building}
Peak load hour of day (0-23): {peak_hour}

Weekly trends: See output CSVs for per-building weekly totals.
"""
    with open(OUTPUT_DIR / "summary.txt", "w") as f:
        f.write(summary_txt)

    # Create three separate plots
    plt.figure(figsize=(10,4))
    for b, g in daily.groupby("building"):
        plt.plot(pd.to_datetime(g["timestamp"]), g["kwh"], label=b)
    plt.title("Daily consumption over time (per building)")
    plt.xlabel("Date")
    plt.ylabel("kWh (daily)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "trend_daily.png")
    plt.close()

    avg_weekly = weekly.groupby("building")["kwh"].mean().reset_index()
    plt.figure(figsize=(6,4))
    plt.bar(avg_weekly["building"], avg_weekly["kwh"])
    plt.title("Average weekly usage per building")
    plt.xlabel("Building")
    plt.ylabel("kWh (weekly average)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "avg_weekly.png")
    plt.close()

    peak_hr = combined.groupby(["building","hour\])["kwh"].sum().reset_index()
    peak_by_build = peak_hr.loc[peak_hr.groupby("building")["kwh"].idxmax()]
    plt.figure(figsize=(6,4))
    plt.scatter(peak_by_build["building"], peak_by_build["kwh"])
    plt.title("Peak-hour consumption by building (total kWh during peak hour across year)")
    plt.xlabel("Building")
    plt.ylabel("kWh (peak hour aggregated)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "peak_scatter.png")
    plt.close()

    imgs = [Image.open(OUTPUT_DIR / p) for p in ["trend_daily.png","avg_weekly.png","peak_scatter.png"]]
    widths, heights = zip(*(i.size for i in imgs))
    total_width = max(widths)
    total_height = sum(heights)
    new_im = Image.new('RGB', (total_width, total_height), (255,255,255))
    y_offset = 0
    for im in imgs:
        new_im.paste(im, (0, y_offset))
        y_offset += im.size[1]
    new_im.save(OUTPUT_DIR / "dashboard.png")

if __name__ == "__main__":
    main()
