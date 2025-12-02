# energy_dashboard.py
# Campus Energy-Use Dashboard (Capstone Project)
# Author: Yash Verma

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# ============== CONFIGURATION ==============

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)


# ============== TASK 3: OOP CLASSES ==============

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []  # list of MeterReading objects

    def add_reading(self, reading: MeterReading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

    def to_dataframe(self):
        # Convert stored readings to a pandas DataFrame
        data = {
            "timestamp": [r.timestamp for r in self.meter_readings],
            "kwh": [r.kwh for r in self.meter_readings],
            "building": [self.name] * len(self.meter_readings),
        }
        return pd.DataFrame(data)

    def generate_report(self):
        total = self.calculate_total_consumption()
        count = len(self.meter_readings)
        avg = total / count if count > 0 else 0
        report_lines = [
            f"Building: {self.name}",
            f"Total Consumption (kWh): {total:.2f}",
            f"Average Consumption per Reading (kWh): {avg:.2f}",
            f"Total Number of Readings: {count}",
        ]
        return "\n".join(report_lines)


class BuildingManager:
    def __init__(self):
        self.buildings = {}  # name -> Building object

    def get_or_create_building(self, name):
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        return self.buildings[name]

    def load_from_dataframe(self, df: pd.DataFrame):
        """
        Create Building & MeterReading objects from a pandas DataFrame.
        DataFrame must contain: timestamp (datetime64), kwh (float), building (str)
        """
        for _, row in df.iterrows():
            b_name = row["building"]
            ts = row["timestamp"]
            kwh = row["kwh"]
            building = self.get_or_create_building(b_name)
            building.add_reading(MeterReading(ts, kwh))

    def building_summaries(self):
        """Return a pandas DataFrame with building-wise summary."""
        rows = []
        for name, building in self.buildings.items():
            df_b = building.to_dataframe()
            total = df_b["kwh"].sum()
            mean = df_b["kwh"].mean()
            minimum = df_b["kwh"].min()
            maximum = df_b["kwh"].max()
            rows.append(
                {
                    "building": name,
                    "total_kwh": total,
                    "mean_kwh": mean,
                    "min_kwh": minimum,
                    "max_kwh": maximum,
                }
            )
        return pd.DataFrame(rows)


# ============== TASK 1: DATA INGESTION & VALIDATION ==============

def load_and_validate_data():
    """
    Reads all .csv files from data/ folder and combines them into a single DataFrame.
    Handles missing/corrupt files using try/except and skips bad rows.
    """
    all_frames = []
    print("🔍 Scanning data directory for CSV files...")

    if not DATA_DIR.exists():
        print(f"⚠️ data/ folder not found at {DATA_DIR.resolve()}")
        return pd.DataFrame()

    for csv_file in DATA_DIR.glob("*.csv"):
        print(f"➡ Reading file: {csv_file.name}")
        try:
            # error_bad_lines / on_bad_lines handle corrupt lines
            df = pd.read_csv(csv_file, on_bad_lines="skip")

            # Ensure required columns exist
            # Expect: timestamp, kwh
            if "timestamp" not in df.columns or "kwh" not in df.columns:
                print(f"⚠️ Skipping {csv_file.name}: missing required columns.")
                continue

            # Parse timestamp column
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df = df.dropna(subset=["timestamp", "kwh"])

            # Add metadata if not present
            building_name = csv_file.stem  # e.g., building_a
            if "building" not in df.columns:
                df["building"] = building_name

            # Optional: Add month column
            if "month" not in df.columns:
                df["month"] = df["timestamp"].dt.to_period("M").astype(str)

            all_frames.append(df)

        except FileNotFoundError:
            print(f"❌ File not found: {csv_file.name}")
        except Exception as e:
            print(f"❌ Error reading {csv_file.name}: {e}")

    if not all_frames:
        print("⚠️ No valid CSV files found in data/ directory.")
        return pd.DataFrame()

    df_combined = pd.concat(all_frames, ignore_index=True)
    print("✅ Data loaded successfully!")
    return df_combined


# ============== TASK 2: AGGREGATION LOGIC ==============

def calculate_daily_totals(df: pd.DataFrame):
    """Return DataFrame with daily total kWh per building."""
    df = df.copy()
    df.set_index("timestamp", inplace=True)
    daily = df.groupby("building")["kwh"].resample("D").sum().reset_index()
    return daily


def calculate_weekly_aggregates(df: pd.DataFrame):
    """Return DataFrame with weekly total kWh per building."""
    df = df.copy()
    df.set_index("timestamp", inplace=True)
    weekly = df.groupby("building")["kwh"].resample("W").sum().reset_index()
    return weekly


def building_wise_summary(df: pd.DataFrame):
    """Return summary DataFrame with mean, min, max, total per building."""
    summary = df.groupby("building")["kwh"].agg(
        total_kwh="sum",
        mean_kwh="mean",
        min_kwh="min",
        max_kwh="max",
    ).reset_index()
    return summary


# ============== TASK 4: VISUALIZATION DASHBOARD ==============

def create_dashboard_plots(df: pd.DataFrame, daily: pd.DataFrame, weekly: pd.DataFrame):
    """
    Create a figure with:
    1. Trend Line – daily consumption over time for all buildings
    2. Bar Chart – average weekly usage across buildings
    3. Scatter Plot – peak-hour consumption vs. time
    Saves the figure as 'dashboard.png' in output/ folder.
    """
    if df.empty:
        print("⚠️ No data available for plotting.")
        return

    # Prepare figure
    fig, axes = plt.subplots(3, 1, figsize=(10, 15))
    fig.suptitle("Campus Energy-Use Dashboard", fontsize=16)

    # 1️⃣ Line Plot – Daily trend per building
    ax1 = axes[0]
    for building_name, group in daily.groupby("building"):
        ax1.plot(group["timestamp"], group["kwh"], marker="o", label=building_name)

    ax1.set_title("Daily Electricity Consumption")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("kWh")
    ax1.legend()
    ax1.grid(True)

    # 2️⃣ Bar Chart – Average weekly usage per building
    ax2 = axes[1]
    # Compute avg weekly per building
    weekly_avg = weekly.groupby("building")["kwh"].mean().reset_index()
    ax2.bar(weekly_avg["building"], weekly_avg["kwh"])
    ax2.set_title("Average Weekly Consumption per Building")
    ax2.set_xlabel("Building")
    ax2.set_ylabel("Average kWh")

    # 3️⃣ Scatter Plot – Peak-hour consumption vs time
    ax3 = axes[2]
    df_scatter = df.copy()
    df_scatter["hour"] = df_scatter["timestamp"].dt.hour
    # For simplicity, we'll plot hour vs kwh
    ax3.scatter(df_scatter["hour"], df_scatter["kwh"])
    ax3.set_title("Peak-Hour Consumption (Hour vs kWh)")
    ax3.set_xlabel("Hour of Day")
    ax3.set_ylabel("kWh")

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    output_path = OUTPUT_DIR / "dashboard.png"
    plt.savefig(output_path)
    plt.close(fig)
    print(f"✅ Dashboard saved as: {output_path}")


# ============== TASK 5: PERSISTENCE & SUMMARY REPORT ==============

def save_outputs(df_clean: pd.DataFrame, summary_df: pd.DataFrame, manager: BuildingManager):
    # 1. Save cleaned data
    cleaned_path = OUTPUT_DIR / "cleaned_energy_data.csv"
    df_clean.to_csv(cleaned_path, index=False)
    print(f"✅ Cleaned data saved to: {cleaned_path}")

    # 2. Save building summary
    summary_path = OUTPUT_DIR / "building_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"✅ Building summary saved to: {summary_path}")

    # 3. Create text summary
    total_campus_consumption = df_clean["kwh"].sum()
    # Highest consuming building
    building_totals = summary_df.set_index("building")["total_kwh"]
    highest_building = building_totals.idxmax()
    highest_building_value = building_totals.max()

    # Peak load time (timestamp with max kwh)
    max_row = df_clean.loc[df_clean["kwh"].idxmax()]
    peak_time = max_row["timestamp"]
    peak_building = max_row["building"]
    peak_value = max_row["kwh"]

    # Simple daily & weekly trend description
    daily = calculate_daily_totals(df_clean)
    weekly = calculate_weekly_aggregates(df_clean)

    summary_lines = [
        "Campus Energy Consumption Summary",
        "=================================",
        f"Total Campus Consumption (kWh): {total_campus_consumption:.2f}",
        "",
        f"Highest Consuming Building: {highest_building} ({highest_building_value:.2f} kWh)",
        "",
        "Peak Load Details:",
        f"  Building : {peak_building}",
        f"  Time     : {peak_time}",
        f"  kWh      : {peak_value:.2f}",
        "",
        "Trends:",
        f"  Number of days recorded : {daily['timestamp'].dt.date.nunique()}",
        f"  Number of weeks recorded: {weekly['timestamp'].dt.isocalendar().week.nunique()}",
    ]

    summary_text = "\n".join(summary_lines)
    summary_file = OUTPUT_DIR / "summary.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary_text)

    print(f"✅ Summary report saved to: {summary_file}")
    print("\n------ EXECUTIVE SUMMARY ------")
    print(summary_text)
    print("------ END OF SUMMARY ------\n")


# ============== MAIN EXECUTION FLOW ==============

def main():
    print("🚀 Campus Energy-Use Dashboard started...")

    # Task 1: Load data
    df = load_and_validate_data()
    if df.empty:
        print("❌ Exiting: No data to process.")
        return

    # Task 2: Aggregations
    daily_totals = calculate_daily_totals(df)
    weekly_totals = calculate_weekly_aggregates(df)
    summary_df = building_wise_summary(df)

    # Task 3: OOP modeling
    manager = BuildingManager()
    manager.load_from_dataframe(df)

    # Task 4: Visual dashboard
    create_dashboard_plots(df, daily_totals, weekly_totals)

    # Task 5: Persistence & summary report
    save_outputs(df, summary_df, manager)

    print("✅ All tasks completed successfully!")


if __name__ == "__main__":
    main()
